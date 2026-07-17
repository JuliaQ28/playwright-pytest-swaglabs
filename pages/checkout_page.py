import re

from playwright.sync_api import Page, expect


class CheckoutInfoPage:
    """checkout-step-one.html — 輸入結帳資訊"""

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.zip_code_input = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")

    def fill_info(self, first_name: str, last_name: str, zip_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_code_input.fill(zip_code)

    def continue_to_overview(self):
        self.continue_button.click()


class CheckoutOverviewPage:
    """checkout-step-two.html — 訂單總覽"""

    def __init__(self, page: Page):
        self.page = page
        self.finish_button = page.get_by_role("button", name="Finish")

    def finish(self):
        self.finish_button.click()


class CheckoutCompletePage:
    """checkout-complete.html — 完成訂單頁面"""

    def __init__(self, page: Page):
        self.page = page
        self.thank_you_message = page.get_by_text("Thank you for your order!")

    def is_order_complete(self) -> bool:
        expect(self.page).to_have_url(re.compile(r".*checkout-complete\.html"))
        expect(self.thank_you_message).to_be_visible()
        return True
