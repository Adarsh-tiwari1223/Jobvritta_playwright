import pytest
from pages.loginpage import LoginPage
#This import is used to enable assertions on Playwright elements
from playwright.sync_api import expect

@pytest.mark.smoke
def test_valid_login(page, credentials, logger):
    page.goto("/")
    page.wait_for_load_state("networkidle")
    login_page = LoginPage(page)
    try:
        admin = credentials['users']['admin']
    except KeyError as e:
        pytest.fail(f"Missing admin credentials in configuration: {e}")
    login_page.login(admin['username'], admin['password'])
    # Add assertion to verify successful login
    expect(page).to_have_url(lambda url: "/dashboard" in url or "/home" in url, timeout=10000)
    logger.info(f"Admin login successful for user: {admin['username']}")

@pytest.mark.regression
def test_invalid_login(page, logger):
    page.goto("/")
    page.wait_for_load_state("networkidle")
    login_page = LoginPage(page)
    login_page.login("invalid@email.com", "wrongpass")
    error = login_page.login_error_msg()
    assert error != "", f"Expected error message but got: '{error}'"
    logger.info(f"Invalid login correctly rejected with error: {error}")