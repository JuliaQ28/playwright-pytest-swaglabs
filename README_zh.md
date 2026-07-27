# Sauce Demo 電商網站測試案例矩陣

![Playwright Tests](https://github.com/JuliaQ28/playwright-pytest-swaglabs/actions/workflows/playwright.yml/badge.svg)

## 專案定位與商業價值

本測試案例矩陣以 [Sauce Demo](https://www.saucedemo.com/) 電商網站為測試對象，由具備產品企劃背景的測試工程師規劃執行。

測試設計並非單純「照劇本點擊驗證」，而是結合產品思維進行風險分級：

- **Priority 分級**：依業務影響程度區分 P1（核心購買流程、結帳異常、登入阻擋等直接影響轉單的路徑）與 P2/P3（次要功能、視覺瑕疵），協助團隊在有限時間內優先驗證高風險路徑
- **業務缺陷發現**：於 2.2 案例中發現「購物車為空仍可跳轉結帳頁」之流程缺陷，此類問題若流入正式環境將直接影響轉換率與客服負擔
- **跨角色溝通**：測試案例同時標註 UI/API 測試屬性，並附上 UIUX 優化建議，便於直接與 PM、設計、工程團隊溝通，而非僅止於通過/不通過的二元回報

---

## 測試範圍

- **Target 目標網站**：Sauce Demo
- **Type 屬性**：E-commerce shopping website 電商購物網站

---

## Case 1：正向情境 (Happy Path)

| Case ID | Priority | Description / 描述 | 測試屬性 | User / 帳號密碼 | Expected / 預期 | Actual Result | Memo / 備忘 |
|---|---|---|---|---|---|---|---|
| 1.1 核心購買流程 | P1 | 1. 登入標準用戶<br>2. 將任一商品加入購物車<br>3. 前往購物車頁面，完成結帳流程 | UI測試 | standard_user / secret_sauce | 成功跳轉至 `checkout-complete.html` 並顯示感謝購買訊息 | Pass 通過 | 刷卡資料並未進行資料驗證（姓名/zip code 可輸入任意值） |
| 1.2 購物車動態數量驗證 | P2 | 1. 任一商品點擊加入購物車按鈕 | UI測試 | standard_user / secret_sauce | 右上角購物車圖示的 Badge 數量能即時 +1 | Pass 通過 | 未驗證極限值 (Max) |
| 1.3 購物車刪除商品 | P2 | 1. 進入購物車頁面<br>2. 點擊 Remove 移除商品 | UI測試 | standard_user / secret_sauce | 商品從列表消失，且購物車數量相應扣減 | Pass 通過 | - |

---

## Case 2：反向情境

| Case ID | Priority | Description / 描述 | 測試屬性 | User / 帳號密碼 | Expected / 預期 | Actual Result | Memo / 備忘 |
|---|---|---|---|---|---|---|---|
| 2.1 結帳缺失必填欄位 (不輸入 Postal Code) | P2 | 1. 進入結帳頁第一步<br>2. 只輸入 First Name / Last Name，不輸入郵遞區號 | UI測試 | standard_user / secret_sauce | 點擊 Continue 後留在原頁，並跳出紅色錯誤提示 `Error: Postal Code is required` | Pass 通過 | - |
| 2.2 購物車為空時點擊結帳 | P1 | 1. 不加入任何商品<br>2. 直接點入購物車點擊 Checkout | UI測試 | standard_user / secret_sauce | 跳出錯誤提示，請先添加商品 | **NG 不通過** | 無商品仍會跳轉至結帳頁 |
| 2.3 錯誤帳號阻擋 | P1 | 1. [登入頁] 輸入錯誤帳號，系統進行阻擋 | UI測試 | notexist_user / secret_sauce | 登入按鈕上方提示顯示 `Epic sadface: Username and password do not match any user in this service` | Pass 通過 | 瀏覽器尺寸 1280 x 551 時，提示文字會破版 |
| 2.4 錯誤密碼阻擋 | P1 | 1. [登入頁] 輸入錯誤密碼，系統進行阻擋 | UI測試 | standard_user / password | 登入按鈕上方提示顯示 `Epic sadface: Username and password do not match any user in this service` | Pass 通過 | 瀏覽器尺寸 1280 x 551 時，提示文字會破版 |
| 2.5 登入鎖定帳號阻擋 | P2 | 1. [登入頁] 登入被鎖定帳號，系統進行阻擋 | UI測試 | locked_out_user / secret_sauce | 登入按鈕上方提示顯示 `Epic sadface: Sorry, this user has been locked out.` | Pass 通過 | - |

---

## Case 3：例外 / 整合與 API 測試情境

| Case ID | Priority | Description / 描述 | 測試屬性 | User / 帳號密碼 | Expected / 預期 | Actual Result |
|---|---|---|---|---|---|---|
| 3.1 破圖用戶驗證 (Problem User) | P3 | 1. 登入指定用戶，驗證破圖異常狀態 | UI測試 | problem_user / secret_sauce | 進入商品頁後，部分商品的 `src` 圖片路徑異常（顯示小狗破圖），或是部分按鈕點擊失效 | Pass 通過 |
| 3.2 登入效能異常用戶 | P2 | 1. 登入效能異常帳號，系統回應時間長 | UI測試 | performance_glitch_user / secret_sauce | 成功登入，但頁面載入時間明顯延遲（例如超過 5 秒），驗證自動化腳本是否會因為 Timeout 而失敗，或需加入 explicit wait | Pass 通過 |
| 3.3 後端商品資料獲取 | P1 | 模擬電商前台向後端 API 請求商品清單 | API測試 | Bearer Token / API Key | 驗證 HTTP 狀態碼為 `200 OK`，且回傳的 JSON 結構中必須包含 `id`、`name`、`price` 等欄位，且型態正確 | *目標網站無串連後端 API，已改以 reqres.in 實作，詳見 Case 4 |
| 3.4 建立訂單與購物車結帳 | P1 | 模擬點擊結帳時，後端 API 接收訂單資料 | API測試 | HTTP POST Payload | 帶入商品 ID 與用戶資料發送 POST 請求，驗證狀態碼為 `201 Created`，並回傳唯一的 `order_id` | *目標網站無串連後端 API，已改以 reqres.in 實作，詳見 Case 4 |

---

## Case 4：API 測試情境 (reqres.in)

因目標網站 Sauce Demo 無串接後端 API，原本 3.3 / 3.4 規劃的 API 測試案例改以 [reqres.in](https://reqres.in) 作為替代目標實作（詳見 `tests/api/`），用以展示 API 自動化測試能力。請求透過 Playwright 的 `APIRequestContext` 發送，回傳的 JSON 結構則以 Pydantic 定義的型別 schema（`schemas/`）進行校驗，而非逐一手動檢查 dict key。

| Case ID | Priority | Description / 描述 | 測試屬性 | Endpoint | Expected / 預期 | Actual Result | Memo / 備忘 |
|---|---|---|---|---|---|---|---|
| 4.1 取得使用者列表 (GET) | P2 | 1. 呼叫 `GET /api/users?page=2` | API測試 | reqres.in + `x-api-key` | 回傳 `200 OK`；JSON 符合 `UsersListResponse` Pydantic schema；`page == 2` 且 `data` 陣列不為空 | Pass 通過 | 結構校驗使用 Pydantic |
| 4.2 建立使用者 (POST) | P2 | 1. 呼叫 `POST /api/users`，帶入 `{name, job}` | API測試 | reqres.in + `x-api-key` | 回傳 `201 Created`；JSON 包含自動產生的 `id` 與 `createdAt` 欄位 | Pass 通過 | - |
| 4.3 登入取得 Token (POST) | P1 | 1. 呼叫 `POST /api/login`，帶入合法帳密 | API測試 | reqres.in + `x-api-key` | 回傳 `200 OK`；JSON 包含非空的 `token` 欄位 | Pass 通過 | API Key 從 `.env` 讀取（不進版本控制） |

---

## UIUX 優化建議

1. 添加商品時，僅能先 +1 (Add to cart)，無法設定想要加入購物車的數量
2. 購物車有商品數量欄位，但無法編輯數量
3. 購物車頁面、結帳頁面，未顯示整筆訂單／全部商品總額
4. 登入頁密碼，建議添加可隱藏／顯示密碼功能
