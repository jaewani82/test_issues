from playwright.sync_api import Page, expect


def test_inquiry_fill_only(page: Page) -> None:
    page.goto("https://solarteq.co.kr/ko")

    page.get_by_role("banner").get_by_role("link", name="문의하기").click()

    modal = page.locator("#inquiry-modal")
    expect(modal).to_be_visible()

    modal.get_by_text("RE100 리스").click()

    # 입력
    page.locator("#inquire_company").fill("테스트테스트")
    page.locator("#inquire_hp").fill("01012341234")
    page.locator("#inquire_address").fill("세지로 35")
    page.locator("#inquire_contents").fill("테스트중입니다")

    # ✅ 핵심: 입력값 검증 (테스트 종료 조건)
    expect(page.locator("#inquire_company")).to_have_value("테스트테스트")
    expect(page.locator("#inquire_hp")).to_have_value("01012341234")
    expect(page.locator("#inquire_address")).to_have_value("세지로 35")
    expect(page.locator("#inquire_contents")).to_have_value("테스트중입니다")