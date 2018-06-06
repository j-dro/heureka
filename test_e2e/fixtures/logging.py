import os
import logging
import daiquiri
from pytest import fixture
from test_e2e.config import configuration
from shared.configuration import ConfigurationError

LOG_DIR = os.path.join('..', os.path.dirname(__name__))
LOG_FILENAME = os.path.join(LOG_DIR, 'testing.log')

logger = daiquiri.getLogger(__name__)


@fixture(scope='session', autouse=True)
def init_logging():
    """
    Fixture that inits logging
    """
    try:
        log_level = getattr(logging, configuration['log_level'].upper())
    except AttributeError:
        raise ConfigurationError('Invalid log level: ' + configuration['log_level'])
    daiquiri.setup(level=log_level,
                   outputs=[daiquiri.output.File(os.path.join(LOG_FILENAME))])


@fixture(autouse=True)
def log_result(request):
    """
    Fixture that logs basic info about test execution
    :param request: pytest Request object
    """
    logger.info('Starting test - ' + request.node.nodeid)
    yield
    logger.info('Test setup: %s' % request.node.rep_setup.outcome)
    try:
        logger.info('Test itself: %s' % request.node.rep_call.outcome)
    except AttributeError:
        pass
    logger.info('Test ended')
