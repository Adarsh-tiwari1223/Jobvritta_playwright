import pytest
from faker import Faker
from pages.loginpage import LoginPage
from Complete_PO_flow.Pages.Sales_post_requirementPage import SalesPostRequirementPage

fake = Faker()


@pytest.mark.smoke
def test_sales_post_requirement(page, credentials, logger):
    # Login as sales person
    page.goto("/login")
    page.wait_for_load_state("networkidle")
    
    login_page = LoginPage(page)
    sales_user = credentials['employees']['nitin']
    login_page.login(sales_user['username'], sales_user['password'])
    logger.info(f"Logged in as sales person: {sales_user['username']}")
    
    # Navigate to Client Contact Person and get company name
    sales_page = SalesPostRequirementPage(page)
    sales_page.navigate_to_client_contact_person()
    
    # Get random company name from table
    companies = sales_page.get_random_company_names(count=1)
    client_name = companies[0]
    logger.info(f"Selected client: {client_name}")
    
    # Navigate to Sales My Requirement
    sales_page.navigate_to_sales_requirement()
    
    # Generate fake data
    job_title = fake.job()
    rate = str(fake.random_int(min=80, max=200))
    skills = f"{fake.word().title()}, {fake.word().title()}"
    duration = str(fake.random_int(min=3, max=12))
    positions = str(fake.random_int(min=1, max=5))
    job_description = fake.text(max_nb_chars=200)
    additional_info = fake.text(max_nb_chars=150)
    
    # Post new requirement with the grabbed client
    page.wait_for_timeout(1000)  # Pause to observe
    sales_page.post_requirement(
        job_title=job_title,
        client=client_name,
        rate=rate,
        skills=skills,
        duration=duration,
        positions=positions,
        job_description=job_description,
        additional_info=additional_info
    )
    
    logger.info(f"Requirement posted: {job_title} - Rate: ${rate}/hr")


@pytest.mark.regression
def test_sales_post_multiple_requirements(page, credentials, logger):
    # Login as sales person
    page.goto("/login")
    page.wait_for_load_state("networkidle")
    
    login_page = LoginPage(page)
    sales_user = credentials['employees']['anil']
    login_page.login(sales_user['username'], sales_user['password'])
    logger.info(f"Logged in as sales person: {sales_user['username']}")
    
    # Navigate to Client Contact Person and get multiple companies
    sales_page = SalesPostRequirementPage(page)
    sales_page.navigate_to_client_contact_person()
    
    companies = sales_page.get_random_company_names(count=3)
    logger.info(f"Selected clients: {companies}")
    
    # Navigate to Sales My Requirement
    sales_page.navigate_to_sales_requirement()
    
    # Post requirements for each client
    for idx, client in enumerate(companies, 1):
        job_title = fake.job()
        rate = str(fake.random_int(min=100, max=150))
        skills = f"{fake.word().title()}, {fake.word().title()}, {fake.word().title()}"
        duration = str(fake.random_int(min=6, max=18))
        positions = str(fake.random_int(min=2, max=10))
        job_description = fake.text(max_nb_chars=250)
        additional_info = fake.text(max_nb_chars=180)
        
        sales_page.post_requirement(
            job_title=job_title,
            client=client,
            rate=rate,
            skills=skills,
            duration=duration,
            positions=positions,
            job_description=job_description,
            additional_info=additional_info
        )
        logger.info(f"Requirement {idx} posted: {job_title} for {client}")
