# playwright-pytest-swaglabs

![Playwright Tests](https://github.com/JuliaQ28/playwright-pytest-swaglabs/actions/workflows/playwright.yml/badge.svg)

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

## Tech Stack & Test Architecture

- **Page Object Model (`pages/`)**: Each real page (login, inventory, cart, checkout) has its own class encapsulating that page's locators and user actions (e.g. `LoginPage.login()`, `InventoryPage.is_loaded()`). Test files never touch raw locators directly — they only call page object methods, so a UI change only requires updating one class instead of every test that touches that page.
- **Pytest Fixtures (`tests/conftest.py`)**: Every page object is exposed as a fixture (`login_page`, `inventory_page`, `cart_page`, …) that auto-injects the underlying Playwright `page`. Test functions simply declare the fixtures they need as parameters — no manual `LoginPage(page)` instantiation inside test bodies.
- **Schema Validation with Pydantic (`schemas/`)**: API responses are validated against typed models (`UsersListResponse`, `LoginResponse`, …) instead of ad-hoc dict key checks — a missing field or wrong type raises a precise `ValidationError` instead of a confusing `KeyError`.
- **Test Markers (`smoke` / `regression`)**: Tests are tagged so CI can run a fast smoke subset (critical paths) separately from the full regression suite — see [pytest.ini](pytest.ini).
- **CI/CD (`.github/workflows/playwright.yml`)**: GitHub Actions runs the full suite on every push/PR, generates a self-contained `pytest-html` report, uploads it as a build artifact, and can optionally publish it to GitHub Pages on manual trigger.
- **Secrets Management**: API keys are loaded from a local `.env` file (via `python-dotenv`, gitignored) locally, and from GitHub Actions Secrets in CI — never hardcoded in source.

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
| 2.3 Invalid Username Blocked | P1 | 1. On the login page, enter an invalid username | UI Test | notexist_user / secret_sauce | An error appears above the login button: `Epic sadface: Username and password do not match any user in this service` | Pass | At 1280 x 551 viewport, the error text layout breaks. Implemented together with 2.4 as one data-driven `@pytest.mark.parametrize` test (`test_login_with_invalid_credentials`) instead of two near-duplicate test functions |
| 2.4 Invalid Password Blocked | P1 | 1. On the login page, enter an invalid password | UI Test | standard_user / password | An error appears above the login button: `Epic sadface: Username and password do not match any user in this service` | Pass | Same parametrized test as 2.3 — see Memo above |
| 2.5 Locked-Out Account Blocked | P2 | 1. On the login page, log in with a locked-out account | UI Test | locked_out_user / secret_sauce | An error appears above the login button: `Epic sadface: Sorry, this user has been locked out.` | Pass | - |

---

## Case 3: Exception / Integration & API Test Scenarios

| Case ID | Priority | Description | Test Type | User / Credentials | Expected Result | Actual Result |
|---|---|---|---|---|---|---|
| 3.1 Broken Image User Validation (Problem User) | P3 | 1. Log in as the designated user and validate the broken-image state | UI Test | problem_user / secret_sauce | On the product page, some items' `src` image paths are broken (showing a placeholder dog image), and some buttons may be unresponsive | Pass |
| 3.2 Performance Glitch User | P2 | 1. Log in with the performance-glitch account and observe response time | UI Test | performance_glitch_user / secret_sauce | Login succeeds, but page load is noticeably delayed (e.g., over 5 seconds) — used to verify whether automation scripts time out or require an explicit wait | Pass |
| 3.3 Backend Product Data Retrieval | P1 | Simulate the storefront requesting the product list from a backend API | API Test | Bearer Token / API Key | Verify HTTP status `200 OK`, and that the returned JSON contains `id`, `name`, `price` fields with correct data types | *Target site has no connected backend API; implemented against reqres.in instead — see Case 4 |
| 3.4 Create Order at Checkout | P1 | Simulate the backend API receiving order data on checkout | API Test | HTTP POST Payload | Send product IDs and user data via POST; verify status `201 Created` and a unique `order_id` returned | *Target site has no connected backend API; implemented against reqres.in instead — see Case 4 |

---

## Case 4: API Test Scenarios (reqres.in)

Since Sauce Demo has no connected backend API, the API test cases originally planned in 3.3 / 3.4 were implemented against [reqres.in](https://reqres.in) instead, as a stand-in target for demonstrating API automation skills (`tests/api/`). Requests are sent via Playwright's `APIRequestContext`, and response bodies are validated against typed schemas defined with Pydantic (`schemas/`) rather than raw dict key checks.

| Case ID | Priority | Description / Steps | Test Type | Endpoint | Expected Result | Actual Result | Memo |
|---|---|---|---|---|---|---|---|
| 4.1 Get User List (GET) | P2 | 1. Call `GET /api/users?page=2` | API Test | reqres.in + `x-api-key` | Returns `200 OK`; JSON matches the `UsersListResponse` Pydantic schema; `page == 2` and `data` is non-empty | Pass | Schema validated via Pydantic |
| 4.2 Create User (POST) | P2 | 1. Call `POST /api/users` with `{name, job}` | API Test | reqres.in + `x-api-key` | Returns `201 Created`; JSON includes auto-generated `id` and `createdAt` fields | Pass | - |
| 4.3 Login & Get Token (POST) | P1 | 1. Call `POST /api/login` with valid credentials | API Test | reqres.in + `x-api-key` | Returns `200 OK`; JSON includes a non-empty `token` field | Pass | API key is loaded from `.env` (not committed) |
| 4.4 Login with Missing Password (POST, Negative) | P2 | 1. Call `POST /api/login` with only `email`, no `password` | API Test | reqres.in + `x-api-key` | Returns `400 Bad Request`; JSON matches `ErrorResponse` schema with `error == "Missing password"` | Pass | Covers negative-path API coverage (all other Case 4 tests are happy-path only) |

---

## UX Improvement Recommendations

1. Items can only be added to cart one at a time (+1); there is no option to specify quantity before adding.
2. The cart displays a quantity field, but it is not editable.
3. Neither the cart page nor the checkout page displays an order subtotal / total.
4. The login page password field should include a show/hide toggle.
