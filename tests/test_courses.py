
import os
from playwright.sync_api import sync_playwright, expect

def test_empty_courses_list():
    state_file = "storage_state.json"

    # Чистим предыдущее состояние
    if os.path.exists(state_file):
        os.remove(state_file)

    with sync_playwright() as pw:
        # 1) Регистрация и сохранение state
        browser = pw.chromium.launch(
            headless=False,                 # при необходимости включите True для CI
            args=["--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Регистрация
        page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

        page.get_by_test_id("registration-form-email-input").locator("input").fill("user.name@gmail.com")
        page.get_by_test_id("registration-form-username-input").locator("input").fill("username")
        page.get_by_test_id("registration-form-password-input").locator("input").fill("password")
        page.get_by_test_id("registration-page-registration-button").click()

        # Проверяем, что попали на дашборд
        dashboard_heading = page.get_by_role("heading", name="Dashboard")
        expect(dashboard_heading).to_be_visible(timeout=5000)

        # Сохраняем состояние и закрываем первый контекст
        context.storage_state(path=state_file)
        context.close()

        # 2) Открываем страницу курсов с подставленным state
        context2 = browser.new_context(storage_state=state_file, no_viewport=True)
        page2 = context2.new_page()
        page2.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")

        # Базовые проверки
        courses_heading = page2.get_by_role("heading", name="Courses")
        expect(courses_heading).to_be_visible(timeout=5000)

        # Ключевая проверка теста: список пуст — видим заглушку
        no_results = page2.get_by_text("There is no results")
        expect(no_results).to_be_visible(timeout=5000)

        # Для дебага в -s режиме
        print("✅ Courses открыт со state, заголовок и текст заглушки присутствуют.")

        context2.close()
        browser.close()
