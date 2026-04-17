import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://dot.apps-dotincorp.com/")
    page.get_by_role("dialog").click()
    page.get_by_role("button", name="다시보지 않기").click()
    page.get_by_role("button", name="로그인").click()
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("hhj")
    page.get_by_role("textbox", name="Username").press("Tab")
    page.get_by_role("textbox", name="Password").fill("guru133//")
    page.get_by_role("button", name="Login").click()
