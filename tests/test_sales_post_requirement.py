import pytest
from pages.loginpage import LoginPage
from pages.Sales_requirement_posting_page import SalesRequirementPostingPage
from data.requirement_posting_data import TestData


def run_requirement_flow(page, credentials, logger, employee_key='shivanshu', count=5):
    page.goto("/login")
    page.wait_for_load_state("networkidle")

    login_page = LoginPage(page)
    sales_user = credentials['employees'][employee_key]
    login_page.login(sales_user['username'], sales_user['password'])
    logger.info(f"Logged in as: {sales_user['username']}")

    sales_page = SalesRequirementPostingPage(page, logger)

    stored_company = sales_page.get_company_from_client_contact()
    logger.info(f"Stored company from Client Contact Person: {stored_company}")

    sales_page.navigate_to_sales_requirement()

    for idx in range(1, count + 1):
        logger.info(f"========== Requirement {idx} START ==========")

        sales_page.click_new()
        client_name = sales_page.get_client_from_requirement_table(stored_company)
        logger.info(f"Selected client: {client_name}")

        data = TestData.generate_requirement_data()
        sales_page.post_requirement(client_name, **data)

        logger.info(f"Requirement {idx} posted: {data['job_title']} for {client_name} - Rate: ${data['rate']}/hr")

        logger.info(f"========== Requirement {idx} END ==========")


@pytest.mark.smoke
def test_sales_post_requirement(page, credentials, logger):
    run_requirement_flow(page, credentials, logger, employee_key='shivanshu', count=1)


@pytest.mark.regression
def test_sales_post_multiple_requirements(page, credentials, logger):
    run_requirement_flow(page, credentials, logger, employee_key='anil', count=3)
