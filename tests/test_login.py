import pytest
from ..pages.loginpage import LoginPage

@pytest.mark.smoke
def test_valid_login(page, credentials, logger):
    login_page = LoginPage(page)
    login_page.navigate("/login")
    try:
        admin = credentials['users']['admin']
    except KeyError as e:
        pytest.fail(f"Missing admin credentials in configuration: {e}")
    login_page.login(admin['username'], admin['password'])
    logger.info(f"Admin login successful for user: {admin['username']}")

@pytest.mark.regression
def test_invalid_login(page, logger):
    login_page = LoginPage(page)
    login_page.navigate("/login")
    login_page.login("invalid@email.com", "wrongpass")
    error = login_page.get_error_message()
    assert error is not None
    logger.info(f"Invalid login correctly rejected with error: {error}")