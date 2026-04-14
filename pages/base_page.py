from playwright.sync_api import Page, expect
from datetime import datetime
from pathlib import Path

SCREENSHOTS_DIR = Path("reports") / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ==========================================================
    # BASIC ELEMENT INTERACTIONS
    # ==========================================================

    def find(self, selector: str):
        """Return a locator safely."""
        return self.page.locator(selector)

    def click(self, locator):
        locator.click()

    def fill(self, locator, value: str):
        locator.fill(value)

    def get_text(self, locator) -> str:
        return locator.inner_text().strip()

    def open(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def wait_for_visible(self, locator, timeout=5000):
        locator.wait_for(state="visible", timeout=timeout)

    # ==========================================================
    # DROPDOWNS — AUTO-SUGGEST / SIMPLE / MULTI-SELECT
    # ==========================================================

    def dropdown_select(self, dropdown_locator, option_text: str):
        """Click dropdown → pick option (simple select)."""
        dropdown_locator.click()
        option = self.page.get_by_role("option", name=option_text)
        expect(option).to_be_visible()
        option.click()

    def auto_suggest_select(self, input_locator, input_text: str, option_text: str):
        """Type in input → select matching suggestion (stable)."""

        # Step 1: focus + type
        input_locator.click()
        input_locator.fill("")
        input_locator.type(input_text, delay=50)

        # Step 2: wait for suggestion panel
        panel = self.page.locator(".p-autocomplete-panel, .p-dropdown-panel").last
        panel.wait_for(state="visible")

        # Step 3: select option inside panel
        option = panel.locator("li", has_text=option_text).first
        option.wait_for(state="visible")

        option.click()
        self._log(f"Selected suggestion: {option_text}")
        
    def multi_select_dropdown(self, dropdown_locator, options: list):
        """Multi-select dropdown."""
        dropdown_locator.click()
        for opt in options:
            option = self.page.get_by_role("option", name=opt)
            expect(option).to_be_visible()
            option.click()
        self.page.keyboard.press("Escape")

    def select_dropdown_option(self, dropdown_button_name: str, option_value: str):
        """Select option from dropdown by clicking button then option."""
        self.page.get_by_role("button", name=dropdown_button_name).click()
        self.page.get_by_role("option", name=option_value, exact=True).click()

    def universal_select(self, locator, value: str):
        """Automatically detect dropdown type and select."""
        tag = locator.evaluate("el => el.tagName.toLowerCase()")
        classes = locator.evaluate("el => el.className")

        # Native select
        if tag == "select":
            locator.select_option(label=value)
            return

        # Autosuggest (input)
        if tag == "input":
            self.auto_suggest_select(locator, value, value)
            return

        # Multi-select detection
        if "multi" in classes:
            self.multi_select_dropdown(locator, [value])
            return

        # Default
        self.dropdown_select(locator, value)

    # ==========================================================
    # DATE PICKER HANDLER (UNIVERSAL)
    # ==========================================================

    def select_date(self, input_locator, target_date: str):
        """
        target_date format: YYYY-MM-DD
        Works with PrimeNG, Angular Material, React, Bootstrap, etc.
        """
        from datetime import datetime
        d = datetime.strptime(target_date, "%Y-%m-%d")
        year, month, day = d.year, d.strftime("%B"), d.day

        input_locator.click()

        header = self.page.locator(
            ".p-datepicker-title, .mat-calendar-period-button, .react-datepicker__current-month"
        )

        next_btn = self.page.locator(
            ".p-datepicker-next, .mat-calendar-next-button, .react-datepicker__navigation--next"
        )

        # Navigate months
        for _ in range(12):
            hdr = header.inner_text().lower()
            if month.lower() in hdr and str(year) in hdr:
                break
            next_btn.click()

        # Pick day
        day_cell = self.page.locator(
            f"//td[normalize-space()='{day}'] | //span[normalize-space()='{day}']"
        )
        day_cell.first.click()

    # ==========================================================
    # TOAST MESSAGE READER (ALL FRAMEWORKS)
    # ==========================================================
    def get_toast_message(self, timeout=8000) -> str:
        """Fetch toast/snackbar message reliably across UI libraries."""
        try:
            toast = self.page.get_by_text("Added Successfully").first
            toast.wait_for(state="visible", timeout=timeout)
            text = toast.inner_text().strip()
            if text:
                self._log(f"Toast captured: {text}")
                return text
        except Exception:
            pass
        return ""

    # ==========================================================
    # HIGHLIGHT ELEMENT (Debugging Helper)
    # ==========================================================

    def highlight(self, locator, duration=500):
        """Temporarily highlight an element."""
        original_style = locator.evaluate("el => el.getAttribute('style')")
        locator.evaluate("el => el.setAttribute('style', 'border:3px solid red; background:yellow;')")
        self.page.wait_for_timeout(duration)
        locator.evaluate(f"el => el.setAttribute('style', '{original_style or ''}')")

    # ==========================================================
    # SCREENSHOTS (PAGE + ELEMENT)
    # ==========================================================

    def take_screenshot(self, name="screenshot", locator=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = SCREENSHOTS_DIR / f"{name}_{timestamp}.png"

        if locator:
            locator.screenshot(path=str(file_path))
        else:
            self.page.screenshot(path=str(file_path))

        return str(file_path)
    
    def fill_ckeditor_by_label(self, label_text: str, text: str):
        # Step 1: Anchor to label (flexible match)
        label = self.page.get_by_text(label_text, exact=False)

        # Step 2: Move to container
        container = label.locator("xpath=..")

        # Step 3: Locate CKEditor textbox
        editor = container.locator("div[role='textbox']")

        # Step 4: Ensure single visible editor
        editor = editor.first
        editor.wait_for(state="visible")

        # Step 5: Interact safely
        editor.click()
        editor.press("Control+A")
        editor.type(text, delay=10)  # slight delay improves stability

        self._log(f"Filled CKEditor field: {label_text}")
    