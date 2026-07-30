from playwright.sync_api import Page


class CartPage:
    """購物車頁 (cart.html) 的 Page Object。"""

    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = page.get_by_role("button", name="Checkout")

    def checkout(self):
        """點擊 Checkout 按鈕，進入結帳流程第一步 (checkout-step-one.html)"""
        self.checkout_button.click()
