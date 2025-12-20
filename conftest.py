import pytest
from playwright.sync_api import sync_playwright
from utils.yaml_loader import load_config
from utils.logger_setup import setup_logger


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(scope="session")
def settings(config):
    return config["settings"]


@pytest.fixture(scope="session")
def credentials(config):
    return config["credentials"]     # employees + users


@pytest.fixture(scope="session")
def logger():
    return setup_logger()


@pytest.fixture
def browser_context(settings):
    base_url = settings["base_url"]
    browser_cfg = settings["browser"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=browser_cfg["headless"])
        context = browser.new_context(
            viewport=browser_cfg["viewport"],
            base_url=base_url
        )
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()
