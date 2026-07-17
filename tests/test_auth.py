import re

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage


def test_login_and_checkout(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_info_page = CheckoutInfoPage(page)
    checkout_overview_page = CheckoutOverviewPage(page)
    checkout_complete_page = CheckoutCompletePage(page)

    # 1. 開啟首頁
    login_page.goto()

    # 2. 登入
    login_page.login("standard_user", "secret_sauce")

    # 3. 驗證成功進入商品列表頁
    assert inventory_page.is_loaded() is True

    # 4. 加入第一個商品到購物車
    inventory_page.add_first_item_to_cart()

    # 5. 點擊購物車圖示
    inventory_page.open_cart()

    # 6. 點擊 Checkout
    cart_page.checkout()

    # 7. 輸入結帳資訊（假資料）
    checkout_info_page.fill_info("Julia", "Chen", "100")

    # 8. 點擊 Continue -> Finish
    checkout_info_page.continue_to_overview()
    checkout_overview_page.finish()

    # 9. 最終驗證
    expect(page).to_have_url(re.compile(r".*checkout-complete\.html"))
    expect(checkout_complete_page.thank_you_message).to_be_visible()
