import pytest
from test_e2e.pages.oops_page import OopsPage


@pytest.mark.usefixtures('start_browser')
class TestOopsPage:
    def test_404_page(self):
        """
        Test content of the 404 error page
        """
        oops_page = OopsPage(self.driver)
        oops_page.open_404_page()

        assert oops_page.title() == 'Ooops, něco není dobře'
        assert oops_page.text() == 'Zdá se, že hledáte stranku, která tu není'
        assert oops_page.suggestion_text() == 'Zkusme začít od začátku'
        assert oops_page.button_text() == 'Na začátek'
