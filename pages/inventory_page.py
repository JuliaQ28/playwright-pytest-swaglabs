import re

from playwright.sync_api import Page, expect


class InventoryPage:
    """商品列表頁 (inventory.html) 的 Page Object。"""

    def __init__(self, page: Page):
        self.page = page
        # 畫面上每個商品都有一個「Add to cart」按鈕，用 role+name 一次定位到一整組
        self.add_to_cart_buttons = page.get_by_role("button", name="Add to cart")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.page_title = page.locator(".title")

    def add_first_item_to_cart(self):
        """把清單中第一個商品加入購物車（.first 取第一個符合條件的元素）"""
        self.add_to_cart_buttons.first.click()

    def open_cart(self):
        """點擊右上角購物車圖示，前往購物車頁面"""
        self.cart_icon.click()

    def is_loaded(self) -> bool:
        """驗證目前確實停留在商品列表頁：網址符合 inventory.html，且標題顯示 'Products'。

        expect() 是 Playwright 的 auto-retrying assertion，會在逾時前重複輪詢直到條件成立，
        比單純比對字串更能容忍網路延遲造成的非同步渲染。
        """
        expect(self.page).to_have_url(re.compile(r".*inventory\.html"))
        expect(self.page_title).to_have_text("Products")
        return True
