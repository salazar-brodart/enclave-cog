from .enlevel import enlevel


def setup(bot):
    n = enlevel(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)
