from typing import *
import logging

from bunsenlabs.sourcemgr.session import Session

from pydantic import BaseModel, AnyHttpUrl

logger = logging.getLogger(__name__)

class Remote(BaseModel):
    session: Session
    url: AnyHttpUrl

    def scan(self):
        pass

    class Config:
        arbitrary_types_allowed = True
