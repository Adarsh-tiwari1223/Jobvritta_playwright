from playwright.sync_api import Page
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
    
    @property
    def username_input(self):
        return self.page.get_by_role("textbox", name="UserName")
    
    @property
    def password_input(self):
        return self.page.get_by_role("textbox", name="Password")
    
    @property
    def login_button(self):
        return self.page.get_by_role("button", name="LOGIN")
    
    @property
    def secret_password_input(self):
        return self.page.get_by_role("textbox", name="Enter Secret Password")
    
    @property
    def save_button(self):
        return self.page.get_by_role("button", name="SAVE")
        
    def navigate(self, url: str):
        self.open(url)
        
    def login(self, email: str, password: str):
        self.username_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
    
    def submit_secret(self, secret: str):
        self.secret_password_input.fill(secret)
        self.save_button.click()
    
    def login_via_name(self, name: str):
        """Login using employee name from environment variables"""
        import os
        
        name_upper = name.upper().replace(' ', '_')
        username = os.getenv(f"{name_upper}_USERNAME")
        password = os.getenv(f"{name_upper}_PASSWORD")
        
        if not username or not password:
            raise ValueError(f"Credentials not found for {name}")
            
        self.login(username, password)

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