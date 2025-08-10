
import os
import pytest
from playwright.sync_api import Page, Playwright, expect

BROWSER_STATE_FILE = "browser-state.json"


@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):

    # Регистрируем нового пользователя и сохраняем состояние браузера для повторного использования.
    if os.path.exists(BROWSER_STATE_FILE):
        os.remove(BROWSER_STATE_FILE)

    browser = playwright.chromium.launch(
        headless=False,  # для CI лучше True
        args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    # Заполняем форму регистрации
    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")
    page.get_by_test_id("registration-form-email-input").locator("input").fill("user.name@gmail.com")
    page.get_by_test_id("registration-form-username-input").locator("input").fill("username")
    page.get_by_test_id("registration-form-password-input").locator("input").fill("password")
    page.get_by_test_id("registration-page-registration-button").click()

    # Проверяем, что открылась страница Dashboard
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible(timeout=5000)

    # Сохраняем состояние браузера
    context.storage_state(path=BROWSER_STATE_FILE)

    context.close()
    browser.close()


@pytest.fixture(scope="function")
def chromium_page_with_state(initialize_browser_state, playwright: Playwright) -> Page:
    # Открываем авторизованную сессию
    browser = playwright.chromium.launch(
        headless=False,  # для CI лучше True
        args=["--start-maximized"]
    )
    context = browser.new_context(
        storage_state=BROWSER_STATE_FILE,
        no_viewport=True
    )
    page = context.new_page()

    yield page

    context.close()
    browser.close()
