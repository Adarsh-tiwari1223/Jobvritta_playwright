import random
from playwright.sync_api import Page
from pages.base_page import BasePage


class SalesRequirementPostingPage(BasePage):
    def __init__(self, page: Page, logger=None):
        super().__init__(page)
        self.logger = logger

    def _log(self, msg: str):
        if self.logger:
            self.logger.info(msg)

    def get_company_from_client_contact(self) -> str:
        self.page.get_by_role("button", name=" Masters").click()
        self.page.get_by_role("link", name=" Client Contact Person").click()
        self.page.wait_for_load_state("networkidle")
        rows = self.page.locator("//tbody/tr")
        total = rows.count()
        if total == 0:
            raise ValueError("No company names found in Client Contact Person")
        idx = random.randint(1, total)
        name = self.page.locator(f"//tbody/tr[{idx}]/td[3]").inner_text().strip()
        self._log(f"Picked company from Client Contact Person: {name}")
        return name

    def navigate_to_sales_requirement(self):
        self.page.get_by_role("button", name=" Requirement").click()
        self.page.get_by_role("link", name=" Sales My Requirement").click()
        self.page.wait_for_load_state("networkidle")
        self._log("Navigated to Sales My Requirement")

    def click_new(self):
        self.page.get_by_role("button", name="New").click()
        self.page.wait_for_load_state("networkidle")
        self._log("Clicked New button")

    def get_client_from_requirement_table(self, stored_company: str) -> str:
        combobox = self.page.get_by_role("combobox", name="Search Client/Company")
        combobox.click()
        combobox.fill(stored_company)
        self.page.wait_for_timeout(500)
        self.page.get_by_role("option").first.click()
        self._log(f"Selected suggestion: {stored_company}")

        self.page.locator(".p-button.p-component.p-button-warning").click()
        self._log("Clicked search button")

        child_dialog = self.page.locator("div.p-dialog-mask div.p-dialog-content")
        child_dialog.wait_for(state="visible", timeout=60000)
        self.page.wait_for_timeout(500)
        self._log("Child dialog table loaded")

        radio = child_dialog.locator("td > .p-radiobutton > .p-radiobutton-box").first
        radio.wait_for(state="visible", timeout=10000)
        radio.click()
        self._log("Selected first record via radio button")

        history_dialog = self.page.locator("[role='dialog']").filter(has_text="History of today posted Req")
        if history_dialog.count() > 0 and history_dialog.is_visible():
            history_dialog.locator("button[aria-label='Close']").click()
            self.page.wait_for_timeout(500)
            self._log("Closed history dialog")

        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)
        return stored_company

    def post_requirement(self, client_name: str, job_title: str, rate: str,
                         skills: str, job_term: str = "Contract", duration: str = None,
                         positions: str = "1", job_description: str = "", additional_info: str = ""):

        self.page.locator("input[name='req_Job_Title']").fill(job_title)
        self._log(f"Filled job title: {job_title}")

        self.page.locator("span").filter(has_text="Contract").click()
        self.page.get_by_role("option", name=job_term, exact=True).click()
        self._log(f"Selected job term: {job_term}")

        if job_term in ("Contract", "Contract-to-Hire") and duration:
            self.page.locator("input[name='req_Duration']").fill(duration)
            self._log(f"Filled duration: {duration}")

        self.page.locator("span").filter(has_text="Onsite").click()
        self.page.get_by_role("option", name="Remote").click()
        self._log("Selected job type: Remote")

        self.page.get_by_role("combobox", name="Search State").click()
        self.page.get_by_role("combobox", name="Search State").fill("s")
        self.page.get_by_role("option", name="Seoul").click()
        self.page.get_by_role("combobox", name="Search City").click()
        self.page.get_by_role("combobox", name="Search City").fill("s")
        self.page.get_by_role("option", name="Seoul").click()
        self._log("Selected location: Seoul")

        self.page.locator("input[name='req_Rate']").fill(rate)
        self._log(f"Filled rate: {rate}")

        self.page.locator("span").filter(has_text="Select Client Category").click()
        self.page.get_by_text("Tier 1 Vendor", exact=True).click()
        self._log("Selected client category: Tier 1 Vendor")

        self.page.locator("span").filter(has_text="Select Client Type").click()
        self.page.get_by_role("listbox").filter(has_text="Direct Client").get_by_role("option", name="Direct Client").first.click()
        self._log("Selected client type: Direct Client")

        self.page.get_by_text("Select Visa").click()
        self.page.get_by_role("checkbox").nth(2).click()
        self._log("Selected visa")

        self.page.locator("span").filter(has_text="Select Industry Type").click()
        self.page.get_by_role("option", name="dont Know").click()
        self._log("Selected industry type")

        self.page.locator("span").filter(has_text="Select Skills Category").click()
        self.page.get_by_role("option", name="ERP").click()
        self.page.locator("span").filter(has_text="Select Sub Category").click()
        self.page.get_by_role("option", name="Investment Management (SAP IM)").click()
        self._log("Selected skills category: ERP > Investment Management")

        self.page.locator("input[name='req_RequiredSkill']").fill(skills)
        self._log(f"Filled required skills: {skills}")

        self.page.locator("span").filter(has_text="Telephonic").click()
        self.page.get_by_role("option", name="Skype", exact=True).click()
        self._log("Selected interview process: Skype")

        self.page.get_by_text("Select Special Constraints").click()
        self.page.get_by_role("option", name="No Constraints").click()
        self._log("Selected special constraints: No Constraints")

        self.page.get_by_text("Select Client Communication").click()
        self.page.locator("li").filter(has_text="Phone").first.click()
        self._log("Selected client communication: Phone")

        self.fill_ckeditor_by_label("Job Description", job_description)
        self._log("Filled job description")

        self.fill_ckeditor_by_label("Additional Info", additional_info)
        self._log("Filled additional info")

        save_btn = self.page.locator("button").filter(has_text="SAVE")
        save_btn.click()
        self._log("Clicked SAVE button")
        # Wait for SAVE button to finish loading state
        self.page.wait_for_function(
            "() => !document.querySelector('button.p-button-loading')",
            timeout=60000
        )
        self._log("SAVE completed")
        try:
            self.page.locator(".p-toast-message").first.wait_for(state="visible", timeout=8000)
            toast = self.page.locator(".p-toast-message").first.inner_text().strip()
        except:
            toast = self.get_toast_message(timeout=5000)
        self._log(f"Toast: '{toast}'")
        assert toast, f"No success toast after saving requirement: '{job_title}'"
        self._log(f"Saved requirement: {job_title} - Rate: ${rate}/hr")

       
