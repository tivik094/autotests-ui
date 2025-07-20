import time
import os
from playwright.sync_api import sync_playwright, expect

def run_registration():
    os.makedirs("screen", exist_ok=True)    # Создаём папку для скриншотов, если её нет
    start_time = time.perf_counter()    # Включаем замер времени

    with sync_playwright() as pw:
        # Запускаем браузер в окне, развернутом на весь экран
        browser = pw.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()


        page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")  # Открываем страницу регистрации

        # Заполняем форму
        page.get_by_test_id("registration-form-email-input").locator("input").fill("user.name@gmail.com")
        page.get_by_test_id("registration-form-username-input").locator("input").fill("username")
        page.get_by_test_id("registration-form-password-input").locator("input").fill("password")

        page.get_by_test_id("registration-page-registration-button").click()    # Нажимаем кнопку "Registration"

        # Ждем редиректа и проверяем заголовок дашборда
        dashboard_heading = page.get_by_role("heading", name="Dashboard")
        expect(dashboard_heading).to_be_visible(timeout=5000)

        # Делаем скриншот страницы Dashboard
        screenshot_path = os.path.join("screen", "dashboard.png")
        page.screenshot(path=screenshot_path, full_page=True)

        browser.close()

    # Выключаем замер времени
    end_time = time.perf_counter()
    duration = end_time - start_time

    # Выводим сообщения
    print(f"✅ Регистрация прошла успешно. "
          f"Время выполнения: {duration:.2f} сек. "
          f"Скриншот сохранён: {screenshot_path}")

if __name__ == "__main__":
    run_registration()
