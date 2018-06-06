import pytest
import daiquiri
import test_e2e.libs.browser as browser

logger = daiquiri.getLogger(__name__)


@pytest.fixture()
def start_browser(request):
    """
    Fixture for starting and stopping the browser
    :param request: pytest Request object
    """
    instance = request.node.parent.obj
    instance.driver = browser.start_browser(request.node.nodeid)
    yield

    if (request.node.rep_setup.failed or request.node.rep_call.failed) and instance.driver:
        browser.save_screenshot(instance.driver, request.node.name + '.png')

    browser.stop_browser(instance.driver)
