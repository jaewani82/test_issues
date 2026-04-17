"""
솔라테크 수익계산기 E2E 테스트
==============================
홈페이지(https://solarteq.co.kr/ko) → 수익계산기 → 평수 입력 → 결과 검증

실행:
  pytest test_revenue_calculator.py -v -s
  pytest test_revenue_calculator.py -v --headed --slowmo=800
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://solarteq.co.kr/ko"
TIMEOUT  = 15_000


# ── 공통 헬퍼 ─────────────────────────────────────────────────────────────────

def open_calculator(page: Page) -> None:
    """수익계산기 링크 클릭 → 모달 입력창 노출까지 대기"""
    page.get_by_role("link", name="수익계산기").click()
    page.get_by_role("textbox").first.wait_for(state="visible", timeout=TIMEOUT)


def calculate(page: Page, value: str) -> None:
    """평수 입력 후 계산하기 클릭"""
    tb = page.get_by_role("textbox").first
    tb.click()
    tb.fill(value)
    page.get_by_role("button", name="계산하기").first.click()


def catch_dialog(page: Page) -> list[str]:
    """
    다이얼로그(alert) 자동 닫기 + 메시지 수집.
    calculate() 호출 전에 먼저 등록해야 한다.
    """
    messages: list[str] = []
    page.once("dialog", lambda d: (messages.append(d.message), d.accept()))
    return messages


# ── 픽스처 ───────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def goto_home(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)


# ═════════════════════════════════════════════════════════════════════════════
# ✅ 성공 케이스 (3개)
# ═════════════════════════════════════════════════════════════════════════════

def test_TC01_modal_opens(page: Page):
    """수익계산기 버튼 클릭 시 모달과 입력창이 노출돼야 한다"""
    open_calculator(page)

    expect(page.get_by_text("건물 지붕 임대 수익은").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_role("textbox").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_role("button", name="계산하기").first).to_be_visible(timeout=TIMEOUT)

    print("\n✅ TC01 PASS: 수익계산기 모달 정상 오픈")


def test_TC02_300pyeong_shows_result(page: Page):
    """300평 입력 → 발전용량·임대료·총 수익 항목이 노출돼야 한다"""
    open_calculator(page)
    calculate(page, "300")

    page.wait_for_selector("text=임대료", timeout=TIMEOUT)

    expect(page.get_by_text("발전용량", exact=False).first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("임대료",   exact=False).first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("kW",       exact=False).first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("20년 총 예상 수익", exact=False).first).to_be_visible(timeout=TIMEOUT)

    print("\n✅ TC02 PASS: 300평 → 수익 계산 결과 정상 출력")


def test_TC03_invalid_input_shows_dialog(page: Page):
    """빈 값 또는 문자 입력 시 경고 다이얼로그가 자동으로 처리돼야 한다"""
    open_calculator(page)

    # 다이얼로그 핸들러를 먼저 등록 → 뜨는 순간 자동으로 accept + 메시지 수집
    msgs = catch_dialog(page)
    calculate(page, "abc")

    page.wait_for_timeout(1_500)  # 다이얼로그 처리 대기

    assert len(msgs) > 0, "경고 다이얼로그가 출력되지 않았습니다."
    print(f"\n✅ TC03 PASS: 잘못된 입력 → 경고창 자동 처리 완료 (메시지: '{msgs[0]}')")


# ═════════════════════════════════════════════════════════════════════════════
# ❌ 실패 케이스 (3개) — 잘못된 기댓값으로 의도적 실패 확인
# ═════════════════════════════════════════════════════════════════════════════

def test_TC04_wrong_result_amount(page: Page):
    """
    [의도적 실패] 300평 결과가 '9999만원'이어야 한다고 주장
    → 실제 결과(822만원)와 달라 실패해야 정상
    """
    open_calculator(page)
    calculate(page, "300")

    page.wait_for_selector("text=임대료", timeout=TIMEOUT)

    # 실제 결과는 822만원 — 9999만원은 존재하지 않으므로 실패
    expect(page.get_by_text("9999만원", exact=False).first).to_be_visible(timeout=5_000)

    print("\n❌ TC04: 이 줄은 실행되지 않아야 합니다.")


def test_TC05_result_without_opening_modal(page: Page):
    """
    [의도적 실패] 수익계산기 모달을 열지 않고 결과 텍스트가 보여야 한다고 주장
    → 모달을 열지 않았으므로 결과가 없어 실패해야 정상
    """
    # open_calculator() 호출 없이 바로 결과 검증
    expect(page.get_by_text("발전용량", exact=False).first).to_be_visible(timeout=5_000)

    print("\n❌ TC05: 이 줄은 실행되지 않아야 합니다.")


def test_TC06_modal_close_wrong_selector(page: Page):
    """
    [의도적 실패] 존재하지 않는 선택자로 닫기 버튼을 찾으려 시도
    → 선택자가 없으므로 실패해야 정상
    """
    open_calculator(page)

    # 존재하지 않는 클래스명으로 닫기 버튼 탐색 → 타임아웃으로 실패
    expect(page.locator(".this-close-button-does-not-exist")).to_be_visible(timeout=5_000)

    print("\n❌ TC06: 이 줄은 실행되지 않아야 합니다.")
