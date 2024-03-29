"""Module to manage rutrivia sessions."""
import asyncio
import time
import random
from collections import Counter
import discord
from redbot.core import bank, errors, commands
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box, bold, humanize_list, humanize_number
from redbot.core.utils.common_filters import normalize_smartquotes
from .log import LOG

__all__ = ["rutriviaSession"]

T_ = Translator("rutriviaSession", __file__)


_ = lambda s: s
_REVEAL_MESSAGES = (
    _("I know this one! {answer}!"),
    _("Easy: {answer}."),
    _("Oh really? It's {answer} of course."),
)

SPOILER_REVEAL_MESSAGES = (
    _("I know this one! ||{answer}!||"),
    _("Easy: ||{answer}.||"),
    _("Oh really? It's ||{answer}|| of course."),
)

_FAIL_MESSAGES = (
    _("To the next one I guess..."),
    _("Moving on..."),
    _("I'm sure you'll know the answer of the next one."),
    _("\N{PENSIVE FACE} Next one."),
)
_ = T_


class rutriviaSession:
    """Class to run a session of rutrivia with the user.

    To run the rutrivia session immediately, use `rutriviaSession.start` instead of
    instantiating directly.

    Attributes
    ----------
    ctx : `commands.Context`
        Context object from which this session will be run.
        This object assumes the session was started in `ctx.channel`
        by `ctx.author`.
    question_list : `dict`
        A list of tuples mapping questions (`str`) to answers (`list` of
        `str`).
    settings : `dict`
        Settings for the rutrivia session, with values for the following:
         - ``max_score`` (`int`)
         - ``delay`` (`float`)
         - ``timeout`` (`float`)
         - ``reveal_answer`` (`bool`)
         - ``bot_plays`` (`bool`)
         - ``allow_override`` (`bool`)
         - ``payout_multiplier`` (`float`)
    scores : `collections.Counter`
        A counter with the players as keys, and their scores as values. The
        players are of type `discord.Member`.
    count : `int`
        The number of questions which have been asked.

    """

    def __init__(self, ctx, question_list: dict, settings: dict):
        self.ctx = ctx
        list_ = list(question_list.items())
        random.shuffle(list_)
        self.question_list = list_
        self.settings = settings
        self.scores = Counter()
        self.count = 0
        self._last_response = time.time()
        self._task = None

    @classmethod
    def start(cls, ctx, question_list, settings):
        """Create and start a rutrivia session.

        This allows the session to manage the running and cancellation of its
        own tasks.

        Parameters
        ----------
        ctx : `commands.Context`
            Same as `rutriviaSession.ctx`
        question_list : `dict`
            Same as `rutriviaSession.question_list`
        settings : `dict`
            Same as `rutriviaSession.settings`

        Returns
        -------
        rutriviaSession
            The new rutrivia session being run.

        """
        session = cls(ctx, question_list, settings)
        loop = ctx.bot.loop
        session._task = loop.create_task(session.run())
        session._task.add_done_callback(session._error_handler)
        return session

    def _error_handler(self, fut):
        """Catches errors in the session task."""
        try:
            fut.result()
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            LOG.error("A rutrivia session has encountered an error.\n", exc_info=exc)
            asyncio.create_task(
                self.ctx.send(
                    _(
                        "An unexpected error occurred in the rutrivia session.\nCheck your console or logs for details."
                    )
                )
            )
            self.stop()

    async def run(self):
        """Run the rutrivia session.

        In order for the rutrivia session to be stopped correctly, this should
        only be called internally by `rutriviaSession.start`.
        """
        await self._send_startup_msg()
        max_score = self.settings["max_score"]
        delay = self.settings["delay"]
        timeout = self.settings["timeout"]
        for question, answers in self._iter_questions():
            async with self.ctx.typing():
                await asyncio.sleep(3)
            self.count += 1
            msg = await self.ctx.send(f"**Вопрос №{self.count}!**\n```fix\n" + question + "```")
            continue_ = await self.wait_for_answer(answers, delay, timeout)
            await msg.edit(f"**Вопрос №{self.count}!**\n```fix\n✅ Отвечено.```")
            if continue_ is False:
                break
            if any(score >= max_score for score in self.scores.values()):
                await self.end_game()
                break
        else:
            await self.ctx.send(_("There are no more questions!"))
            await self.end_game()

    async def _send_startup_msg(self):
        list_names = []
        for idx, tup in enumerate(self.settings["lists"].items()):
            name, author = tup
            if author:
                title = _("{rutrivia_list} (от {author})").format(rutrivia_list=name, author=author)
            else:
                title = name
            list_names.append(title)
        await self.ctx.send(
            _("Ну что, друзья, начнём нашу викторину!\n||Никому не говори, но я болею за тебя.||").format(list_names=humanize_list(list_names))
        )

    def _iter_questions(self):
        """Iterate over questions and answers for this session.

        Yields
        ------
        `tuple`
            A tuple containing the question (`str`) and the answers (`tuple` of
            `str`).

        """
        for question, answers in self.question_list:
            answers = _parse_answers(answers)
            yield question, answers

    async def wait_for_answer(self, answers, delay: float, timeout: float):
        """Wait for a correct answer, and then respond.

        Scores are also updated in this method.

        Returns False if waiting was cancelled; this is usually due to the
        session being forcibly stopped.

        Parameters
        ----------
        answers : `iterable` of `str`
            A list of valid answers to the current question.
        delay : float
            How long users have to respond (in seconds).
        timeout : float
            How long before the session ends due to no responses (in seconds).

        Returns
        -------
        bool
            :code:`True` if the session wasn't interrupted.

        """
        try:
            message = await self.ctx.bot.wait_for(
                "message", check=self.check_answer(answers), timeout=delay
            )
        except asyncio.TimeoutError:
            if time.time() - self._last_response >= timeout:
                await self.ctx.send(_("Guys...? Well, I guess I'll stop then."))
                self.stop()
                return False
            if self.settings["reveal_answer"]:
                if self.settings["use_spoilers"]:
                    reply = T_(random.choice(SPOILER_REVEAL_MESSAGES)).format(answer=answers[0])
                else:
                    reply = T_(random.choice(_REVEAL_MESSAGES)).format(answer=answers[0])
            else:
                reply = T_(random.choice(_FAIL_MESSAGES))
            if self.settings["bot_plays"]:
                reply += _(" **+1** for me!")
                self.scores[self.ctx.guild.me] += 1
            await self.ctx.send(reply)
        else:
            self.scores[message.author] += 1
            reply = _("You got it {user}! **+1** to you!").format(user=message.author.display_name)
            await self.ctx.send(reply)
        return True

    def check_answer(self, answers):
        """Get a predicate to check for correct answers.

        The returned predicate takes a message as its only parameter,
        and returns ``True`` if the message contains any of the
        given answers.

        Parameters
        ----------
        answers : `iterable` of `str`
            The answers which the predicate must check for.

        Returns
        -------
        function
            The message predicate.

        """
        answers = tuple(s.lower() for s in answers)

        def _pred(message: discord.Message):
            early_exit = message.channel != self.ctx.channel or message.author == self.ctx.guild.me
            if early_exit:
                return False

            self._last_response = time.time()
            guess = message.content.lower()
            guess = normalize_smartquotes(guess)
            for answer in answers:
                if " " in answer and answer in guess:
                    # Exact matching, issue #331
                    return True
                elif any(word == answer for word in guess.split(" ")):
                    return True
            return False

        return _pred

    async def end_game(self):
        """End the rutrivia session and display scores."""
        if self.scores:
            await self.send_table()
        multiplier = self.settings["payout_multiplier"]
        if multiplier > 0:
            await self.pay_winners(multiplier)
        self.stop()

    async def send_table(self):
        """Send a table of scores to the session's channel."""
        table = "+ Результаты: \n\n"
        for user, score in self.scores.most_common():
            table += "+ {}\t\t\t{}\n".format(user, score)
        await self.ctx.send(box(table, lang="diff"))

    def stop(self):
        """Stop the rutrivia session, without showing scores."""
        self.ctx.bot.dispatch("rutrivia_end", self)

    def force_stop(self):
        """Cancel whichever tasks this session is running."""
        self._task.cancel()
        channel = self.ctx.channel
        LOG.debug("Force stopping rutrivia session; #%s in %s", channel, channel.guild.id)

    async def pay_winners(self, multiplier: float):
        """Pay the winner(s) of this rutrivia session.

        Payout only occurs if there are at least 3 human contestants.
        If a tie occurs the payout is split evenly among the winners.

        Parameters
        ----------
        multiplier : float
            The coefficient of the winning score, used to determine the amount
            paid.

        """
        if not self.scores:
            return
        top_score = self.scores.most_common(1)[0][1]
        winners = []
        num_humans = 0
        for (player, score) in self.scores.items():
            if not player.bot:
                if score == top_score:
                    winners.append(player)
                num_humans += 1
        if not winners or num_humans < 1:
            return
        payout = int(top_score * multiplier / len(winners))
        if payout <= 0:
            return
        for winner in winners:
            LOG.debug("Paying rutrivia winner: %d credits --> %s", payout, winner.name)
            try:
                await bank.deposit_credits(winner, payout)
            except errors.BalanceTooHigh as e:
                await bank.set_balance(winner, e.max_balance)
        if len(winners) > 1:
            msg = _(
                "Congratulations {users}! You have each received {num} {currency} for winning!"
            ).format(
                users=humanize_list([bold(winner.display_name) for winner in winners]),
                num=payout,
                currency=await bank.get_currency_name(self.ctx.guild),
            )
        else:
            msg = _(
                "Congratulations {user}! You have received {num} {currency} for winning!"
            ).format(
                user=bold(winners[0].display_name),
                num=payout,
                currency=await bank.get_currency_name(self.ctx.guild),
            )
        await self.ctx.send(msg)
        await self.ruquest(ctx=self.ctx, user=winners[0])

    async def ruquest(self, ctx, user: discord.Member):
        author=user
        authbal=await bank.get_balance(author)
        max_bal=await bank.get_max_balance(guild=getattr(author, "guild", None))
        JOLA=ctx.bot.user
        NET = '❌'
        DA = '✅'
        i=0
        for r in author.roles:
            if r.name.startswith("Квест Эрудит"):
                i=23
                rr=r
        if i==0:
            return
        while i<28:
            for s in ctx.guild.roles:
                if s.name==str(rr.id)+str(i) and i<28:
                    await s.delete()
                    i=28
            i+=1
        C1=DA
        C2=DA
        C3=DA
        C4=DA
        C5=DA
        sm=""
        z=5
        for s in ctx.guild.roles:
            if s.name==str(rr.id)+"23":
                    C1=NET
                    z-=1
            if s.name==str(rr.id)+"24":
                    C2=NET
                    z-=1
            if s.name==str(rr.id)+"25":
                    C3=NET
                    z-=1
            if s.name==str(rr.id)+"26":
                    C4=NET
                    z-=1
            if s.name==str(rr.id)+"27":
                    C5=NET
                    z-=1
        await asyncio.sleep(0.5)
        if z==5:
            for r in author.roles:
                if r.name.startswith("Квест Эрудит"):
                    await r.delete()
            #p=50
            #p=await self.buffexp(ctx, author, p)
            g=1500
            if authbal>(max_bal-g):
                g=(max_bal-authbal)
            await bank.deposit_credits(author, g)
            return await ctx.send(f"{author.display_name} наглядно показывает всем в чём польза образования!\n*{author.display_name} получает кубок победителя с {g} золотыми монетами!*")
        else:
            if z==1:
                sm='четыре раза'
            elif z==2:
                sm='три раза'
            elif z==3:
                sm='два раза'
            else:
                sm='всего один раз'
            for r in author.roles:
                if r.name.startswith("Квест Эрудит"):
                    await r.edit(name="Квест Эрудит: "+C1+C2+C3+C4+C5)
            return await ctx.send(f"{author.display_name} успешно продвигается в своём задании {rr.name}! Осталось победить ещё {sm}! Не расслабляйся!")

def _parse_answers(answers):
    """Parse the raw answers to readable strings.

    The reason this exists is because of YAML's ambiguous syntax. For example,
    if the answer to a question in YAML is ``yes``, YAML will load it as the
    boolean value ``True``, which is not necessarily the desired answer. This
    function aims to undo that for bools, and possibly for numbers in the
    future too.

    Parameters
    ----------
    answers : `iterable` of `str`
        The raw answers loaded from YAML.

    Returns
    -------
    `tuple` of `str`
        The answers in readable/ guessable strings.

    """
    ret = []
    for answer in answers:
        if isinstance(answer, bool):
            if answer is True:
                ret.extend(["True", "Yes", "On"])
            else:
                ret.extend(["False", "No", "Off"])
        else:
            ret.append(str(answer))
    # Uniquify list
    seen = set()
    return tuple(x for x in ret if not (x in seen or seen.add(x)))
