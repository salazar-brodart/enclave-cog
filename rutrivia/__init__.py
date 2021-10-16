"""Package for rutrivia cog."""
from .rutrivia import *
from .session import *
from .log import *


def setup(bot):
    """Load rutrivia."""
    cog = rutrivia()
    bot.add_cog(cog)
