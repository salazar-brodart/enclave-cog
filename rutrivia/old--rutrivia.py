"""Module for rutrivia cog."""
import asyncio
import math
import pathlib
from collections import Counter
from typing import List, Literal

import io
import yaml
import discord

from redbot.core import Config, commands, checks
from redbot.cogs.bank import is_owner_if_bank_global
from redbot.core.data_manager import cog_data_path
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import box, pagify, bold
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate

from .checks import rutrivia_stop_check
from .converters import finite_float
from .log import LOG
from .session import rutriviaSession

__all__ = ["rutrivia", "UNIQUE_ID", "get_core_lists"]

UNIQUE_ID = 0xB3C0E453

_ = Translator("rutrivia", __file__)


class InvalidListError(Exception):
    """A rutrivia list file is in invalid format."""

    pass


@cog_i18n(_)
class rutrivia(commands.Cog):
    """Play rutrivia with friends!"""

    def __init__(self):
        super().__init__()
        self.rutrivia_sessions = []
        self.config = Config.get_conf(self, identifier=UNIQUE_ID, force_registration=True)

        self.config.register_guild(
            max_score=10,
            timeout=120.0,
            delay=15.0,
            bot_plays=False,
            reveal_answer=True,
            payout_multiplier=0.0,
            allow_override=True,
        )

        self.config.register_member(wins=0, games=0, total_score=0)

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        if requester != "discord_deleted_user":
            return

        all_members = await self.config.all_members()

        async for guild_id, guild_data in AsyncIter(all_members.items(), steps=100):
            if user_id in guild_data:
                await self.config.member_from_ids(guild_id, user_id).clear()

    @commands.group()
    @commands.guild_only()
    @checks.mod_or_permissions(administrator=True)
    async def rutriviaset(self, ctx: commands.Context):
        """Manage rutrivia settings."""

    @rutriviaset.command(name="showsettings")
    async def rutriviaset_showsettings(self, ctx: commands.Context):
        """Show the current rutrivia settings."""
        settings = self.config.guild(ctx.guild)
        settings_dict = await settings.all()
        msg = box(
            _(
                "Current settings\n"
                "Bot gains points: {bot_plays}\n"
                "Answer time limit: {delay} seconds\n"
                "Lack of response timeout: {timeout} seconds\n"
                "Points to win: {max_score}\n"
                "Reveal answer on timeout: {reveal_answer}\n"
                "Payout multiplier: {payout_multiplier}\n"
                "Allow lists to override settings: {allow_override}"
            ).format(**settings_dict),
            lang="py",
        )
        await ctx.send(msg)

    @rutriviaset.command(name="maxscore")
    async def rutriviaset_max_score(self, ctx: commands.Context, score: int):
        """Set the total points required to win."""
        if score < 0:
            await ctx.send(_("Score must be greater than 0."))
            return
        settings = self.config.guild(ctx.guild)
        await settings.max_score.set(score)
        await ctx.send(_("Done. Points required to win set to {num}.").format(num=score))

    @rutriviaset.command(name="timelimit")
    async def rutriviaset_timelimit(self, ctx: commands.Context, seconds: finite_float):
        """Set the maximum seconds permitted to answer a question."""
        if seconds < 4.0:
            await ctx.send(_("Must be at least 4 seconds."))
            return
        settings = self.config.guild(ctx.guild)
        await settings.delay.set(seconds)
        await ctx.send(_("Done. Maximum seconds to answer set to {num}.").format(num=seconds))

    @rutriviaset.command(name="stopafter")
    async def rutriviaset_stopafter(self, ctx: commands.Context, seconds: finite_float):
        """Set how long until rutrivia stops due to no response."""
        settings = self.config.guild(ctx.guild)
        if seconds < await settings.delay():
            await ctx.send(_("Must be larger than the answer time limit."))
            return
        await settings.timeout.set(seconds)
        await ctx.send(
            _(
                "Done. rutrivia sessions will now time out after {num} seconds of no responses."
            ).format(num=seconds)
        )

    @rutriviaset.command(name="override")
    async def rutriviaset_allowoverride(self, ctx: commands.Context, enabled: bool):
        """Allow/disallow rutrivia lists to override settings."""
        settings = self.config.guild(ctx.guild)
        await settings.allow_override.set(enabled)
        if enabled:
            await ctx.send(
                _("Done. rutrivia lists can now override the rutrivia settings for this server.")
            )
        else:
            await ctx.send(
                _(
                    "Done. rutrivia lists can no longer override the rutrivia settings for this "
                    "server."
                )
            )

    @rutriviaset.command(name="botplays", usage="<true_or_false>")
    async def trivaset_bot_plays(self, ctx: commands.Context, enabled: bool):
        """Set whether or not the bot gains points.

        If enabled, the bot will gain a point if no one guesses correctly.
        """
        settings = self.config.guild(ctx.guild)
        await settings.bot_plays.set(enabled)
        if enabled:
            await ctx.send(_("Done. I'll now gain a point if users don't answer in time."))
        else:
            await ctx.send(_("Alright, I won't embarrass you at rutrivia anymore."))

    @rutriviaset.command(name="revealanswer", usage="<true_or_false>")
    async def trivaset_reveal_answer(self, ctx: commands.Context, enabled: bool):
        """Set whether or not the answer is revealed.

        If enabled, the bot will reveal the answer if no one guesses correctly
        in time.
        """
        settings = self.config.guild(ctx.guild)
        await settings.reveal_answer.set(enabled)
        if enabled:
            await ctx.send(_("Done. I'll reveal the answer if no one knows it."))
        else:
            await ctx.send(_("Alright, I won't reveal the answer to the questions anymore."))

    @is_owner_if_bank_global()
    @checks.admin_or_permissions(manage_guild=True)
    @rutriviaset.command(name="payout")
    async def rutriviaset_payout_multiplier(self, ctx: commands.Context, multiplier: finite_float):
        """Set the payout multiplier.

        This can be any positive decimal number. If a user wins rutrivia when at
        least 3 members are playing, they will receive credits. Set to 0 to
        disable.

        The number of credits is determined by multiplying their total score by
        this multiplier.
        """
        settings = self.config.guild(ctx.guild)
        if multiplier < 0:
            await ctx.send(_("Multiplier must be at least 0."))
            return
        await settings.payout_multiplier.set(multiplier)
        if multiplier:
            await ctx.send(_("Done. Payout multiplier set to {num}.").format(num=multiplier))
        else:
            await ctx.send(_("Done. I will no longer reward the winner with a payout."))

    @rutriviaset.group(name="custom")
    @commands.is_owner()
    async def rutriviaset_custom(self, ctx: commands.Context):
        """Manage Custom rutrivia lists."""
        pass

    @rutriviaset_custom.command(name="list")
    async def custom_rutrivia_list(self, ctx: commands.Context):
        """List uploaded custom rutrivia."""
        personal_lists = sorted([p.resolve().stem for p in cog_data_path(self).glob("*.yaml")])
        no_lists_uploaded = _("No custom rutrivia lists uploaded.")

        if not personal_lists:
            if await ctx.embed_requested():
                await ctx.send(
                    embed=discord.Embed(
                        colour=await ctx.embed_colour(), description=no_lists_uploaded
                    )
                )
            else:
                await ctx.send(no_lists_uploaded)
            return

        if await ctx.embed_requested():
            await ctx.send(
                embed=discord.Embed(
                    title=_("Uploaded rutrivia lists"),
                    colour=await ctx.embed_colour(),
                    description=", ".join(sorted(personal_lists)),
                )
            )
        else:
            msg = box(
                bold(_("Uploaded rutrivia lists")) + "\n\n" + ", ".join(sorted(personal_lists))
            )
            if len(msg) > 1000:
                await ctx.author.send(msg)
            else:
                await ctx.send(msg)

    @commands.is_owner()
    @rutriviaset_custom.command(name="upload", aliases=["add"])
    async def rutrivia_upload(self, ctx: commands.Context):
        """Upload a rutrivia file."""
        if not ctx.message.attachments:
            await ctx.send(_("Supply a file with next message or type anything to cancel."))
            try:
                message = await ctx.bot.wait_for(
                    "message", check=MessagePredicate.same_context(ctx), timeout=30
                )
            except asyncio.TimeoutError:
                await ctx.send(_("You took too long to upload a list."))
                return
            if not message.attachments:
                await ctx.send(_("You have cancelled the upload process."))
                return
            parsedfile = message.attachments[0]
        else:
            parsedfile = ctx.message.attachments[0]
        try:
            await self._save_rutrivia_list(ctx=ctx, attachment=parsedfile)
        except yaml.error.MarkedYAMLError as exc:
            await ctx.send(_("Invalid syntax: ") + str(exc))
        except yaml.error.YAMLError:
            await ctx.send(
                _("There was an error parsing the rutrivia list. See logs for more info.")
            )
            LOG.exception("Custom rutrivia file %s failed to upload", parsedfile.filename)

    @commands.is_owner()
    @rutriviaset_custom.command(name="delete", aliases=["remove"])
    async def rutrivia_delete(self, ctx: commands.Context, name: str):
        """Delete a rutrivia file."""
        filepath = cog_data_path(self) / f"{name}.yaml"
        if filepath.exists():
            filepath.unlink()
            await ctx.send(_("rutrivia {filename} was deleted.").format(filename=filepath.stem))
        else:
            await ctx.send(_("rutrivia file was not found."))

    @commands.group(invoke_without_command=True, require_var_positional=True)
    @commands.guild_only()
    async def rutrivia(self, ctx: commands.Context, *categories: str):
        """Start rutrivia session on the specified category.

        You may list multiple categories, in which case the rutrivia will involve
        questions from all of them.
        """
        categories = [c.lower() for c in categories]
        session = self._get_rutrivia_session(ctx.channel)
        if session is not None:
            await ctx.send(_("There is already an ongoing rutrivia session in this channel."))
            return
        rutrivia_dict = {}
        authors = []
        for category in reversed(categories):
            # We reverse the categories so that the first list's config takes
            # priority over the others.
            try:
                dict_ = self.get_rutrivia_list(category)
            except FileNotFoundError:
                await ctx.send(
                    _(
                        "Invalid category `{name}`. See `{prefix}rutrivia list` for a list of "
                        "rutrivia categories."
                    ).format(name=category, prefix=ctx.clean_prefix)
                )
            except InvalidListError:
                await ctx.send(
                    _(
                        "There was an error parsing the rutrivia list for the `{name}` category. It "
                        "may be formatted incorrectly."
                    ).format(name=category)
                )
            else:
                rutrivia_dict.update(dict_)
                authors.append(rutrivia_dict.pop("AUTHOR", None))
                continue
            return
        if not rutrivia_dict:
            await ctx.send(
                _("The rutrivia list was parsed successfully, however it appears to be empty!")
            )
            return
        settings = await self.config.guild(ctx.guild).all()
        config = rutrivia_dict.pop("CONFIG", None)
        if config and settings["allow_override"]:
            settings.update(config)
        settings["lists"] = dict(zip(categories, reversed(authors)))
        session = rutriviaSession.start(ctx, rutrivia_dict, settings)
        self.rutrivia_sessions.append(session)
        LOG.debug("New rutrivia session; #%s in %d", ctx.channel, ctx.guild.id)

    @rutrivia_stop_check()
    @rutrivia.command(name="stop")
    async def rutrivia_stop(self, ctx: commands.Context):
        """Stop an ongoing rutrivia session."""
        session = self._get_rutrivia_session(ctx.channel)
        if session is None:
            await ctx.send(_("There is no ongoing rutrivia session in this channel."))
            return
        await session.end_game()
        session.force_stop()
        await ctx.send(_("rutrivia stopped."))

    @rutrivia.command(name="list")
    async def rutrivia_list(self, ctx: commands.Context):
        """List available rutrivia categories."""
        lists = set(p.stem for p in self._all_lists())
        if await ctx.embed_requested():
            await ctx.send(
                embed=discord.Embed(
                    title=_("Available rutrivia lists"),
                    colour=await ctx.embed_colour(),
                    description=", ".join(sorted(lists)),
                )
            )
        else:
            msg = box(bold(_("Available rutrivia lists")) + "\n\n" + ", ".join(sorted(lists)))
            if len(msg) > 1000:
                await ctx.author.send(msg)
            else:
                await ctx.send(msg)

    @rutrivia.group(
        name="leaderboard", aliases=["lboard"], autohelp=False, invoke_without_command=True
    )
    async def rutrivia_leaderboard(self, ctx: commands.Context):
        """Leaderboard for rutrivia.

        Defaults to the top 10 of this server, sorted by total wins. Use
        subcommands for a more customised leaderboard.
        """
        cmd = self.rutrivia_leaderboard_server
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            cmd = self.rutrivia_leaderboard_global
        await ctx.invoke(cmd, "wins", 10)

    @rutrivia_leaderboard.command(name="server")
    @commands.guild_only()
    async def rutrivia_leaderboard_server(
        self, ctx: commands.Context, sort_by: str = "wins", top: int = 10
    ):
        """Leaderboard for this server.

        `<sort_by>` can be any of the following fields:
         - `wins`  : total wins
         - `avg`   : average score
         - `total` : total correct answers
         - `games` : total games played

        `<top>` is the number of ranks to show on the leaderboard.
        """
        key = self._get_sort_key(sort_by)
        if key is None:
            await ctx.send(
                _(
                    "Unknown field `{field_name}`, see `{prefix}help rutrivia leaderboard server` "
                    "for valid fields to sort by."
                ).format(field_name=sort_by, prefix=ctx.clean_prefix)
            )
            return
        guild = ctx.guild
        data = await self.config.all_members(guild)
        data = {guild.get_member(u): d for u, d in data.items()}
        data.pop(None, None)  # remove any members which aren't in the guild
        await self.send_leaderboard(ctx, data, key, top)

    @rutrivia_leaderboard.command(name="global")
    async def rutrivia_leaderboard_global(
        self, ctx: commands.Context, sort_by: str = "wins", top: int = 10
    ):
        """Global rutrivia leaderboard.

        `<sort_by>` can be any of the following fields:
         - `wins`  : total wins
         - `avg`   : average score
         - `total` : total correct answers from all sessions
         - `games` : total games played

        `<top>` is the number of ranks to show on the leaderboard.
        """
        key = self._get_sort_key(sort_by)
        if key is None:
            await ctx.send(
                _(
                    "Unknown field `{field_name}`, see `{prefix}help rutrivia leaderboard server` "
                    "for valid fields to sort by."
                ).format(field_name=sort_by, prefix=ctx.clean_prefix)
            )
            return
        data = await self.config.all_members()
        collated_data = {}
        for guild_id, guild_data in data.items():
            guild = ctx.bot.get_guild(guild_id)
            if guild is None:
                continue
            for member_id, member_data in guild_data.items():
                member = guild.get_member(member_id)
                if member is None:
                    continue
                collated_member_data = collated_data.get(member, Counter())
                for v_key, value in member_data.items():
                    collated_member_data[v_key] += value
                collated_data[member] = collated_member_data
        await self.send_leaderboard(ctx, collated_data, key, top)

    @staticmethod
    def _get_sort_key(key: str):
        key = key.lower()
        if key in ("wins", "average_score", "total_score", "games"):
            return key
        elif key in ("avg", "average"):
            return "average_score"
        elif key in ("total", "score", "answers", "correct"):
            return "total_score"

    async def send_leaderboard(self, ctx: commands.Context, data: dict, key: str, top: int):
        """Send the leaderboard from the given data.

        Parameters
        ----------
        ctx : commands.Context
            The context to send the leaderboard to.
        data : dict
            The data for the leaderboard. This must map `discord.Member` ->
            `dict`.
        key : str
            The field to sort the data by. Can be ``wins``, ``total_score``,
            ``games`` or ``average_score``.
        top : int
            The number of members to display on the leaderboard.

        Returns
        -------
        `list` of `discord.Message`
            The sent leaderboard messages.

        """
        if not data:
            await ctx.send(_("There are no scores on record!"))
            return
        leaderboard = self._get_leaderboard(data, key, top)
        ret = []
        for page in pagify(leaderboard, shorten_by=10):
            ret.append(await ctx.send(box(page, lang="py")))
        return ret

    @staticmethod
    def _get_leaderboard(data: dict, key: str, top: int):
        # Mix in average score
        for member, stats in data.items():
            if stats["games"] != 0:
                stats["average_score"] = stats["total_score"] / stats["games"]
            else:
                stats["average_score"] = 0.0
        # Sort by reverse order of priority
        priority = ["average_score", "total_score", "wins", "games"]
        try:
            priority.remove(key)
        except ValueError:
            raise ValueError(f"{key} is not a valid key.")
        # Put key last in reverse priority
        priority.append(key)
        items = data.items()
        for key in priority:
            items = sorted(items, key=lambda t: t[1][key], reverse=True)
        max_name_len = max(map(lambda m: len(str(m)), data.keys()))
        # Headers
        headers = (
            _("Rank"),
            _("Member") + " " * (max_name_len - 6),
            _("Wins"),
            _("Games Played"),
            _("Total Score"),
            _("Average Score"),
        )
        lines = [" | ".join(headers), " | ".join(("-" * len(h) for h in headers))]
        # Header underlines
        for rank, tup in enumerate(items, 1):
            member, m_data = tup
            # Align fields to header width
            fields = tuple(
                map(
                    str,
                    (
                        rank,
                        member,
                        m_data["wins"],
                        m_data["games"],
                        m_data["total_score"],
                        round(m_data["average_score"], 2),
                    ),
                )
            )
            padding = [" " * (len(h) - len(f)) for h, f in zip(headers, fields)]
            fields = tuple(f + padding[i] for i, f in enumerate(fields))
            lines.append(" | ".join(fields))
            if rank == top:
                break
        return "\n".join(lines)

    @commands.Cog.listener()
    async def on_rutrivia_end(self, session: rutriviaSession):
        """Event for a rutrivia session ending.

        This method removes the session from this cog's sessions, and
        cancels any tasks which it was running.

        Parameters
        ----------
        session : rutriviaSession
            The session which has just ended.

        """
        channel = session.ctx.channel
        LOG.debug("Ending rutrivia session; #%s in %s", channel, channel.guild.id)
        if session in self.rutrivia_sessions:
            self.rutrivia_sessions.remove(session)
        if session.scores:
            await self.update_leaderboard(session)

    async def update_leaderboard(self, session):
        """Update the leaderboard with the given scores.

        Parameters
        ----------
        session : rutriviaSession
            The rutrivia session to update scores from.

        """
        max_score = session.settings["max_score"]
        for member, score in session.scores.items():
            if member.id == session.ctx.bot.user.id:
                continue
            stats = await self.config.member(member).all()
            if score == max_score:
                stats["wins"] += 1
            stats["total_score"] += score
            stats["games"] += 1
            await self.config.member(member).set(stats)

    def get_rutrivia_list(self, category: str) -> dict:
        """Get the rutrivia list corresponding to the given category.

        Parameters
        ----------
        category : str
            The desired category. Case sensitive.

        Returns
        -------
        `dict`
            A dict mapping questions (`str`) to answers (`list` of `str`).

        """
        try:
            path = next(p for p in self._all_lists() if p.stem == category)
        except StopIteration:
            raise FileNotFoundError("Could not find the `{}` category.".format(category))

        with path.open(encoding="utf-8") as file:
            try:
                dict_ = yaml.safe_load(file)
            except yaml.error.YAMLError as exc:
                raise InvalidListError("YAML parsing failed.") from exc
            else:
                return dict_

    async def _save_rutrivia_list(
        self, ctx: commands.Context, attachment: discord.Attachment
    ) -> None:
        """Checks and saves a rutrivia list to data folder.

        Parameters
        ----------
        file : discord.Attachment
            A discord message attachment.

        Returns
        -------
        None
        """
        filename = attachment.filename.rsplit(".", 1)[0].casefold()

        # Check if rutrivia filename exists in core files or if it is a command
        if filename in self.rutrivia.all_commands or any(
            filename == item.stem for item in get_core_lists()
        ):
            await ctx.send(
                _(
                    "{filename} is a reserved rutrivia name and cannot be replaced.\n"
                    "Choose another name."
                ).format(filename=filename)
            )
            return

        file = cog_data_path(self) / f"{filename}.yaml"
        if file.exists():
            overwrite_message = _("{filename} already exists. Do you wish to overwrite?").format(
                filename=filename
            )

            can_react = ctx.channel.permissions_for(ctx.me).add_reactions
            if not can_react:
                overwrite_message += " (y/n)"

            overwrite_message_object: discord.Message = await ctx.send(overwrite_message)
            if can_react:
                # noinspection PyAsyncCall
                start_adding_reactions(
                    overwrite_message_object, ReactionPredicate.YES_OR_NO_EMOJIS
                )
                pred = ReactionPredicate.yes_or_no(overwrite_message_object, ctx.author)
                event = "reaction_add"
            else:
                pred = MessagePredicate.yes_or_no(ctx=ctx)
                event = "message"
            try:
                await ctx.bot.wait_for(event, check=pred, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(_("You took too long answering."))
                return

            if pred.result is False:
                await ctx.send(_("I am not replacing the existing file."))
                return

        buffer = io.BytesIO(await attachment.read())
        yaml.safe_load(buffer)
        buffer.seek(0)

        with file.open("wb") as fp:
            fp.write(buffer.read())
        await ctx.send(_("Saved rutrivia list as {filename}.").format(filename=filename))

    def _get_rutrivia_session(self, channel: discord.TextChannel) -> rutriviaSession:
        return next(
            (session for session in self.rutrivia_sessions if session.ctx.channel == channel), None
        )

    def _all_lists(self) -> List[pathlib.Path]:
        personal_lists = [p.resolve() for p in cog_data_path(self).glob("*.yaml")]

        return personal_lists + get_core_lists()

    def cog_unload(self):
        for session in self.rutrivia_sessions:
            session.force_stop()


def get_core_lists() -> List[pathlib.Path]:
    """Return a list of paths for all rutrivia lists packaged with the bot."""
    core_lists_path = pathlib.Path(__file__).parent.resolve() / "data/lists"
    return list(core_lists_path.glob("*.yaml"))
