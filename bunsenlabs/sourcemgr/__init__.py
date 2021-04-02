import logging

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s")

LOGGER_VERBOSE = logging.DEBUG
LOGGER_NONVERBOSE = logging.INFO

root_logger = logging.getLogger(__name__)
root_logger.setLevel(LOGGER_NONVERBOSE)
