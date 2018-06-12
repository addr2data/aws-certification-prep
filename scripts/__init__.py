"""Scripts."""

from .showregions import showregions

import logging
logger = logging.getLogger(__name__)


class ScriptError(Exception):
    """Raise exception when an error occurs."""

    def __init__(self, message):
        """Docstring."""
        err_msg = 'error:  ' + message
        logger.debug(err_msg)
        super(ScriptError, self).__init__(err_msg)
