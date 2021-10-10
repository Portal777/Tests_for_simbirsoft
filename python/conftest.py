import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def config_browser():
    browser = webdriver.Chrome()
    browser.get('http://google.com')
    yield browser
    browser.quit()
