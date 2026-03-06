from pages.base_page import BasePage
from pages.loginpage import LoginPage
from playwright.sync_api import Page

class CategoriesPage(BasePage):
    # Locators
    CATEGORIES_LINK = "link[name=' Categories']"
    NEW_BUTTON = "button[name='New']"
    CATEGORY_NAME_INPUT = "input[name='category_Name']"
    CATEGORY_DESCRIPTION_INPUT = "input[name='category_Description']"
    STATUS_DROPDOWN = "span:has-text('Active')"
    ACTIVE_OPTION = "option[name='Active']"
    SAVE_BUTTON = "button[name='SAVE']"
    SUCCESS_MESSAGE = "text=Added Successfully"
    EDIT_BUTTON = "tr:nth-child(13) > td:nth-child(8) > .cursor-pointer"
    
    def navigate_to_categories(self):
        try:
            self.page.get_by_role("link", name=" Categories").click()
        except Exception as e:
            raise Exception(f"Failed to navigate to categories: {str(e)}")
    
    def click_new_category(self):
        try:
            self.page.get_by_role("button", name="New").click()
        except Exception as e:
            raise Exception(f"Failed to click New button: {str(e)}")
    
    def fill_category_form(self, name, description, status="Active"):
        try:
            self.page.locator("input[name='category_Name']").fill(name)
            self.page.locator("input[name='category_Description']").fill(description)
            if status:
                self.select_dropdown_option("Select Status", status)
        except Exception as e:
            raise Exception(f"Failed to fill category form: {str(e)}")
    
    def save_category(self):
        try:
            self.page.get_by_role("button", name="SAVE").click()
        except Exception as e:
            raise Exception(f"Failed to save category: {str(e)}")
    
    def verify_success_message(self):
        try:
            message = self.get_toast_message()
            return "Added Successfully" in message
        except Exception as e:
            raise Exception(f"Failed to verify success message: {str(e)}")
    
    def verify_category_in_table(self, name, description):
        try:
            name_cell = self.page.get_by_role("cell", name=name, exact=True).first
            desc_cell = self.page.get_by_role("cell", name=description).first
            return name_cell.is_visible() and desc_cell.is_visible()
        except Exception as e:
            raise Exception(f"Failed to verify category in table: {str(e)}")
    
    def edit_category(self):
        try:
            self.page.locator("tr:nth-child(13) > td:nth-child(8) > .cursor-pointer").click()
        except Exception as e:
            raise Exception(f"Failed to edit category: {str(e)}")
    
    def click_first_row_status(self):
        try:
            # Click the status column (8th column) of the first data row
            first_row_status = self.page.locator("tbody tr:first-child td:nth-child(8)")
            first_row_status.click()
        except Exception as e:
            raise Exception(f"Failed to click first row status: {str(e)}")
    
    def get_first_row_status(self):
        try:
            # Get the status text from the first row's 8th column
            first_row_status = self.page.locator("tbody tr:first-child td:nth-child(8)")
            return first_row_status.inner_text().strip()
        except Exception as e:
            raise Exception(f"Failed to get first row status: {str(e)}")
    
    def click_category_status(self, category_name):
        try:
            # Find the row containing the category name and click its status column (8th column)
            row = self.page.get_by_role("row").filter(has_text=category_name)
            status_cell = row.locator("td:nth-child(8)")
            status_cell.click()
        except Exception as e:
            raise Exception(f"Failed to click status for category {category_name}: {str(e)}")
    
    def get_category_status(self, category_name):
        try:
            # Get the current status of the category from the 8th column
            row = self.page.get_by_role("row").filter(has_text=category_name)
            status_cell = row.locator("td:nth-child(8)")
            return status_cell.inner_text().strip()
        except Exception as e:
            raise Exception(f"Failed to get status for category {category_name}: {str(e)}")
    
    def verify_update_message(self):
        try:
            message = self.get_toast_message()
            return "Updated Successfully" in message
        except Exception as e:
            raise Exception(f"Failed to verify update message: {str(e)}")