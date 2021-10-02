from .enclave import enclave
from .enlevel import enlevel
from redbot.core.bot import Red


def setup(bot: Red):
    n=enclave(bot)
    l=enlevel(bot)
    bot.add_cog(n)
    bot.add_cog(l)
    bot.add_listener(l.listener, "on_message")
