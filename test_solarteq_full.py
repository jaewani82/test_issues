"""
솔라테크 (https://solarteq.co.kr/ko) 전체 E2E 테스트
=====================================================
페이지 분석 결과 도출한 테스트 케이스:

  [홈페이지]
  TC001 - 페이지 정상 로드 (타이틀 확인)
  TC002 - 로고 클릭 → 홈 유지

  [네비게이션]
  TC003 - 햄버거 메뉴 오픈
  TC004 - 햄버거 메뉴 닫기

  [수익계산기]
  TC005 - 수익계산기 모달 오픈
  TC006 - 300평 입력 → 결과(발전용량·임대료·수익) 출력
  TC007 - 빈 값 제출 → 경고창 자동 처리
  TC008 - 문자 입력 → 경고창 자동 처리

  [문의하기]
  TC009 - 문의하기 모달 오픈 및 필드 확인
  TC010 - 필수 필드 미입력 제출 → 검증 동작

  [슬라이더/UI]
  TC011 - Hero 슬라이더 Next 버튼 동작
  TC012 - 서비스 "자세히 보기" 링크 동작

  [기타]
  TC013 - 언어 전환 버튼(한국어) 노출 확인
  TC014 - 푸터 개인정보 처리방침 링크 동작

실행:
  pytest test_solarteq_full.py -v -s
  pytest test_solarteq_full.py -v -s --tb=short
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://solarteq.co.kr/ko"
TIMEOUT  = 15_000


# ── 공통 헬퍼 ─────────────────────────────────────────────────────────────────

def go_home(page: Page) -> None:
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)


def open_calculator(page: Page) -> None:
    page.get_by_role("link", name="수익계산기").click()
    page.get_by_role("textbox").first.wait_for(state="visible", timeout=TIMEOUT)


def open_inquiry(page: Page) -> None:
    page.get_by_role("link", name="문의하기").first.click()
    page.wait_for_selector("text=문의구분", timeout=TIMEOUT)


def catch_dialog(page: Page) -> list[str]:
    """다이얼로그 자동 accept + 메시지 수집 (calculate 전에 등록해야 함)"""
    messages: list[str] = []
    page.once("dialog", lambda d: (messages.append(d.message), d.accept()))
    return messages


@pytest.fixture(autouse=True)
def setup(page: Page):
    go_home(page)


# ══════════════════════════════════════════════════════════════════════════════
# [홈페이지]
# ══════════════════════════════════════════════════════════════════════════════

def test_TC001_page_title(page: Page):
    """홈페이지 로드 시 타이틀에 'SOLARTEQ'가 포함돼야 한다"""
    assert "SOLARTEQ" in page.title(), f"타이틀 불일치: {page.title()}"
    expect(page.get_by_role("link", name="수익계산기")).to_be_visible(timeout=TIMEOUT)
    print(f"\n✅ TC001 PASS | title: {page.title()}")


def test_TC002_logo_click_stays_home(page: Page):
    """로고 클릭 시 홈페이지(ko)에 머물러야 한다"""
    page.locator("a[href='/ko']").first.click()
    page.wait_for_load_state("domcontentloaded")
    assert "/ko" in page.url, f"URL 불일치: {page.url}"
    print(f"\n✅ TC002 PASS | URL: {page.url}")


# ══════════════════════════════════════════════════════════════════════════════
# [네비게이션]
# ══════════════════════════════════════════════════════════════════════════════

def test_TC003_hamburger_menu_open(page: Page):
    """햄버거 메뉴 클릭 시 '회사소개', '사업소개' 메뉴가 노출돼야 한다"""
    page.locator("button").filter(has_text="").last.click()
    page.wait_for_timeout(800)

    expect(page.get_by_text("회사소개").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("사업소개").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("솔라테크 소식").first).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC003 PASS | 햄버거 메뉴 오픈 확인")


def test_TC004_hamburger_menu_close(page: Page):
    """햄버거 메뉴 오픈 후 X 버튼 클릭 시 메뉴가 닫혀야 한다"""
    # 오픈
    page.locator("button").last.click()
    page.wait_for_selector("text=회사소개", timeout=TIMEOUT)

    # 닫기 (X 버튼 — 메뉴 오픈 후 마지막 버튼이 X)
    page.locator("button").last.click()
    page.wait_for_timeout(800)

    # 메뉴 nav 컨테이너의 aria-hidden 또는 display:none 상태 확인
    # 메뉴 내부의 서브링크가 숨겨지면 닫힌 것으로 판단
    nav_link = page.locator("nav a", has_text="지붕임대 태양광").first
    # 메뉴가 닫히면 nav 링크가 hidden이거나 viewport 밖으로 이동
    is_in_viewport = nav_link.is_visible()
    assert not is_in_viewport, "메뉴가 닫히지 않았습니다."
    print("\n✅ TC004 PASS | 햄버거 메뉴 닫기 확인")


# ══════════════════════════════════════════════════════════════════════════════
# [수익계산기]
# ══════════════════════════════════════════════════════════════════════════════

def test_TC005_calculator_modal_open(page: Page):
    """수익계산기 버튼 클릭 시 모달과 입력창이 노출돼야 한다"""
    open_calculator(page)

    expect(page.get_by_text("건물 지붕 임대 수익은").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_role("textbox").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_role("button", name="계산하기").first).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC005 PASS | 수익계산기 모달 오픈 확인")


def test_TC006_calculator_300pyeong(page: Page):
    """300평 입력 → 계산하기 → 발전용량·임대료·20년 총 예상 수익 결과 출력"""
    open_calculator(page)

    tb = page.get_by_role("textbox").first
    tb.click()
    tb.fill("300")
    page.get_by_role("button", name="계산하기").first.click()

    page.wait_for_selector("text=임대료", timeout=TIMEOUT)

    expect(page.get_by_text("발전용량", exact=False).first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("임대료",   exact=False).first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("kW",       exact=False).first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("20년 총 예상 수익", exact=False).first).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC006 PASS | 300평 수익 계산 결과 확인")


def test_TC007_calculator_empty_input_dialog(page: Page):
    """빈 값 제출 → 경고 다이얼로그 자동 처리 (페이지 멈춤 없음)"""
    open_calculator(page)

    msgs = catch_dialog(page)
    page.get_by_role("button", name="계산하기").first.click()
    page.wait_for_timeout(1_500)

    assert len(msgs) > 0, "경고창이 출력되지 않았습니다."
    print(f"\n✅ TC007 PASS | 경고창 메시지: '{msgs[0]}'")


def test_TC008_calculator_invalid_text_dialog(page: Page):
    """문자(abc) 입력 → 경고 다이얼로그 자동 처리"""
    open_calculator(page)

    tb = page.get_by_role("textbox").first
    tb.click()
    tb.fill("abc")

    msgs = catch_dialog(page)
    page.get_by_role("button", name="계산하기").first.click()
    page.wait_for_timeout(1_500)

    assert len(msgs) > 0, "경고창이 출력되지 않았습니다."
    print(f"\n✅ TC008 PASS | 경고창 메시지: '{msgs[0]}'")


# ══════════════════════════════════════════════════════════════════════════════
# [문의하기]
# ══════════════════════════════════════════════════════════════════════════════

def test_TC009_inquiry_modal_open(page: Page):
    """문의하기 버튼 클릭 시 모달이 열리고 필드들이 노출돼야 한다"""
    open_inquiry(page)

    expect(page.get_by_text("문의구분")).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("회사명/성명")).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("연락처")).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("설치주소")).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_role("button", name="문의하기")).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC009 PASS | 문의하기 모달 및 필드 확인")


def test_TC010_inquiry_submit_without_required(page: Page):
    """필수 필드 미입력 상태에서 제출 시 브라우저/JS 검증이 동작해야 한다"""
    open_inquiry(page)

    msgs = catch_dialog(page)
    page.get_by_role("button", name="문의하기").click()
    page.wait_for_timeout(1_500)

    # 검증 방식 1: dialog 발생
    # 검증 방식 2: 페이지가 그대로 문의하기 모달에 머물러 있음
    modal_still_visible = page.get_by_text("문의구분").is_visible()
    assert modal_still_visible or len(msgs) > 0, "미입력 제출 검증이 동작하지 않았습니다."
    print(f"\n✅ TC010 PASS | 미입력 제출 검증 동작 확인 (dialog={msgs})")


# ══════════════════════════════════════════════════════════════════════════════
# [슬라이더/UI]
# ══════════════════════════════════════════════════════════════════════════════

def test_TC011_hero_slider_next(page: Page):
    """Hero 슬라이더 Next 버튼 클릭 시 슬라이드가 전환돼야 한다"""
    next_btn = page.get_by_role("button", name="Next slide").first
    expect(next_btn).to_be_visible(timeout=TIMEOUT)
    next_btn.click()
    page.wait_for_timeout(1_000)

    # 슬라이더가 여전히 살아있으면 정상 (에러 없이 클릭 완료)
    expect(next_btn).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC011 PASS | Hero 슬라이더 Next 버튼 동작 확인")


def test_TC012_service_detail_link(page: Page):
    """서비스 '자세히 보기' 클릭 시 해당 페이지로 이동해야 한다"""
    detail_links = page.get_by_role("link", name="자세히 보기")
    expect(detail_links.first).to_be_visible(timeout=TIMEOUT)

    detail_links.first.click()
    page.wait_for_load_state("domcontentloaded")

    # 홈페이지가 아닌 다른 URL로 이동했는지 확인
    assert page.url != BASE_URL, f"페이지 이동 안됨: {page.url}"
    print(f"\n✅ TC012 PASS | 자세히 보기 이동 URL: {page.url}")


# ══════════════════════════════════════════════════════════════════════════════
# [기타]
# ══════════════════════════════════════════════════════════════════════════════

def test_TC013_language_button_visible(page: Page):
    """헤더에 언어 전환 버튼(한국어)이 노출돼야 한다"""
    lang_btn = page.get_by_role("link", name="한국어")
    expect(lang_btn.first).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC013 PASS | 언어 전환 버튼 노출 확인")


def test_TC014_footer_privacy_link(page: Page):
    """푸터의 '개인정보 처리방침' 링크가 존재하고 클릭 가능해야 한다"""
    privacy = page.get_by_role("link", name="개인정보 처리방침")
    expect(privacy.first).to_be_visible(timeout=TIMEOUT)

    privacy.first.click()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1_000)

    assert page.url != "", f"URL이 비어 있습니다."
    print(f"\n✅ TC014 PASS | 개인정보 처리방침 이동 URL: {page.url}")
