from .enclave import enclave
from redbot.core.bot import Red


def setup(bot: Red):
    n=enclave(bot)
    bot.add_cog(n)
    bot.add_listener(n.listener, "on_message")
