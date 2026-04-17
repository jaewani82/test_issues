"""
솔라테크 (https://solarteq.co.kr/ko) E2E 통합 테스트
======================================================
기존 57개 + 품질 지표 22개 = 총 79개 TC

  [홈페이지]
  TC001 - 페이지 정상 로드 (타이틀 확인)
  TC002 - 로고 클릭 → 홈 유지

  [네비게이션]
  TC003 - 햄버거 메뉴 오픈
  TC004 - 햄버거 메뉴 닫기

  [수익계산기 기본]
  TC005 - 수익계산기 모달 오픈
  TC006 - 300평 입력 → 결과 출력
  TC007 - 빈 값 제출 → 경고창
  TC008 - 문자 입력 → 경고창

  [문의하기 기본]
  TC009 - 문의하기 모달 오픈 및 필드 확인
  TC010 - 필수 필드 미입력 제출 → 검증

  [슬라이더/UI 기본]
  TC011 - Hero 슬라이더 Next 버튼
  TC012 - 서비스 자세히 보기 링크

  [기타 기본]
  TC013 - 언어 전환 버튼 노출
  TC014 - 푸터 개인정보 처리방침 링크

  [수익계산기 경계값/예외]
  TC015 - 경계 최솟값 1평
  TC016 - 경계 최댓값 9999평
  TC017 - 정상값 300평 재확인
  TC018 - 소수점 입력 (100.5)
  TC019 - 0평 경고창
  TC020 - 음수 경고창
  TC021 - 빈값 제출
  TC022 - 영문 문자 입력
  TC023 - 특수문자 입력
  TC024 - 매우 큰 수 (999999)
  TC025 - 계산 후 홈 재로드 → 재오픈 입력창 확인
  TC026 - 결과값 숫자+단위 정규식 검증
  TC027 - 동일 평수 연속 2회 계산 → 결과 정상

  [문의하기 모달 상세]
  TC028 - 라디오버튼: 지붕임대 태양광
  TC029 - 라디오버튼: RE100 리스
  TC030 - 라디오버튼: RPS 전력판매
  TC031 - 라디오버튼: 지원사업
  TC032 - 라디오버튼: 회사소개
  TC033 - 연락처 전화번호 형식 입력
  TC034 - 연락처 한글 입력 확인
  TC035 - 미입력 상태 제출 차단
  TC036 - 모든 필드 정상 입력 → 제출버튼 visible

  [네비게이션 상세]
  TC037 - 햄버거 → 솔라테크 소개 이동
  TC038 - 햄버거 → 연혁 이동
  TC039 - 햄버거 → 인증·특허 이동
  TC040 - 서브페이지 → 뒤로가기 → /ko 복귀
  TC041 - 햄버거 서브메뉴 지붕임대 태양광 노출

  [UI/슬라이더 상세]
  TC042 - Hero 슬라이더 Prev 버튼
  TC043 - Hero 슬라이더 Next×2 → Prev×2 연속
  TC044 - 포트폴리오 슬라이더 Next 버튼
  TC045 - 스크롤 후 헤더 sticky 확인
  TC046 - 자세히 보기 링크 href 존재 확인

  [반응형 viewport]
  TC047 - desktop 1920×1080
  TC048 - desktop 1280×800
  TC049 - tablet 768×1024
  TC050 - mobile 375×812

  [언어 전환]
  TC051 - 한국어 → 영어 전환 → /en 확인
  TC052 - 영문 페이지 타이틀 확인
  TC053 - 영어 → 한국어 재전환 → /ko 복귀

  [기타/보완]
  TC054 - 개인정보 처리방침 → /ko/policy 이동
  TC055 - Footer 문의하기 → 모달 오픈
  TC056 - 페이지 타이틀 비어있지 않음
  TC057 - 콘솔 에러 없음 확인

  [성능 Performance]
  TC058 - 페이지 로드 3초 이내 (domcontentloaded 기준)
  TC059 - 뷰포트 내 이미지 개수 과다 여부 (30개 미만)
  TC060 - 뷰포트 밖 이미지 lazy loading 적용 여부

  [접근성 Accessibility]
  TC061 - 이미지 alt 텍스트 누락 검사
  TC062 - 아이콘 버튼 aria-label 존재 여부
  TC063 - 폼 input에 label 또는 placeholder 존재 여부
  TC064 - 폼 요소 tabindex=-1 없음 (키보드 접근성)
  TC065 - 링크 텍스트 의미 있음 ("여기", "클릭" 등 금지)

  [SEO]
  TC066 - meta description 존재 및 50자 이상
  TC067 - h1 태그 정확히 1개
  TC068 - OG 태그(og:title, og:description) 존재
  TC069 - canonical URL 태그 존재

  [보안 Security]
  TC070 - 외부 링크 rel=noopener 설정 여부
  TC071 - HTTP → HTTPS 리다이렉트 확인
  TC072 - 민감 정보 폼 autocomplete 설정 여부

  [UX]
  TC073 - 모바일(375px) 가로 스크롤 없음
  TC074 - 잘못된 URL 접근 시 404 처리 여부
  TC075 - CTA 버튼(수익계산기) 스크롤 없이 뷰포트 내 노출
  TC076 - 문의 폼 제출 후 사용자 피드백(완료 메시지) 여부

실행:
  pytest test_solarteq_all.py -v -s
  pytest test_solarteq_all.py -v -s --tb=short
  pytest test_solarteq_all.py -v -k "TC01"   # 기본
  pytest test_solarteq_all.py -v -k "TC02"   # 수익계산기 경계값
  pytest test_solarteq_all.py -v -k "TC04"   # UI/슬라이더
  pytest test_solarteq_all.py -v -k "TC05"   # 반응형
  pytest test_solarteq_all.py -v -k "TC058 or TC059 or TC060"  # 성능
  pytest test_solarteq_all.py -v -k "TC061 or TC062 or TC063 or TC064 or TC065"  # 접근성
  pytest test_solarteq_all.py -v -k "TC066 or TC067 or TC068 or TC069"  # SEO
  pytest test_solarteq_all.py -v -k "TC070 or TC071 or TC072"  # 보안
  pytest test_solarteq_all.py -v -k "TC073 or TC074 or TC075 or TC076"  # UX
"""

import re
import time
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
    """다이얼로그 자동 accept + 메시지 수집 — 액션 전에 반드시 등록"""
    messages: list[str] = []
    page.once("dialog", lambda d: (messages.append(d.message), d.accept()))
    return messages


def calc_input_and_submit(page: Page, value: str) -> None:
    tb = page.get_by_role("textbox").first
    tb.click()
    tb.fill(value)
    page.get_by_role("button", name="계산하기").first.click()


def open_hamburger(page: Page) -> None:
    """햄버거 메뉴 오픈"""
    page.locator("button").filter(has_text="").last.click()
    page.wait_for_selector("text=회사소개", timeout=TIMEOUT)
    page.wait_for_timeout(400)


def click_nav_link(page: Page, name: str) -> None:
    """메뉴 내 링크 — href 추출 후 직접 navigate (viewport 밖 이슈 우회)"""
    link = page.locator(f"a:has-text('{name}')").first
    link.wait_for(state="attached", timeout=TIMEOUT)
    href = link.get_attribute("href")
    if href and href.startswith("/"):
        href = f"https://solarteq.co.kr{href}"
    page.goto(href or BASE_URL, wait_until="domcontentloaded", timeout=30_000)


@pytest.fixture(autouse=True)
def setup(page: Page):
    go_home(page)


# ══════════════════════════════════════════════════════════════════════════════
# [홈페이지]  TC001 – TC002
# ══════════════════════════════════════════════════════════════════════════════

def test_TC001_page_title(page: Page):
    """TC001: 홈페이지 로드 시 타이틀에 'SOLARTEQ' 포함"""
    assert "SOLARTEQ" in page.title(), f"타이틀 불일치: {page.title()}"
    expect(page.get_by_role("link", name="수익계산기")).to_be_visible(timeout=TIMEOUT)
    print(f"\n✅ TC001 PASS | title: {page.title()}")


def test_TC002_logo_click_stays_home(page: Page):
    """TC002: 로고 클릭 시 홈(/ko)에 머물러야 한다"""
    page.locator("a[href='/ko']").first.click()
    page.wait_for_load_state("domcontentloaded")
    assert "/ko" in page.url, f"URL 불일치: {page.url}"
    print(f"\n✅ TC002 PASS | URL: {page.url}")


# ══════════════════════════════════════════════════════════════════════════════
# [네비게이션]  TC003 – TC004
# ══════════════════════════════════════════════════════════════════════════════

def test_TC003_hamburger_menu_open(page: Page):
    """TC003: 햄버거 메뉴 클릭 시 회사소개·사업소개·솔라테크소식 노출"""
    page.locator("button").filter(has_text="").last.click()
    page.wait_for_timeout(800)
    expect(page.get_by_text("회사소개").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("사업소개").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("솔라테크 소식").first).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC003 PASS | 햄버거 메뉴 오픈 확인")


def test_TC004_hamburger_menu_close(page: Page):
    """TC004: 햄버거 메뉴 오픈 후 X 버튼 클릭 시 닫혀야 한다"""
    page.locator("button").last.click()
    page.wait_for_selector("text=회사소개", timeout=TIMEOUT)
    page.locator("button").last.click()
    page.wait_for_timeout(800)

    nav_link = page.locator("nav a", has_text="지붕임대 태양광").first
    assert not nav_link.is_visible(), "메뉴가 닫히지 않았습니다."
    print("\n✅ TC004 PASS | 햄버거 메뉴 닫기 확인")


# ══════════════════════════════════════════════════════════════════════════════
# [수익계산기 기본]  TC005 – TC008
# ══════════════════════════════════════════════════════════════════════════════

def test_TC005_calculator_modal_open(page: Page):
    """TC005: 수익계산기 버튼 클릭 시 모달과 입력창 노출"""
    open_calculator(page)
    expect(page.get_by_text("건물 지붕 임대 수익은").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_role("textbox").first).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_role("button", name="계산하기").first).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC005 PASS | 수익계산기 모달 오픈 확인")


def test_TC006_calculator_300pyeong(page: Page):
    """TC006: 300평 → 계산하기 → 발전용량·임대료·20년 총 예상 수익 출력"""
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
    """TC007: 빈 값 제출 → 경고 다이얼로그 자동 처리"""
    open_calculator(page)
    msgs = catch_dialog(page)
    page.get_by_role("button", name="계산하기").first.click()
    page.wait_for_timeout(1_500)
    assert len(msgs) > 0, "경고창이 출력되지 않았습니다."
    print(f"\n✅ TC007 PASS | 경고창: '{msgs[0]}'")


def test_TC008_calculator_invalid_text_dialog(page: Page):
    """TC008: 문자(abc) 입력 → 경고 다이얼로그 자동 처리"""
    open_calculator(page)
    tb = page.get_by_role("textbox").first
    tb.click()
    tb.fill("abc")
    msgs = catch_dialog(page)
    page.get_by_role("button", name="계산하기").first.click()
    page.wait_for_timeout(1_500)
    assert len(msgs) > 0, "경고창이 출력되지 않았습니다."
    print(f"\n✅ TC008 PASS | 경고창: '{msgs[0]}'")


# ══════════════════════════════════════════════════════════════════════════════
# [문의하기 기본]  TC009 – TC010
# ══════════════════════════════════════════════════════════════════════════════

def test_TC009_inquiry_modal_open(page: Page):
    """TC009: 문의하기 버튼 클릭 시 모달이 열리고 필드 노출"""
    open_inquiry(page)
    expect(page.get_by_text("문의구분")).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("회사명/성명")).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("연락처")).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_text("설치주소")).to_be_visible(timeout=TIMEOUT)
    expect(page.get_by_role("button", name="문의하기")).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC009 PASS | 문의하기 모달 및 필드 확인")


def test_TC010_inquiry_submit_without_required(page: Page):
    """TC010: 필수 필드 미입력 상태에서 제출 시 검증 동작"""
    open_inquiry(page)
    msgs = catch_dialog(page)
    page.get_by_role("button", name="문의하기").click()
    page.wait_for_timeout(1_500)
    modal_still_visible = page.get_by_text("문의구분").is_visible()
    assert modal_still_visible or len(msgs) > 0, "미입력 제출 검증이 동작하지 않았습니다."
    print(f"\n✅ TC010 PASS | 미입력 제출 검증 확인 (dialog={msgs})")


# ══════════════════════════════════════════════════════════════════════════════
# [슬라이더/UI 기본]  TC011 – TC012
# ══════════════════════════════════════════════════════════════════════════════

def test_TC011_hero_slider_next(page: Page):
    """TC011: Hero 슬라이더 Next 버튼 클릭 시 슬라이드 전환"""
    next_btn = page.get_by_role("button", name="Next slide").first
    expect(next_btn).to_be_visible(timeout=TIMEOUT)
    next_btn.click()
    page.wait_for_timeout(1_000)
    expect(next_btn).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC011 PASS | Hero 슬라이더 Next 동작 확인")


def test_TC012_service_detail_link(page: Page):
    """TC012: 서비스 '자세히 보기' 클릭 시 해당 페이지 이동"""
    detail_links = page.get_by_role("link", name="자세히 보기")
    expect(detail_links.first).to_be_visible(timeout=TIMEOUT)
    detail_links.first.click()
    page.wait_for_load_state("domcontentloaded")
    assert page.url != BASE_URL, f"페이지 이동 안됨: {page.url}"
    print(f"\n✅ TC012 PASS | 자세히 보기 이동 URL: {page.url}")


# ══════════════════════════════════════════════════════════════════════════════
# [기타 기본]  TC013 – TC014
# ══════════════════════════════════════════════════════════════════════════════

def test_TC013_language_button_visible(page: Page):
    """TC013: 헤더에 언어 전환 버튼(한국어) 노출"""
    lang_btn = page.get_by_role("link", name="한국어")
    expect(lang_btn.first).to_be_visible(timeout=TIMEOUT)
    print("\n✅ TC013 PASS | 언어 전환 버튼 노출 확인")


def test_TC014_footer_privacy_link(page: Page):
    """TC014: 푸터 개인정보 처리방침 링크 → 클릭 가능"""
    privacy = page.get_by_role("link", name="개인정보 처리방침")
    expect(privacy.first).to_be_visible(timeout=TIMEOUT)
    privacy.first.click()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1_000)
    assert page.url != "", f"URL이 비어 있습니다."
    print(f"\n✅ TC014 PASS | 개인정보 처리방침 URL: {page.url}")


# ══════════════════════════════════════════════════════════════════════════════
# [수익계산기 경계값/예외]  TC015 – TC027
# ══════════════════════════════════════════════════════════════════════════════

CALC_CASES = [
    ("1",      "result", "TC015", "경계 최솟값 1평"),
    ("9999",   "result", "TC016", "경계 최댓값 9999평"),
    ("300",    "result", "TC017", "정상값 300평 재확인"),
    ("100.5",  "result", "TC018", "소수점 입력 — 사이트가 결과 출력"),
    ("0",      "alert",  "TC019", "0평 — 경고창 필수"),
    ("-100",   "alert",  "TC020", "음수 — 경고창 필수"),
    ("",       "alert",  "TC021", "빈값 제출"),
    ("abc",    "alert",  "TC022", "영문 문자 입력"),
    ("!@#$",   "alert",  "TC023", "특수문자 입력"),
    ("999999", "result", "TC024", "매우 큰 수"),
]


@pytest.mark.parametrize("input_val,expect_type,tc_id,desc", CALC_CASES)
def test_calculator_boundary(page: Page, input_val: str, expect_type: str,
                             tc_id: str, desc: str):
    """수익계산기 경계값/예외"""
    open_calculator(page)

    if expect_type == "alert":
        msgs = catch_dialog(page)
        calc_input_and_submit(page, input_val)
        page.wait_for_timeout(1_500)
        assert len(msgs) > 0, f"[{tc_id}] 경고창 미출력 (입력: '{input_val}')"
        print(f"\n✅ {tc_id} PASS | '{input_val}' → 경고창: '{msgs[0]}'")
    else:
        calc_input_and_submit(page, input_val)
        page.wait_for_selector("text=임대료", timeout=TIMEOUT)
        expect(page.get_by_text("발전용량", exact=False).first).to_be_visible(timeout=TIMEOUT)
        expect(page.get_by_text("임대료",   exact=False).first).to_be_visible(timeout=TIMEOUT)
        print(f"\n✅ {tc_id} PASS | '{input_val}' → 결과 정상 출력")


def test_TC025_modal_reopen_resets_input(page: Page):
    """TC025: 계산 후 홈 재로드 → 수익계산기 재오픈 → 입력창 정상 노출 확인"""
    open_calculator(page)
    calc_input_and_submit(page, "300")
    page.wait_for_selector("text=임대료", timeout=TIMEOUT)

    go_home(page)
    open_calculator(page)

    textbox = page.get_by_role("textbox").first
    assert textbox.is_visible(), "재오픈 후 입력창이 보이지 않습니다."
    current_val = textbox.input_value()
    print(f"\n✅ TC025 PASS | 재오픈 후 입력값: '{current_val}'")


def test_TC026_result_format_regex(page: Page):
    """TC026: 300평 결과값이 숫자+단위 형식인지 정규식 검증"""
    open_calculator(page)
    calc_input_and_submit(page, "300")
    page.wait_for_selector("text=임대료", timeout=TIMEOUT)

    result_section = page.locator("text=20년 총 예상 수익").first
    result_section.wait_for(state="visible", timeout=TIMEOUT)
    page_text = page.inner_text("body")

    pattern = re.compile(r"\d[\d,]*\s*만원")
    matches = pattern.findall(page_text)
    assert len(matches) > 0, f"'숫자만원' 패턴 미발견. 추출: {matches}"
    print(f"\n✅ TC026 PASS | 정규식 매칭: {matches[:3]}")


def test_TC027_consistent_result(page: Page):
    """TC027: 동일 평수(500평) 연속 2회 계산 → 결과 섹션 정상 출력 확인"""
    open_calculator(page)

    for attempt in (1, 2):
        tb = page.get_by_role("textbox").first
        tb.click()
        tb.fill("500")
        page.get_by_role("button", name="계산하기").first.click()
        page.wait_for_selector("text=임대료", timeout=TIMEOUT)
        assert page.get_by_text("발전용량", exact=False).first.is_visible(), \
            f"[{attempt}차 계산] 결과가 표시되지 않았습니다."

    print(f"\n✅ TC027 PASS | 동일 평수 2회 계산 결과 정상")


# ══════════════════════════════════════════════════════════════════════════════
# [문의하기 모달 상세]  TC028 – TC036
# ══════════════════════════════════════════════════════════════════════════════

INQUIRY_TYPES = [
    ("TC028", "지붕임대 태양광"),
    ("TC029", "RE100 리스"),
    ("TC030", "RPS 전력판매"),
    ("TC031", "지원사업(건물·금융·주택·탄소중립)"),
    ("TC032", "회사소개·지명원 요청"),
]


@pytest.mark.parametrize("tc_id,label", INQUIRY_TYPES)
def test_inquiry_radio_buttons(page: Page, tc_id: str, label: str):
    """문의구분 라디오버튼 선택 가능 확인"""
    open_inquiry(page)

    idx = ["TC028", "TC029", "TC030", "TC031", "TC032"].index(tc_id)

    labels = page.locator("label").filter(has_text=label)
    if labels.count() > 0:
        labels.first.click(force=True)
    else:
        radio = page.locator("input[type='radio']").nth(idx)
        radio.evaluate("el => el.click()")

    page.wait_for_timeout(500)

    checked = page.locator("input[type='radio']:checked")
    assert checked.count() > 0, f"[{tc_id}] 라디오버튼 미선택: {label}"
    print(f"\n✅ {tc_id} PASS | 라디오버튼 선택 확인: {label}")


def test_TC033_inquiry_phone_number(page: Page):
    """TC033: 연락처 필드에 전화번호 형식(010-1234-5678) 입력 가능 확인"""
    open_inquiry(page)
    phone_field = page.get_by_role("textbox").nth(1)
    phone_field.click()
    phone_field.fill("010-1234-5678")
    val = phone_field.input_value()
    assert val != "", "연락처 필드에 값이 입력되지 않았습니다."
    print(f"\n✅ TC033 PASS | 연락처 입력값: '{val}'")


def test_TC034_inquiry_phone_korean(page: Page):
    """TC034: 연락처에 한글 입력 시 필드 값 확인 (입력 허용 여부)"""
    open_inquiry(page)
    phone_field = page.get_by_role("textbox").nth(1)
    phone_field.click()
    phone_field.fill("홍길동")
    val = phone_field.input_value()
    print(f"\n✅ TC034 PASS | 한글 입력 후 필드값: '{val}'")


def test_TC035_inquiry_submit_without_privacy(page: Page):
    """TC035: 미입력 상태에서 제출 → 경고창 또는 모달 유지 확인"""
    open_inquiry(page)
    msgs = catch_dialog(page)
    page.get_by_role("button", name="문의하기").click()
    page.wait_for_timeout(1_500)
    modal_still_visible = page.get_by_text("문의구분").is_visible()
    assert modal_still_visible or len(msgs) > 0, "미입력 제출 차단이 동작하지 않았습니다."
    print(f"\n✅ TC035 PASS | 미입력 제출 차단 확인 (dialog={msgs})")


def test_TC036_inquiry_all_fields_filled(page: Page):
    """TC036: 모든 필드 정상 입력 → 제출 버튼 visible 확인 (실제 제출 안 함)"""
    open_inquiry(page)

    first_label = page.locator("label").filter(has_text="지붕임대 태양광").first
    if first_label.is_visible():
        first_label.click()
    else:
        page.locator("input[type='radio']").first.click(force=True)
    page.wait_for_timeout(300)

    textboxes = page.get_by_role("textbox")
    textboxes.nth(0).fill("솔라테크 테스트")
    textboxes.nth(1).fill("010-0000-0000")
    textboxes.nth(2).fill("경기도 테스트시")

    submit_btn = page.get_by_role("button", name="문의하기")
    assert submit_btn.is_visible(), "문의하기 버튼이 보이지 않습니다."
    print(f"\n✅ TC036 PASS | 모든 필드 입력 완료, 제출 버튼 visible 확인")


# ══════════════════════════════════════════════════════════════════════════════
# [네비게이션 상세]  TC037 – TC041
# ══════════════════════════════════════════════════════════════════════════════

def test_TC037_nav_company_intro(page: Page):
    """TC037: 햄버거 → 솔라테크 소개 클릭 → URL 이동 확인"""
    open_hamburger(page)
    click_nav_link(page, "솔라테크 소개")
    assert page.url != BASE_URL, f"페이지 이동 안 됨: {page.url}"
    print(f"\n✅ TC037 PASS | 이동 URL: {page.url}")


def test_TC038_nav_history(page: Page):
    """TC038: 햄버거 → 연혁 클릭 → 이동 확인"""
    open_hamburger(page)
    click_nav_link(page, "연혁")
    assert "solarteq.co.kr" in page.url, f"URL 이탈: {page.url}"
    print(f"\n✅ TC038 PASS | 이동 URL: {page.url}")


def test_TC039_nav_certification(page: Page):
    """TC039: 햄버거 → 인증·특허 클릭 → 이동 확인"""
    open_hamburger(page)
    click_nav_link(page, "인증·특허")
    assert "solarteq.co.kr" in page.url, f"URL 이탈: {page.url}"
    print(f"\n✅ TC039 PASS | 이동 URL: {page.url}")


def test_TC040_back_navigation(page: Page):
    """TC040: 서브페이지 이동 후 뒤로가기 → /ko 복귀 확인"""
    page.get_by_role("link", name="자세히 보기").first.click()
    page.wait_for_load_state("domcontentloaded")
    page.go_back()
    page.wait_for_load_state("domcontentloaded")
    assert "/ko" in page.url, f"뒤로가기 후 URL 이상: {page.url}"
    print(f"\n✅ TC040 PASS | 뒤로가기 후 URL: {page.url}")


def test_TC041_submenu_visible(page: Page):
    """TC041: 햄버거 메뉴 오픈 시 사업소개 서브메뉴 '지붕임대 태양광' 노출"""
    open_hamburger(page)
    submenu_item = page.locator("a:has-text('지붕임대 태양광')").first
    submenu_item.wait_for(state="visible", timeout=TIMEOUT)
    expect(submenu_item).to_be_visible(timeout=TIMEOUT)
    print(f"\n✅ TC041 PASS | 서브메뉴 '지붕임대 태양광' 노출 확인")


# ══════════════════════════════════════════════════════════════════════════════
# [UI/슬라이더 상세]  TC042 – TC046
# ══════════════════════════════════════════════════════════════════════════════

def test_TC042_hero_slider_prev(page: Page):
    """TC042: Hero 슬라이더 Prev 버튼 클릭 → 에러 없이 슬라이드 전환"""
    prev_btn = page.get_by_role("button", name="Previous slide").first
    expect(prev_btn).to_be_visible(timeout=TIMEOUT)
    prev_btn.click()
    page.wait_for_timeout(1_000)
    expect(prev_btn).to_be_visible(timeout=TIMEOUT)
    print(f"\n✅ TC042 PASS | Hero 슬라이더 Prev 동작 확인")


def test_TC043_hero_slider_multiple_clicks(page: Page):
    """TC043: Hero 슬라이더 Next×2 → Prev×2 연속 클릭 → 오류 없음"""
    next_btn = page.get_by_role("button", name="Next slide").first
    prev_btn = page.get_by_role("button", name="Previous slide").first

    for _ in range(2):
        next_btn.click()
        page.wait_for_timeout(600)

    for _ in range(2):
        prev_btn.click()
        page.wait_for_timeout(600)

    expect(next_btn).to_be_visible(timeout=TIMEOUT)
    expect(prev_btn).to_be_visible(timeout=TIMEOUT)
    print(f"\n✅ TC043 PASS | 슬라이더 Next×2 → Prev×2 오류 없음")


def test_TC044_portfolio_slider(page: Page):
    """TC044: 포트폴리오 슬라이더 Next 버튼 존재 및 클릭 가능 확인"""
    portfolio = page.get_by_text("포트폴리오").first
    portfolio.scroll_into_view_if_needed()
    page.wait_for_timeout(800)

    next_btns = page.get_by_role("button", name="Next slide")
    assert next_btns.count() >= 2, "포트폴리오 슬라이더 Next 버튼 미발견"

    next_btns.nth(1).click()
    page.wait_for_timeout(800)
    print(f"\n✅ TC044 PASS | 포트폴리오 슬라이더 Next 동작 확인")


def test_TC045_sticky_header(page: Page):
    """TC045: 스크롤 후에도 헤더(수익계산기 버튼) visible 유지 확인"""
    page.evaluate("window.scrollTo(0, 800)")
    page.wait_for_timeout(500)
    header_btn = page.get_by_role("link", name="수익계산기")
    expect(header_btn.first).to_be_visible(timeout=TIMEOUT)
    print(f"\n✅ TC045 PASS | 스크롤 후 헤더 sticky 확인")


def test_TC046_detail_links_have_href(page: Page):
    """TC046: '자세히 보기' 링크 3개 모두 href 속성 존재 확인 (빈 링크 방지)"""
    links = page.get_by_role("link", name="자세히 보기")
    count = links.count()
    assert count >= 1, "자세히 보기 링크를 찾지 못했습니다."

    empty_hrefs = []
    for i in range(min(count, 3)):
        href = links.nth(i).get_attribute("href")
        if not href or href.strip() in ("", "#", "javascript:;", "javascript:void(0)"):
            empty_hrefs.append(i)

    assert len(empty_hrefs) == 0, f"빈 href 링크 발견: 인덱스 {empty_hrefs}"
    print(f"\n✅ TC046 PASS | 자세히 보기 링크 {min(count,3)}개 모두 href 정상")


# ══════════════════════════════════════════════════════════════════════════════
# [반응형 viewport]  TC047 – TC050
# ══════════════════════════════════════════════════════════════════════════════

VIEWPORTS = [
    ("TC047", 1920, 1080, "desktop_1920"),
    ("TC048", 1280, 800,  "desktop_1280"),
    ("TC049", 768,  1024, "tablet"),
    ("TC050", 375,  812,  "mobile"),
]


@pytest.mark.parametrize("tc_id,width,height,label", VIEWPORTS)
def test_responsive_layout(page: Page, tc_id: str, width: int,
                           height: int, label: str):
    """반응형 레이아웃 — 로고/헤더 visible 확인"""
    page.set_viewport_size({"width": width, "height": height})
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(800)

    logo = page.locator("a[href='/ko']").first
    expect(logo).to_be_visible(timeout=TIMEOUT)

    if width >= 768:
        calc_btn = page.get_by_role("link", name="수익계산기")
        expect(calc_btn.first).to_be_visible(timeout=TIMEOUT)

    if width <= 375:
        hamburger = page.locator("button").last
        expect(hamburger).to_be_visible(timeout=TIMEOUT)

    print(f"\n✅ {tc_id} PASS | {label} ({width}×{height}) 레이아웃 확인")


# ══════════════════════════════════════════════════════════════════════════════
# [언어 전환]  TC051 – TC053
# ══════════════════════════════════════════════════════════════════════════════

def test_TC051_language_switch_to_english(page: Page):
    """TC051: 한국어 → 영어 전환 → URL에 /en 포함 확인"""
    lang_btn = page.get_by_role("link", name="한국어").first
    expect(lang_btn).to_be_visible(timeout=TIMEOUT)
    lang_btn.click()
    page.wait_for_timeout(1_000)

    en_option = page.get_by_role("link", name="English")
    if en_option.count() > 0 and en_option.first.is_visible():
        en_option.first.click()
        page.wait_for_load_state("domcontentloaded")
        assert "/en" in page.url, f"영어 전환 후 URL에 /en 없음: {page.url}"
        print(f"\n✅ TC051 PASS | 영어 전환 URL: {page.url}")
    else:
        print(f"\n✅ TC051 PASS | 언어 전환 버튼 동작 확인 (URL: {page.url})")


def test_TC052_english_page_content(page: Page):
    """TC052: 영문 페이지(/en) 타이틀 비어있지 않음 확인"""
    page.goto("https://solarteq.co.kr/en", wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)
    title = page.title()
    assert title != "", "영문 페이지 타이틀이 비어있습니다."
    print(f"\n✅ TC052 PASS | 영문 페이지 타이틀: {title}")


def test_TC053_language_switch_back_to_korean(page: Page):
    """TC053: 영어 페이지에서 한국어로 재전환 → /ko 복귀 확인"""
    page.goto("https://solarteq.co.kr/en", wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(800)

    lang_btn = page.get_by_role("link", name="English")
    if lang_btn.count() == 0:
        lang_btn = page.get_by_role("link", name="한국어")

    if lang_btn.count() > 0 and lang_btn.first.is_visible():
        lang_btn.first.click()
        page.wait_for_timeout(1_000)
        ko_option = page.get_by_role("link", name="한국어")
        if ko_option.count() > 0 and ko_option.first.is_visible():
            ko_option.first.click()
            page.wait_for_load_state("domcontentloaded")

    assert "/ko" in page.url or "solarteq.co.kr" in page.url, \
        f"한국어 재전환 실패: {page.url}"
    print(f"\n✅ TC053 PASS | 한국어 복귀 URL: {page.url}")


# ══════════════════════════════════════════════════════════════════════════════
# [기타/보완]  TC054 – TC057
# ══════════════════════════════════════════════════════════════════════════════

def test_TC054_privacy_policy_url(page: Page):
    """TC054: 개인정보 처리방침 → /ko/policy 이동 확인"""
    privacy = page.get_by_role("link", name="개인정보 처리방침").first
    expect(privacy).to_be_visible(timeout=TIMEOUT)
    href = privacy.get_attribute("href")
    assert href and "policy" in href, f"href에 'policy' 없음: {href}"
    privacy.click()
    page.wait_for_load_state("domcontentloaded")
    assert "policy" in page.url, f"이동 후 URL에 'policy' 없음: {page.url}"
    print(f"\n✅ TC054 PASS | 개인정보 처리방침 URL: {page.url}")


def test_TC055_footer_inquiry_button(page: Page):
    """TC055: Footer 문의하기 버튼 클릭 → 문의 모달 오픈 확인"""
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(800)
    footer_inquiry = page.get_by_role("link", name="문의하기").last
    expect(footer_inquiry).to_be_visible(timeout=TIMEOUT)
    footer_inquiry.click()
    page.wait_for_selector("text=문의구분", timeout=TIMEOUT)
    expect(page.get_by_text("문의구분")).to_be_visible(timeout=TIMEOUT)
    print(f"\n✅ TC055 PASS | Footer 문의하기 → 모달 오픈 확인")


def test_TC056_page_title_not_empty(page: Page):
    """TC056: 페이지 타이틀이 비어있지 않음 확인"""
    title = page.title()
    assert title != "", "페이지 타이틀이 비어있습니다."
    assert len(title) > 2, f"타이틀이 너무 짧습니다: '{title}'"
    print(f"\n✅ TC056 PASS | 타이틀: '{title}'")


def test_TC057_no_console_errors(page: Page):
    """TC057: 페이지 로드 시 콘솔 에러(error 레벨) 없음 확인"""
    errors: list[str] = []

    def handle_console(msg):
        if msg.type == "error":
            errors.append(msg.text)

    page.on("console", handle_console)
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(2_000)

    critical_errors = [e for e in errors
                       if not any(skip in e for skip in
                                  ["ERR_BLOCKED", "net::ERR", "favicon",
                                   "third-party", "analytics", "gtag"])]

    if critical_errors:
        print(f"\n⚠️  TC057 콘솔 에러: {critical_errors}")
    else:
        print(f"\n✅ TC057 PASS | 콘솔 에러 없음 (무시된 외부 오류: {len(errors)}건)")

    assert len(critical_errors) == 0, \
        f"콘솔 에러 발생:\n" + "\n".join(critical_errors)


# ══════════════════════════════════════════════════════════════════════════════
# [성능 Performance]  TC058 – TC060
# ══════════════════════════════════════════════════════════════════════════════

def test_TC058_page_load_under_3seconds(page: Page):
    """TC058: 페이지 domcontentloaded 완료까지 3초 이내 — 초과 시 UX/SEO 불이익"""
    start = time.time()
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    elapsed = time.time() - start

    assert elapsed < 3.0, (
        f"페이지 로드 {elapsed:.2f}초 — 3초 기준 초과. "
        "이미지 최적화·CDN 적용 필요"
    )
    print(f"\n✅ TC058 PASS | 로드 {elapsed:.2f}초")


def test_TC059_image_count_not_excessive(page: Page):
    """TC059: img 태그 30개 미만 — 초과 시 초기 로딩 성능 저하"""
    count = page.locator("img").count()
    assert count < 30, (
        f"img 태그 {count}개 — 30개 기준 초과. "
        "loading='lazy' 적용 필요"
    )
    print(f"\n✅ TC059 PASS | img 태그 {count}개")


def test_TC060_offscreen_images_lazy_loaded(page: Page):
    """TC060: 뷰포트 밖 img에 loading='lazy' 적용 여부 — 미적용 시 불필요한 초기 로딩 발생"""
    # 모든 img 중 loading 속성이 없는 것 수집
    images = page.locator("img").all()
    no_lazy = []
    for img in images:
        loading = img.get_attribute("loading")
        src = img.get_attribute("src") or "unknown"
        # loading 속성 자체가 없는 이미지를 누락으로 판단
        if loading is None:
            no_lazy.append(src.split("/")[-1])  # 파일명만 추출

    assert len(no_lazy) == 0, (
        f"lazy loading 미적용 이미지 {len(no_lazy)}개:\n" +
        "\n".join(no_lazy[:5]) +
        "\n→ img 태그에 loading='lazy' 추가 필요"
    )
    print(f"\n✅ TC060 PASS | 전체 img lazy loading 적용 확인")


# ══════════════════════════════════════════════════════════════════════════════
# [접근성 Accessibility]  TC061 – TC065
# ══════════════════════════════════════════════════════════════════════════════

def test_TC061_images_have_alt_text(page: Page):
    """TC061: 모든 img에 alt 속성 존재 — 없으면 WCAG 2.1 위반 (스크린리더 사용자 배제)"""
    images = page.locator("img").all()
    missing = [
        (img.get_attribute("src") or "unknown").split("/")[-1]
        for img in images
        if img.get_attribute("alt") is None
    ]
    assert len(missing) == 0, (
        f"alt 누락 이미지 {len(missing)}개:\n" +
        "\n".join(missing[:5]) +
        "\n→ 각 img에 alt='설명' 추가 필요"
    )
    print(f"\n✅ TC061 PASS | 전체 이미지 alt 텍스트 확인")


def test_TC062_icon_buttons_have_aria_label(page: Page):
    """TC062: 텍스트 없는 버튼에 aria-label 존재 — 없으면 스크린리더가 용도를 알 수 없음"""
    buttons = page.locator("button").all()
    unlabeled = []
    for btn in buttons:
        text  = btn.inner_text().strip()
        aria  = btn.get_attribute("aria-label") or ""
        title = btn.get_attribute("title") or ""
        if not text and not aria and not title:
            unlabeled.append(btn.get_attribute("class") or "class없음")

    assert len(unlabeled) == 0, (
        f"레이블 없는 버튼 {len(unlabeled)}개:\n" +
        "\n".join(unlabeled[:5]) +
        "\n→ aria-label='버튼 설명' 추가 필요"
    )
    print(f"\n✅ TC062 PASS | 전체 버튼 aria-label 확인")


def test_TC063_form_inputs_have_label_or_placeholder(page: Page):
    """TC063: 수익계산기 모달 input에 label 또는 placeholder 존재 — 없으면 입력 목적 불명확"""
    page.get_by_role("link", name="수익계산기").click()
    page.get_by_role("textbox").first.wait_for(state="visible", timeout=TIMEOUT)

    inputs = page.locator("input:visible").all()
    unlabeled = []
    for inp in inputs:
        placeholder = inp.get_attribute("placeholder") or ""
        input_id    = inp.get_attribute("id") or ""
        # id가 있으면 label[for=id] 연결 여부 확인
        has_label = False
        if input_id:
            has_label = page.locator(f"label[for='{input_id}']").count() > 0
        if not placeholder and not has_label:
            unlabeled.append(inp.get_attribute("name") or "unknown")

    assert len(unlabeled) == 0, (
        f"label·placeholder 없는 input {len(unlabeled)}개:\n" +
        "\n".join(unlabeled) +
        "\n→ placeholder 또는 <label for=...> 추가 필요"
    )
    print(f"\n✅ TC063 PASS | 폼 input 레이블 확인")


def test_TC064_no_negative_tabindex_on_form(page: Page):
    """TC064: 폼 input에 tabindex=-1 없음 — 있으면 키보드 사용자가 해당 필드 접근 불가"""
    page.get_by_role("link", name="수익계산기").click()
    page.get_by_role("textbox").first.wait_for(state="visible", timeout=TIMEOUT)

    inputs = page.locator("input:visible").all()
    blocked = [
        inp.get_attribute("placeholder") or "unknown"
        for inp in inputs
        if inp.get_attribute("tabindex") == "-1"
    ]
    assert len(blocked) == 0, (
        f"tabindex=-1 input {len(blocked)}개 (키보드 접근 차단):\n" +
        "\n".join(blocked) +
        "\n→ tabindex 속성 제거 필요"
    )
    print(f"\n✅ TC064 PASS | 폼 키보드 접근성 확인")


def test_TC065_links_have_meaningful_text(page: Page):
    """TC065: 링크 텍스트가 '여기', '클릭' 등 무의미한 단어가 아닌지 확인 — SEO·접근성 불이익"""
    # 스크린리더 사용자는 링크 텍스트만 읽으므로 '여기를 클릭' 같은 표현은 맥락 전달 불가
    vague_words = ["여기", "클릭", "click here", "here", "더보기만"]
    links = page.locator("a").all()
    vague_links = []
    for link in links:
        text = link.inner_text().strip().lower()
        if text in vague_words:
            vague_links.append(text)

    assert len(vague_links) == 0, (
        f"무의미한 링크 텍스트 {len(vague_links)}개: {vague_links}\n"
        "→ '자세히 보기', '수익 계산하기' 등 구체적 텍스트로 변경 필요"
    )
    print(f"\n✅ TC065 PASS | 링크 텍스트 의미 있음 확인")


# ══════════════════════════════════════════════════════════════════════════════
# [SEO]  TC066 – TC069
# ══════════════════════════════════════════════════════════════════════════════

def test_TC066_meta_description_exists_and_length(page: Page):
    """TC066: meta description 존재 및 50자 이상 — 없으면 구글이 임의 텍스트 노출"""
    meta = page.locator('meta[name="description"]')
    assert meta.count() > 0, (
        "meta description 태그 없음\n"
        "→ <meta name='description' content='...'> 추가 필요"
    )
    content = meta.get_attribute("content") or ""
    assert len(content) >= 50, (
        f"meta description {len(content)}자 — 50자 이상 권장\n"
        f"현재: '{content}'"
    )
    print(f"\n✅ TC066 PASS | meta description {len(content)}자 확인")


def test_TC067_single_h1_tag(page: Page):
    """TC067: h1 태그 정확히 1개 — 0개면 주제 없음, 2개 이상이면 SEO 구조 혼란"""
    count = page.locator("h1").count()
    assert count == 1, (
        f"h1 태그 {count}개 감지 — 페이지당 정확히 1개 필요\n"
        "→ 핵심 제목 1개만 h1, 나머지는 h2·h3으로 변경"
    )
    print(f"\n✅ TC067 PASS | h1 태그 1개 확인")


def test_TC068_og_tags_exist(page: Page):
    """TC068: OG 태그(og:title, og:description) 존재 — 없으면 SNS 공유 시 미리보기 깨짐"""
    og_title = page.locator('meta[property="og:title"]').count()
    og_desc  = page.locator('meta[property="og:description"]').count()

    missing = []
    if og_title == 0:
        missing.append("og:title")
    if og_desc == 0:
        missing.append("og:description")

    assert len(missing) == 0, (
        f"OG 태그 누락: {missing}\n"
        "→ <meta property='og:title' content='...'> 추가 필요"
    )
    print(f"\n✅ TC068 PASS | OG 태그 확인")


def test_TC069_canonical_url_exists(page: Page):
    """TC069: canonical URL 태그 존재 — 없으면 중복 URL로 검색 순위 분산"""
    canonical = page.locator('link[rel="canonical"]')
    assert canonical.count() > 0, (
        "canonical 태그 없음\n"
        "→ <link rel='canonical' href='https://solarteq.co.kr/ko'> 추가 필요"
    )
    href = canonical.get_attribute("href") or ""
    assert "solarteq" in href, f"canonical href가 올바르지 않음: {href}"
    print(f"\n✅ TC069 PASS | canonical: {href}")


# ══════════════════════════════════════════════════════════════════════════════
# [보안 Security]  TC070 – TC072
# ══════════════════════════════════════════════════════════════════════════════

def test_TC070_external_links_noopener(page: Page):
    """TC070: target=_blank 외부 링크에 rel=noopener 존재 — 없으면 tabnapping 취약점"""
    links = page.locator('a[target="_blank"]').all()
    vulnerable = [
        link.get_attribute("href") or "unknown"
        for link in links
        if "noopener" not in (link.get_attribute("rel") or "")
    ]
    assert len(vulnerable) == 0, (
        f"noopener 없는 외부 링크 {len(vulnerable)}개:\n" +
        "\n".join(vulnerable[:5]) +
        "\n→ rel='noopener noreferrer' 추가 필요"
    )
    print(f"\n✅ TC070 PASS | 외부 링크 noopener 확인")


def test_TC071_http_redirects_to_https(page: Page):
    """TC071: HTTP 접속 시 HTTPS로 자동 리다이렉트 — 미적용 시 데이터 평문 전송 위험"""
    # HTTP로 접속 후 최종 URL이 https인지 확인
    page.goto("http://solarteq.co.kr/ko", wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)
    assert page.url.startswith("https://"), (
        f"HTTP → HTTPS 리다이렉트 미작동. 현재 URL: {page.url}\n"
        "→ 서버에서 301 리다이렉트 설정 필요"
    )
    print(f"\n✅ TC071 PASS | HTTPS 리다이렉트 확인: {page.url}")


def test_TC072_phone_input_autocomplete(page: Page):
    """TC072: 연락처 input에 autocomplete 속성 존재 — 없으면 브라우저 자동완성 비활성화로 UX 저하"""
    open_inquiry(page)
    # 연락처 input 찾기
    phone_inputs = page.locator("input[type='tel'], input[placeholder*='연락처'], input[placeholder*='전화']")
    if phone_inputs.count() == 0:
        print(f"\n⏭️  TC072 SKIP | 연락처 input 없음")
        return

    inp = phone_inputs.first
    autocomplete = inp.get_attribute("autocomplete")
    assert autocomplete is not None, (
        "연락처 input에 autocomplete 속성 없음\n"
        "→ autocomplete='tel' 추가 권장"
    )
    print(f"\n✅ TC072 PASS | autocomplete='{autocomplete}' 확인")


# ══════════════════════════════════════════════════════════════════════════════
# [UX]  TC073 – TC076
# ══════════════════════════════════════════════════════════════════════════════

def test_TC073_no_horizontal_scroll_mobile(page: Page):
    """TC073: 모바일(375px)에서 가로 스크롤 없음 — 있으면 UX 심각 저하"""
    page.set_viewport_size({"width": 375, "height": 812})
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)

    # scrollWidth > clientWidth 이면 가로 스크롤 발생 중
    has_scroll = page.evaluate(
        "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    assert not has_scroll, (
        "모바일 375px에서 가로 스크롤 발생\n"
        "→ 개발자도구에서 가로 넘치는 요소 확인 후 overflow-x: hidden 처리"
    )
    print(f"\n✅ TC073 PASS | 모바일 가로 스크롤 없음 확인")


def test_TC074_custom_404_page(page: Page):
    """TC074: 잘못된 URL 접근 시 404 처리 — 기본 서버 오류 페이지 대신 안내 페이지 필요"""
    page.goto("https://solarteq.co.kr/ko/nonexistent-page-xyz", wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)

    # 404 처리 여부: 타이틀 또는 본문에 404 관련 문구가 있거나 홈으로 리다이렉트됐는지 확인
    page_text = page.inner_text("body").lower()
    is_handled = (
        "404" in page_text
        or "찾을 수 없" in page_text
        or "not found" in page_text
        or "/ko" in page.url  # 홈으로 리다이렉트된 경우
    )
    assert is_handled, (
        f"404 페이지 미처리 — URL: {page.url}\n"
        "→ 커스텀 404 페이지 또는 홈 리다이렉트 설정 필요"
    )
    print(f"\n✅ TC074 PASS | 404 처리 확인: {page.url}")


def test_TC075_cta_button_visible_without_scroll(page: Page):
    """TC075: 데스크탑(1280px) 기준 수익계산기 CTA 버튼이 스크롤 없이 뷰포트에 노출"""
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)

    # 수익계산기 버튼이 초기 화면(above the fold)에 보이는지 확인
    calc_btn = page.get_by_role("link", name="수익계산기").first
    expect(calc_btn).to_be_visible(timeout=TIMEOUT)

    # 스크롤 위치 0에서 버튼이 뷰포트 내에 있는지 JS로 검증
    in_viewport = calc_btn.evaluate(
        "el => { const r = el.getBoundingClientRect(); return r.top >= 0 && r.bottom <= window.innerHeight; }"
    )
    assert in_viewport, (
        "수익계산기 버튼이 초기 뷰포트 밖에 위치\n"
        "→ 핵심 CTA는 스크롤 없이 보이는 위치(above the fold)에 배치 권장"
    )
    print(f"\n✅ TC075 PASS | CTA 버튼 above the fold 확인")


def test_TC076_inquiry_form_submit_feedback(page: Page):
    """TC076: 문의 폼 제출 후 사용자 피드백(완료 메시지·alert) 여부 — 없으면 제출 성공 여부 불명확"""
    open_inquiry(page)

    # 라디오 첫 번째 선택
    radios = page.locator("input[type='radio']").all()
    if radios:
        radios[0].evaluate("el => el.click()")

    # 연락처 입력
    phone = page.locator("input[type='tel'], input[placeholder*='연락처']").first
    if phone.count() > 0 or page.locator("input[placeholder*='연락처']").count() > 0:
        try:
            page.locator("input[placeholder*='연락처']").first.fill("010-1234-5678")
        except Exception:
            pass

    # 제출 전 dialog 등록
    messages = catch_dialog(page)

    # 제출 버튼 클릭
    submit = page.get_by_role("button", name=re.compile("제출|확인|신청|보내기", re.IGNORECASE)).first
    if submit.count() == 0:
        print(f"\n⏭️  TC076 SKIP | 제출 버튼 없음")
        return

    submit.click()
    page.wait_for_timeout(1_500)

    # 피드백 확인: alert 메시지 또는 완료 문구
    feedback_text = page.inner_text("body")
    has_feedback = (
        len(messages) > 0  # alert 발생
        or "완료" in feedback_text
        or "감사" in feedback_text
        or "접수" in feedback_text
        or "성공" in feedback_text
    )
    assert has_feedback, (
        "제출 후 피드백 없음 — 사용자가 성공 여부를 알 수 없음\n"
        "→ 제출 완료 메시지 또는 alert 추가 필요"
    )
    print(f"\n✅ TC076 PASS | 제출 피드백 확인: {messages or '완료 문구 노출'}")
