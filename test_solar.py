"""
🌞 솔라테크 수익계산기 — 면적 입력 검증 테스트
==============================================
시나리오:
  홈페이지 → 수익계산기 → 면적 입력

  ✅ 숫자 입력 → 결과 화면 출력
  ❌ 문자 입력 → 경고창(dialog) 출력

실행:
  pytest test_solar.py -v -s
  pytest test_solar.py -v --headed --slowmo=1000
  pytest test_solar.py -v -n 2
"""

from playwright.sync_api import Page, expect

BASE_URL     = "https://solarteq.co.kr/ko"
VALID_AREA   = "1000"
INVALID_AREA = "abc"
TIMEOUT_MS   = 15000


# ══════════════════════════════════════════════════════════════════
# 공통 함수
# ══════════════════════════════════════════════════════════════════
def go_to_calculator_page(page: Page) -> None:
    """홈페이지 → 수익계산기 이동 + 입력창 준비 완료까지 대기"""
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
    page.get_by_role("link", name="수익계산기").click()

    # ⚡ 입력창이 화면에 나타날 때까지 기다린 후 진행
    #    이 줄 없으면 textbox가 없는 상태에서 fill 시도 → 입력 안 됨
    page.get_by_role("textbox").first.wait_for(state="visible", timeout=TIMEOUT_MS)


def fill_area_and_click(page: Page, value: str) -> None:
    """입력창에 값 넣고 계산하기 클릭"""
    textbox = page.get_by_role("textbox").first
    textbox.click()          # 포커스 먼저
    textbox.fill(value)      # 입력
    page.get_by_role("button", name="계산하기").first.click()


# ══════════════════════════════════════════════════════════════════
# ✅ 케이스 1: 숫자 입력 → 결과 화면 출력
# ══════════════════════════════════════════════════════════════════
def test_valid_number_shows_result(page: Page) -> None:
    """면적에 숫자(1000) 입력 → 발전용량·임대료 결과 확인"""
    go_to_calculator_page(page)
    fill_area_and_click(page, VALID_AREA)

    page.wait_for_selector("text=임대료", timeout=TIMEOUT_MS)

    expect(page.get_by_text("발전용량", exact=False).first).to_be_visible(timeout=TIMEOUT_MS)
    expect(page.get_by_text("임대료",   exact=False).first).to_be_visible(timeout=TIMEOUT_MS)
    expect(page.get_by_text("kW",       exact=False).first).to_be_visible(timeout=TIMEOUT_MS)

    print(f"\n✅ 숫자({VALID_AREA}) 입력 → 결과 정상 출력")


# ══════════════════════════════════════════════════════════════════
# ❌ 케이스 2: 문자 입력 → 경고창 출력
# ══════════════════════════════════════════════════════════════════
def test_invalid_text_shows_dialog(page: Page) -> None:
    """
    면적에 문자(abc) 입력 → 경고창 출력 확인

    ⚡ page.expect_event("dialog") 사용:
       이전 버전 playwright에서 expect_dialog()가 없어서
       expect_event("dialog")를 사용합니다.

       with 블록 안에서 클릭하면
       → dialog 뜨는 순간 즉시 캐치
       → dialog 안 뜨면 timeout → 테스트 자동 실패
    """
    go_to_calculator_page(page)

    # ⚡ dialog 이벤트 감지 — 뜨는 순간 즉시 캐치
    with page.expect_event("dialog", timeout=TIMEOUT_MS) as dialog_info:
        fill_area_and_click(page, INVALID_AREA)

    # dialog 내용 확인 후 닫기
    dialog = dialog_info.value
    print(f"\n  경고창 메시지: '{dialog.message}'")
    dialog.dismiss()

    # ✅ dialog 객체가 존재 = 경고창이 떴다는 증거
    assert dialog is not None, "경고창이 뜨지 않았습니다."

    print(f"❌→✅ 문자({INVALID_AREA}) 입력 → 경고창 정상 출력")