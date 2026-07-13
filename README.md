# playwright-pytest-swaglabs
An end-to-end (E2E) UI and API test automation portfolio for Sauce Demo using Python, Playwright, and Pytest, including comprehensive test case management with a PM mindset.

# Sauce Demo E-Commerce Test Case Matrix

## Project Positioning & Business Value

This test case matrix targets the [Sauce Demo](https://www.saucedemo.com/) e-commerce website, designed and executed by a QA engineer with a product planning background.

Test design goes beyond simple script-based click validation, incorporating product thinking and risk-based prioritization:

- **Priority Classification**: Test cases are ranked by business impact — P1 covers critical paths that directly affect conversion (core purchase flow, checkout blockers, login lockouts), while P2/P3 cover secondary features and visual defects. This helps teams focus limited time on the highest-risk paths first.
- **Business-Impacting Defect Found**: Case 2.2 identified a flow defect where the checkout page remains accessible even with an empty cart. If left unresolved in production, this type of issue would directly impact conversion rate and increase customer support load.
- **Cross-Functional Communication**: Test cases are tagged by type (UI/API) and paired with UX improvement suggestions, making the report directly actionable for PMs, designers, and engineers — not just a binary pass/fail record.

---

## Test Scope

- **Target**: Sauce Demo
- **Type**: E-commerce shopping website

---

## Case 1: Positive Scenarios (Happy Path)

| Case ID | Priority | Description / Steps | Test Type | User / Credentials | Expected Result | Actual Result | Memo |
|---|---|---|---|---|---|---|---|
| 1.1 Core Purchase Flow | P1 | 1. Log in as standard user<br>2. Add any item to cart<br>3. Go to cart page and complete checkout | UI Test | standard_user / secret_sauce | Successfully redirects to `checkout-complete.html` with a thank-you message displayed | Pass | Payment fields are not validated (name/zip code accept arbitrary input) |
| 1.2 Cart Badge Count Validation | P2 | 1. Click "Add to cart" on any item | UI Test | standard_user / secret_sauce | Cart icon badge count updates by +1 in real time | Pass | Upper limit (max quantity) not validated |
| 1.3 Remove Item from Cart | P2 | 1. Go to cart page<br>2. Click "Remove" on an item | UI Test | standard_user / secret_sauce | Item disappears from list; cart count decreases accordingly | Pass | - |

---

## Case 2: Negative Scenarios

| Case ID | Priority | Description / Steps | Test Type | User / Credentials | Expected Result | Actual Result | Memo |
|---|---|---|---|---|---|---|---|
| 2.1 Missing Required Field at Checkout (No Postal Code) | P2 | 1. Enter checkout step one<br>2. Fill in First Name / Last Name only, leave Postal Code blank | UI Test | standard_user / secret_sauce | Clicking Continue keeps user on the same page and shows a red error: `Error: Postal Code is required` | Pass | - |
| 2.2 Checkout with Empty Cart | P1 | 1. Add no items to cart<br>2. Go directly to cart and click Checkout | UI Test | standard_user / secret_sauce | An error message prompts the user to add items first | **Fail** | Checkout page is still reachable with an empty cart |
| 2.3 Invalid Username Blocked | P1 | 1. On the login page, enter an invalid username | UI Test | notexist_user / secret_sauce | An error appears above the login button: `Epic sadface: Username and password do not match any user in this service` | Pass | At 1280 x 551 viewport, the error text layout breaks |
| 2.4 Invalid Password Blocked | P1 | 1. On the login page, enter an invalid password | UI Test | standard_user / password | An error appears above the login button: `Epic sadface: Username and password do not match any user in this service` | Pass | At 1280 x 551 viewport, the error text layout breaks |
| 2.5 Locked-Out Account Blocked | P2 | 1. On the login page, log in with a locked-out account | UI Test | locked_out_user / secret_sauce | An error appears above the login button: `Epic sadface: Sorry, this user has been locked out.` | Pass | - |

---

## Case 3: Exception / Integration & API Test Scenarios

| Case ID | Priority | Description | Test Type | User / Credentials | Expected Result | Actual Result |
|---|---|---|---|---|---|---|
| 3.1 Broken Image User Validation (Problem User) | P3 | 1. Log in as the designated user and validate the broken-image state | UI Test | problem_user / secret_sauce | On the product page, some items' `src` image paths are broken (showing a placeholder dog image), and some buttons may be unresponsive | Pass |
| 3.2 Performance Glitch User | P2 | 1. Log in with the performance-glitch account and observe response time | UI Test | performance_glitch_user / secret_sauce | Login succeeds, but page load is noticeably delayed (e.g., over 5 seconds) — used to verify whether automation scripts time out or require an explicit wait | Pass |
| 3.3 Backend Product Data Retrieval | P1 | Simulate the storefront requesting the product list from a backend API | API Test | Bearer Token / API Key | Verify HTTP status `200 OK`, and that the returned JSON contains `id`, `name`, `price` fields with correct data types | *Target site has no connected backend API; implemented via a separate project instead |
| 3.4 Create Order at Checkout | P1 | Simulate the backend API receiving order data on checkout | API Test | HTTP POST Payload | Send product IDs and user data via POST; verify status `201 Created` and a unique `order_id` returned | *Target site has no connected backend API; implemented via a separate project instead |

---

## UX Improvement Recommendations

1. Items can only be added to cart one at a time (+1); there is no option to specify quantity before adding.
2. The cart displays a quantity field, but it is not editable.
3. Neither the cart page nor the checkout page displays an order subtotal / total.
4. The login page password field should include a show/hide toggle.
