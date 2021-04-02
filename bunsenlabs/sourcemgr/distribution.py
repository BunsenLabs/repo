import datetime
from typing import *

from pydantic import BaseModel, AnyHttpUrl

class DistributionConfiguration(BaseModel):
    url:
    origin: str
    label: str
    codename: str
    date: datetime.datetime
    components: List[

class Distribution:
    """ Representation of an APT repository distribution. """
