
import os
from playwright.sync_api import sync_playwright, expect

def test_empty_courses_list():
    state_file = "storage_state.json"
    if os.path.exists(state_file):
        os.remove(state_file)

    with sync_playwright() as pw:
        # Запускаем браузер в окне, развернутом на весь экран
        browser = pw.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Заполняем форму на странице регистрации
        page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

        page.get_by_test_id("registration-form-email-input").locator("input").fill("user.name@gmail.com")
        page.get_by_test_id("registration-form-username-input").locator("input").fill("username")
        page.get_by_test_id("registration-form-password-input").locator("input").fill("password")

        page.get_by_test_id("registration-page-registration-button").click()

        # Ждем редиректа и проверяем заголовок дашборда
        dashboard_heading = page.get_by_role("heading", name="Dashboard")
        expect(dashboard_heading).to_be_visible(timeout=5000)

        # Сохраняем состояние
        context.storage_state(path=state_file)
        context.close()

        # Подставляем сохраненное состояние
        context2 = browser.new_context(
            storage_state=state_file,
            no_viewport=True
        )
        page2 = context2.new_page()

        # Авторизация и проверка заголовка
        page2.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")

        courses_heading = page2.get_by_role("heading", name="Courses")
        expect(courses_heading).to_be_visible(timeout=5000)

        no_results = page2.get_by_text("There is no results") # Проверка текста
        expect(no_results).to_be_visible(timeout=5000)

        print("✅ Страница Courses открыта с сохранённым состоянием, заголовок и текст присутствуют.")

        browser.close()
