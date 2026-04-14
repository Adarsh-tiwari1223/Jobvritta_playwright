import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils.yaml_loader import load_config
from utils.logger_setup import setup_logger

SCREENSHOTS_DIR = Path("reports") / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")


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
def browser_context(settings, request):
    base_url = settings["base_url"]
    browser_cfg = settings["browser"]
    headless = request.config.getoption("--headless") or browser_cfg["headless"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport=browser_cfg["viewport"],
            base_url=base_url
        )
        context.set_default_timeout(60000)  # 60 seconds for slow tables
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context, request):
    page = browser_context.new_page()
    yield page
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = SCREENSHOTS_DIR / f"FAILED_{request.node.name}_{timestamp}.png"
        page.screenshot(path=str(path))
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
