import re

from playwright.sync_api import Page, expect


def test_login_and_checkout(page: Page):
    # 1. 開啟首頁
    page.goto("https://www.saucedemo.com/")

    # 2. 登入
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # 3. 驗證成功進入商品列表頁
    expect(page).to_have_url(re.compile(r".*inventory\.html"))

    # 4. 加入第一個商品到購物車
    page.get_by_role("button", name="Add to cart").first.click()

    # 5. 點擊購物車圖示
    page.locator(".shopping_cart_link").click()

    # 6. 點擊 Checkout
    page.get_by_role("button", name="Checkout").click()

    # 7. 輸入結帳資訊（假資料）
    page.get_by_placeholder("First Name").fill("Julia")
    page.get_by_placeholder("Last Name").fill("Chen")
    page.get_by_placeholder("Zip/Postal Code").fill("100")

    # 8. 點擊 Continue -> Finish
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Finish").click()

    # 9. 最終驗證
    expect(page).to_have_url(re.compile(r".*checkout-complete\.html"))
    expect(page.get_by_text("Thank you for your order!")).to_be_visible()
