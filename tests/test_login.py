import pytest
from pages.loginpage import LoginPage
from playwright.sync_api import expect

@pytest.mark.smoke
def test_valid_login(page, credentials, logger):
    # Navigate to login page
    page.goto("/login")
    page.wait_for_load_state("networkidle")
    
    login_page = LoginPage(page)
    
    # Get admin credentials
    try:
        admin = credentials['users']['admin']
    except KeyError as e:
        pytest.fail(f"Missing admin credentials in configuration: {e}")
    
    # Perform login
    login_page.login(admin['username'], admin['password'])
    
    # Submit secret password for admin
    page.wait_for_timeout(2000)
    secret = credentials['secret']['password']
    login_page.submit_secret(secret)
    
    # Verify successful login (check URL redirect)
    page.wait_for_timeout(3000)  # Wait for redirect
    current_url = page.url
    assert "/login" not in current_url, f"Login failed - still on login page: {current_url}"
    
    logger.info(f"Admin login successful for user: {admin['username']}")

@pytest.mark.regression
def test_invalid_login(page, logger):
    # Navigate to login page
    page.goto("/login")
    page.wait_for_load_state("networkidle")
    
    login_page = LoginPage(page)
    
    # Test with empty credentials to trigger validation errors
    login_page.login("", "")
    
    # Verify error messages appear
    error = login_page.login_error_msg()
    assert error != "", f"Expected error message but got: '{error}'"
    
    logger.info(f"Invalid login correctly rejected with error: {error}")