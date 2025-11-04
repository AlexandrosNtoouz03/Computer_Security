import base64, haslib, hmac, json, os, time
from typing import Optional

_DATA = None
_ATTEMPTS: dict