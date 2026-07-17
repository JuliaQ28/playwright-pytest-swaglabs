from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage


def test_login_and_checkout(
    login_page: LoginPage,
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_info_page: CheckoutInfoPage,
    checkout_overview_page: CheckoutOverviewPage,
    checkout_complete_page: CheckoutCompletePage,
):
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
    assert checkout_complete_page.is_order_complete() is True


def test_login_with_nonexistent_user(login_page: LoginPage):
    # 1. 開啟首頁
    login_page.goto()

    # 2. 使用不存在的帳號登入
    login_page.login("notexist_user", "secret_sauce")

    # 3. 驗證錯誤提示訊息
    assert (
        login_page.get_error_message()
        == "Epic sadface: Username and password do not match any user in this service"
    )
