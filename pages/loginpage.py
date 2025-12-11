from playwright.sync_api import Page
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = "input[type='email'], input[name='email'], #email"
    PASSWORD_INPUT = "input[type='password'], input[name='password'], #password"
    LOGIN_BUTTON = "button[type='submit'], input[type='submit'], .login-btn"
    SECRET_PASSWORD_INPUT = "textbox[name='Enter Secret Password']"
    SAVE_BUTTON = "button[name='SAVE']"
    # Error message locator
    USERNAME_REQUIRED_ERROR = "text='Username is required'"
    PASSWORD_REQUIRED_ERROR = "text='Password is required'"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    def navigate(self, url: str):
        self.open(url)
        
    def login(self, email: str, password: str):
        self.fill(self.find(self.USERNAME_INPUT), email)
        self.fill(self.find(self.PASSWORD_INPUT), password)
        self.click(self.find(self.LOGIN_BUTTON))
    
    def submit_secret(self, secret: str):
        self.page.get_by_role("textbox", name="Enter Secret Password").fill(secret)
        self.page.get_by_role("button", name="SAVE").click()

    def login_error_msg(self) -> str:
        """Get login error message text."""
        error_selectors = [
            self.USERNAME_REQUIRED_ERROR,
            self.PASSWORD_REQUIRED_ERROR,
            ".error, .alert, .message"
        ]
        
        for selector in error_selectors:
            try:
                element = self.find(selector)
                if element.is_visible():
                    return self.get_text(element)
            except:
                continue
        return ""