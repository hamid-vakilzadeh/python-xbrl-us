__version__ = "0.0.0"

from .fact import FactSearch
from .oauth2 import AuthorizationGrant

"""

A simple Python wrapper for XBRL US API
Read more at XBRL US API documentation: https://xbrlus.github.io/xbrl-api/#/

    - test
"""


__all__ = ["AuthorizationGrant", "FactSearch"]
