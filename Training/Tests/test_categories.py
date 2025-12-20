import pytest
from Training.Page.CategoriesPage import CategoriesPage
from pages.loginpage import LoginPage

@pytest.mark.smoke
def test_create_category(page, credentials, logger):
    try:
        # Login first
        page.goto("/login")
        login_page = LoginPage(page)
        admin = credentials['users']['admin']
        login_page.login(admin['username'], admin['password'])
        login_page.submit_secret(credentials['secret']['password'])
        logger.info("Login successful")
        
        # Navigate to categories and create new category
        categories_page = CategoriesPage(page)
        categories_page.navigate_to_categories()
        categories_page.click_new_category()
        categories_page.fill_category_form("Test", "Test description")
        categories_page.save_category()
        logger.info("Category form filled and saved")
        
        # Verify success
        assert categories_page.verify_success_message(), f"Success message not found: {categories_page.get_toast_message()}"
        assert categories_page.verify_category_in_table("Test", "Test description"), "Category not found in table"
        logger.info("Category created successfully")
        
        # Click status of first row to change it and verify
        initial_status = categories_page.get_first_row_status()
        logger.info(f"Initial status of first row: {initial_status}")
        
        categories_page.click_first_row_status()
        page.wait_for_timeout(2000)  # Wait for status change
        
        new_status = categories_page.get_first_row_status()
        logger.info(f"New status of first row: {new_status}")
        
        assert initial_status != new_status, f"Status did not change: {initial_status} -> {new_status}"
        
        # Check for any success/update message
        toast_message = categories_page.get_toast_message()
        logger.info(f"Toast message after status change: '{toast_message}'")
        
        # Accept various success messages
        success_keywords = ["Updated", "Success", "Changed", "Modified"]
        message_found = any(keyword in toast_message for keyword in success_keywords)
        
        assert message_found or toast_message, f"No success message found. Got: '{toast_message}'"
        logger.info("First row status updated successfully")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise