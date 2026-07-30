from playwright.sync_api import Page


class LoginPage:
    """登入頁 (saucedemo.com 首頁) 的 Page Object。

    把「畫面上有哪些元素」與「怎麼操作它們」封裝在這裡，
    測試檔案只呼叫下面的方法，不直接碰 locator。
    """

    def __init__(self, page: Page):
        self.page = page
        # 用 placeholder 文字定位輸入框（比 CSS class 更貼近使用者視角，且不易因改版失效）
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        # 登入失敗時顯示的紅色錯誤訊息區塊
        self.error_message = page.locator('[data-test="error"]')

    def goto(self):
        """導覽至登入頁（網站首頁本身就是登入頁）"""
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        """輸入帳號密碼並點擊登入按鈕"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        """取得登入失敗時顯示的錯誤訊息文字，供測試斷言使用"""
        return self.error_message.text_content()
