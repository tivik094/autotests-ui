# tests/test_courses.py

import pytest
from playwright.sync_api import expect

@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list(chromium_page_with_state):

    #Проверяем, что список курсов пуст.
    page = chromium_page_with_state
    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")

    # Проверяем заголовок Courses
    expect(page.get_by_role("heading", name="Courses")).to_be_visible(timeout=5000)

    # Проверка текста
    expect(page.get_by_text("There is no results")).to_be_visible(timeout=5000)

    print(")✅ Страница Courses открыта с сохранённым состоянием, заголовок и текст присутствуют.")
