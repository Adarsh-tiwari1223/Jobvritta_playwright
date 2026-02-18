from playwright.sync_api import Page
import random


class SalesPostRequirementPage:
    def __init__(self, page: Page):
        self.page = page

    # Job Details Section
    @property
    def new_button(self):
        return self.page.get_by_role("button", name="New")

    @property
    def client_search(self):
        return self.page.get_by_role("combobox", name="Search Client/Company")

    @property
    def job_title_input(self):
        return self.page.locator("input[name='req_Job_Title']")

    @property
    def duration_input(self):
        return self.page.get_by_role("spinbutton")

    @property
    def state_search(self):
        return self.page.get_by_role("combobox", name="Search State")

    @property
    def city_search(self):
        return self.page.get_by_role("combobox", name="Search City")

    @property
    def rate_input(self):
        return self.page.locator("input[name='req_Rate']")

    @property
    def end_client_search(self):
        return self.page.get_by_role("combobox", name="Search End Client")

    # Position & Category Details
    @property
    def positions_input(self):
        return self.page.get_by_role("spinbutton")

    # Authorization & Constraints
    @property
    def required_skill_input(self):
        return self.page.locator("input[name='req_RequiredSkill']")

    # Description Fields
    @property
    def job_description_editor(self):
        return self.page.get_by_role("paragraph").first

    @property
    def additional_info_editor(self):
        return self.page.get_by_role("paragraph").nth(1)

    # Action Controls
    @property
    def save_button(self):
        return self.page.get_by_role("button", name="SAVE")

    @property
    def clear_button(self):
        return self.page.get_by_role("button", name="CLEAR")

    @property
    def close_button(self):
        return self.page.get_by_role("button", name="Close")

    def navigate_to_client_contact_person(self):
        self.page.get_by_role("button", name=" Masters").click()
        self.page.get_by_role("link", name=" Client Contact Person").click()

    def get_company_name_from_table(self, company_name: str) -> str:
        """Get company name from table by clicking on cell"""
        cell = self.page.get_by_role("cell", name=company_name)
        cell.dblclick()
        return company_name

    def get_random_company_names(self, count=10):
        """Get random company names from the table"""
        # Wait for table to load
        self.page.wait_for_selector("td:has(span:text('Company Name'))", timeout=60000)
        company_cells = self.page.locator("td:has(span:text('Company Name'))")
        total = company_cells.count()
        
        if total == 0:
            raise ValueError("No company names found in table")
        
        indices = random.sample(range(total), min(count, total))
        return [
            company_cells.nth(i).inner_text().replace("Company Name", "").strip()
            for i in indices
        ]

    def navigate_to_sales_requirement(self):
        self.page.get_by_role("button", name=" Requirement").click()
        self.page.get_by_role("link", name=" Sales My Requirement").click()

    def click_new_requirement(self):
        self.new_button.click()

    def select_client(self, client_name: str):
        self.client_search.click()
        self.client_search.fill(client_name)
        self.page.get_by_role("option", name=client_name).click()

    def select_job_term(self, term: str):
        self.page.locator("span").filter(has_text="Contract").click()
        self.page.get_by_role("option", name=term).click()

    def select_job_type(self, job_type: str):
        self.page.locator("span").filter(has_text="Onsite").click()
        self.page.get_by_role("option", name=job_type).click()

    def select_location(self, state: str, city: str):
        self.state_search.click()
        self.state_search.fill(state)
        self.page.get_by_role("option", name=state).click()
        self.city_search.click()
        self.city_search.fill(city)
        self.page.get_by_role("option", name=city).click()

    def select_industry(self, industry: str):
        self.page.locator("span").filter(has_text="Select Industry Type").click()
        self.page.get_by_role("option", name=industry).click()

    def select_skills_category(self, category: str, sub_category: str = None):
        self.page.locator("span").filter(has_text="Select Skills Category").click()
        self.page.get_by_role("option", name=category).click()
        if sub_category:
            self.page.locator("span").filter(has_text="Select Sub Category").click()
            self.page.get_by_role("option", name=sub_category).click()

    def select_priority(self, priority: str):
        self.page.locator("span").filter(has_text="High").click()
        self.page.get_by_role("option", name=priority, exact=True).click()

    def select_client_details(self, client_category: str, client_type: str):
        self.page.locator("span").filter(has_text="Select Client Category").click()
        self.page.wait_for_selector("li[role='option']", state="visible")
        self.page.get_by_role("option", name=client_category, exact=True).click()
        
        self.page.locator("span").filter(has_text="Select Client Type").click()
        self.page.wait_for_selector("li[role='option']", state="visible")
        self.page.get_by_role("option", name=client_type, exact=True).click()

    def select_work_authorization(self, *visa_types):
        self.page.get_by_text("Select Visa").click()
        for idx in range(len(visa_types)):
            self.page.locator(f"li:nth-child({idx+1}) > .p-checkbox > .p-checkbox-box").click()

    def select_interview_process(self, process: str):
        self.page.locator("span").filter(has_text="Telephonic").click()
        self.page.get_by_role("option", name=process, exact=True).click()

    def select_special_constraints(self, *constraints):
        self.page.get_by_text("Select Special Constraints").click()
        for idx in range(len(constraints)):
            self.page.locator(f"li:nth-child({idx+1}) > .p-checkbox > .p-checkbox-box").click()

    def select_client_communication(self, communication: str):
        self.page.locator("div").filter(has_text="Select Client Communication").nth(4).click()
        self.page.get_by_text(communication, exact=True).click()

    def post_requirement(self, job_title: str, client: str, rate: str, skills: str,
                        duration: str = "6", positions: str = "1",
                        job_description: str = "Job description here",
                        additional_info: str = "Additional info here",
                        state: str = "Ohio", city: str = "Ohio City"):
        """Post requirement with all mandatory fields"""
        self.click_new_requirement()
        self.select_client(client)
        self.job_title_input.fill(job_title)
        self.select_job_term("Permanent")
        self.duration_input.fill(duration)
        self.select_job_type("Hybrid")
        self.select_location(state, city)
        self.rate_input.fill(rate)
        self.select_industry("Banking & Finance")
        self.positions_input.fill(positions)
        self.select_skills_category("DevOps", "Azure")
        self.select_priority("High")
        self.select_client_details("Direct Client", "Direct Client")
        self.select_work_authorization("H1B", "GC")
        self.select_interview_process("Telephonic")
        self.select_special_constraints("None")
        self.select_client_communication("Phone")
        self.required_skill_input.fill(skills)
        self.job_description_editor.fill(job_description)
        self.additional_info_editor.fill(additional_info)
        self.save_button.click()