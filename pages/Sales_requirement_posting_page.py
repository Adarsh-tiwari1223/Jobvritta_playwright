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

    def _click_radio_in_dialog(self) -> bool:
        try:
            radio = self.page.locator("div.p-dialog-content").locator("td > .p-radiobutton > .p-radiobutton-box").first
            radio.wait_for(state="visible", timeout=5000)
            radio.click()
            self._log("Radio found — selected directly")
            return True
        except Exception:
            self._log("No radio found in dialog")
            return False

    def _search_and_select_client(self, stored_company: str):
        self._log("No radio found — running search flow")
        dialog = self.page.locator("div.p-dialog-content")

        combobox = dialog.get_by_role("combobox", name="Search Client/Company")
        combobox.wait_for(state="visible", timeout=10000)
        combobox.click()
        combobox.fill(stored_company)
        self._log(f"Filled combobox with: {stored_company}")

        suggestion = self.page.get_by_role("option").filter(has_text=stored_company).first
        suggestion.wait_for(state="visible", timeout=5000)
        suggestion.click()
        self._log(f"Picked suggestion: {stored_company}")

        dialog.locator(".p-button.p-component.p-button-warning").click()
        self._log("Clicked Search button")

        radio = dialog.locator("td > .p-radiobutton > .p-radiobutton-box").first
        radio.wait_for(state="visible", timeout=60000)
        radio.click()
        self._log("Selected radio after search")

    def _close_history_dialog(self):
        try:
            history_close = self.page.locator("[role='dialog']").filter(
                has_text="History of today posted Req"
            ).locator("button[aria-label='Close']")
            history_close.wait_for(state="visible", timeout=3000)
            history_close.click()
            self._log("Closed history dialog")
        except Exception:
            pass

    def select_client(self, stored_company: str = None) -> str:
        if self._click_radio_in_dialog():
            self._close_history_dialog()
            self.page.wait_for_load_state("networkidle")
            company = stored_company or self.page.locator("div.p-dialog-content td:nth-child(3)").first.inner_text().strip()
            self._log(f"Client selected: {company}")
            return company

        # No radio — go fetch company from Masters
        company = self.get_company_from_client_contact()
        self._log(f"Fetched company from Masters: {company}")

        # Return to Sales My Requirement and click New again
        self.navigate_to_sales_requirement()
        self.click_new()

        # Now search and select
        self._search_and_select_client(company)
        self._close_history_dialog()
        self.page.wait_for_load_state("networkidle")
        return company

    def _fill_job_title(self, job_title: str):
        self.page.locator("input[name='req_Job_Title']").fill(job_title)
        self._log(f"Filled job title: {job_title}")

    def _select_job_term(self, job_term: str, duration: str = None):
        self.page.locator("span").filter(has_text="Contract").click()
        self.page.get_by_role("option", name=job_term, exact=True).click()
        self._log(f"Selected job term: {job_term}")
        if job_term in ("Contract", "Contract-to-Hire") and duration:
            self.page.locator("input[name='req_Duration']").fill(duration)
            self._log(f"Filled duration: {duration}")

    def _select_job_type(self):
        self.page.locator("span").filter(has_text="Onsite").click()
        self.page.get_by_role("option", name="Remote").click()
        self._log("Selected job type: Remote")

    def _select_location(self):
        self.page.get_by_role("combobox", name="Search State").click()
        self.page.get_by_role("combobox", name="Search State").fill("s")
        self.page.get_by_role("option", name="Seoul").click()
        self.page.get_by_role("combobox", name="Search City").click()
        self.page.get_by_role("combobox", name="Search City").fill("s")
        self.page.get_by_role("option", name="Seoul").click()
        self._log("Selected location: Seoul")

    def _fill_rate(self, rate: str):
        self.page.locator("input[name='req_Rate']").fill(rate)
        self._log(f"Filled rate: {rate}")

    def _select_client_category(self):
        self.page.locator("span").filter(has_text="Select Client Category").click()
        self.page.get_by_text("Tier 1 Vendor", exact=True).click()
        self._log("Selected client category: Tier 1 Vendor")

    def _select_client_type(self):
        self.page.locator("span").filter(has_text="Select Client Type").click()
        self.page.get_by_role("listbox").filter(has_text="Direct Client").get_by_role("option", name="Direct Client").first.click()
        self._log("Selected client type: Direct Client")

    def _select_visa(self):
        self.page.get_by_text("Select Visa").click()
        self.page.get_by_role("checkbox").nth(2).click()
        self._log("Selected visa")

    def _select_industry_type(self):
        self.page.locator("span").filter(has_text="Select Industry Type").click()
        self.page.get_by_role("option", name="dont Know").click()
        self._log("Selected industry type")

    def _select_skills_category(self, category: str, subcategory: str):
        self.page.locator("span").filter(has_text="Select Skills Category").click()
        self.page.get_by_role("option", name=category).click()
        self.page.locator("span").filter(has_text="Select Sub Category").click()
        self.page.get_by_role("option", name=subcategory).click()
        self._log(f"Selected skills category: {category} > {subcategory}")

    def _fill_required_skills(self, skills: str):
        self.page.locator("input[name='req_RequiredSkill']").fill(skills)
        self._log(f"Filled required skills: {skills}")

    def _select_interview_process(self):
        self.page.locator("span").filter(has_text="Telephonic").click()
        self.page.get_by_role("option", name="Skype", exact=True).click()
        self._log("Selected interview process: Skype")

    def _select_special_constraints(self):
        self.page.get_by_text("Select Special Constraints").click()
        self.page.get_by_role("option", name="No Constraints").click()
        self._log("Selected special constraints: No Constraints")

    def _select_client_communication(self):
        self.page.get_by_text("Select Client Communication").click()
        self.page.locator("li").filter(has_text="Phone").first.click()
        self._log("Selected client communication: Phone")

    def _fill_descriptions(self, job_description: str, additional_info: str):
        self.fill_ckeditor_by_label("Job Description", job_description)
        self._log("Filled job description")
        self.fill_ckeditor_by_label("Additional Info", additional_info)
        self._log("Filled additional info")

    def _save_and_assert_toast(self, job_title: str, rate: str):
        self.page.locator("button").filter(has_text="SAVE").click()
        self._log("Clicked SAVE button")

        toast = ""
        for selector in [".p-toast-detail", ".p-toast-summary", ".p-toast-message-text", ".p-toast-message"]:
            try:
                el = self.page.locator(selector).first
                el.wait_for(state="attached", timeout=120000)
                toast = el.inner_text().strip()
                if toast:
                    break
            except Exception:
                continue

        self._log(f"Toast: '{toast}'")
        self.page.wait_for_timeout(4000)
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        assert toast, f"No success toast after saving requirement: '{job_title}'"
        self._log(f"Saved requirement: {job_title} - Rate: ${rate}/hr")

    def post_requirement(self, client_name: str, job_title: str, rate: str,
                         skills: str, job_term: str = "Contract", duration: str = None,
                         positions: str = "1", job_description: str = "", additional_info: str = ""):
        self._fill_job_title(job_title)
        self._select_job_term(job_term, duration)
        self._select_job_type()
        self._select_location()
        self._fill_rate(rate)
        self._select_client_category()
        self._select_client_type()
        self._select_visa()
        self._select_industry_type()
        self._select_skills_category("JAVA/J2EE", "Java Lead")
        self._fill_required_skills(skills)
        self._select_interview_process()
        self._select_special_constraints()
        self._select_client_communication()
        self._fill_descriptions(job_description, additional_info)
        self._save_and_assert_toast(job_title, rate)
