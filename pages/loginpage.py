from playwright.sync_api import Page
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators - Based on actual Jobvritta application
    USERNAME_INPUT = "textbox[name='UserName']"
    PASSWORD_INPUT = "textbox[name='Password']"
    LOGIN_BUTTON = "button[name='LOGIN']"
    SECRET_PASSWORD_INPUT = "textbox[name='Enter Secret Password']"
    SAVE_BUTTON = "button[name='SAVE']"
    DASHBOARD_LINK = "text='Dashboard'"
    # Error message locator
    USERNAME_REQUIRED_ERROR = "text='Username is required'"
    PASSWORD_REQUIRED_ERROR = "text='Password is required'"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    def navigate(self, url: str):
        self.open(url)
        
    def login(self, email: str, password: str):
        self.page.get_by_role("textbox", name="UserName").fill(email)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="LOGIN").click()
    
    def submit_secret(self, secret: str):
        self.page.get_by_role("textbox", name="Enter Secret Password").fill(secret)
        self.page.get_by_role("button", name="SAVE").click()

    def login_error_msg(self) -> str:
        """Get login error message text."""
        # Wait a moment for error to appear
        self.page.wait_for_timeout(1000)
        
        # Check for specific Jobvritta error messages
        error_messages = []
        
        # Check for username required error
        try:
            username_error = self.page.get_by_text("username is required*")
            if username_error.is_visible():
                error_messages.append("username is required")
        except:
            pass
            
        # Check for password required error
        try:
            password_error = self.page.get_by_text("password is required*")
            if password_error.is_visible():
                error_messages.append("password is required")
        except:
            pass
        
        # Return combined error messages
        if error_messages:
            return ", ".join(error_messages)
        
        # Check if still on login page (indicates failed login)
        if "/login" in self.page.url:
            return "Login failed - still on login page"
        
        return ""