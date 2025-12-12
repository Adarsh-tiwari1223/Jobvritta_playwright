import pytest
from pages.loginpage import LoginPage
#This import is used to enable assertions on Playwright elements
from playwright.sync_api import expect

@pytest.mark.smoke
def test_valid_login(page, credentials, logger):
    page.goto("/")
    page.wait_for_load_state("networkidle")
    
    # Debug: Take screenshot and print page content
    page.screenshot(path="reports/screenshots/debug_page.png")
    print(f"Page title: {page.title()}")
    print(f"Page URL: {page.url}")
    logger.info(f"Page title: {page.title()}")
    logger.info(f"Page URL: {page.url}")
    
    login_page = LoginPage(page)
    try:
        admin = credentials['users']['admin']
    except KeyError as e:
        pytest.fail(f"Missing admin credentials in configuration: {e}")
    
    # Navigate directly to login page
    page.goto("/login")
    page.wait_for_load_state("networkidle")
    print("Navigated to login page")
    
    login_page.login(admin['username'], admin['password'])
    print(f"Login attempted for user: {admin['username']}")
    logger.info(f"Login attempted for user: {admin['username']}")

@pytest.mark.regression
def test_invalid_login(page, logger):
    page.goto("/")
    page.wait_for_load_state("networkidle")
    
    # Navigate directly to login page
    page.goto("/login")
    page.wait_for_load_state("networkidle")
    
    login_page = LoginPage(page)
    # Test with empty credentials to trigger validation errors
    login_page.login("", "")
    print("Empty login attempted, checking for validation errors...")
    error = login_page.login_error_msg()
    print(f"Error message found: '{error}'")
    assert error != "", f"Expected error message but got: '{error}'"
    logger.info(f"Invalid login correctly rejected with error: {error}")