import urllib.parse
import logging

from bunsenlabs.sourcemgr.session import Session
from bunsenlabs.sourcemgr.remote import Remote

import click
from pydantic.error_wrappers import ValidationError

logger = logging.getLogger(__name__)

@click.command("scan")
@click.argument("url")
def scan(url: str) -> int:
    """ Discover remote distributions and components. """
    session = Session()
    try:
        remote = Remote(session=session, url=url)
    except ValidationError as err:
        logger.error("invalid parameters: %s", err)
        raise click.Abort(err)

@click.group()
@click.option("--verbose", is_flag=True, default=False, help="enable verbose debug logging")
def entrypoint(verbose: bool) -> int:
    """ apt-sourcemgr is a simple command line interface for managing the local configuration of APT
    package sources. """

    if verbose:
        from bunsenlabs.sourcemgr import root_logger, LOGGER_VERBOSE
        root_logger.setLevel(LOGGER_VERBOSE)

entrypoint.add_command(scan)
