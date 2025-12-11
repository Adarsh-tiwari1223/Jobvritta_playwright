from playwright.sync_api import Page
from ..locators.login_locators import LoginLocators

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        
    def navigate(self, url: str):
        self.page.goto(url)
        
    def login(self, email: str, password: str):
        self.page.fill(LoginLocators.EMAIL_INPUT, email)
        self.page.fill(LoginLocators.PASSWORD_INPUT, password)
        self.page.click(LoginLocators.LOGIN_BUTTON)
        
    def get_error_message(self):
        return self.page.text_content(LoginLocators.ERROR_MESSAGE)