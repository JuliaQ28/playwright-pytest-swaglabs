import re

from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.add_to_cart_buttons = page.get_by_role("button", name="Add to cart")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.page_title = page.locator(".title")

    def add_first_item_to_cart(self):
        self.add_to_cart_buttons.first.click()

    def open_cart(self):
        self.cart_icon.click()

    def is_loaded(self) -> bool:
        expect(self.page).to_have_url(re.compile(r".*inventory\.html"))
        expect(self.page_title).to_have_text("Products")
        return True
