"""
DOT APPS E2E 자동화 테스트
===========================
대상: https://dot.apps-dotincorp.com/
TC001 ~ TC044 (44개)

실행 전체:
    pytest test_dot_all.py -v -s

섹션별 실행 예시:
    pytest test_dot_all.py -v -k "TC01"   # TC010~TC019 범위
    pytest test_dot_all.py -v -k "login"

슬로우모션 디버깅:
    pytest test_dot_all.py -v --headed --slowmo=800 -k "TC015"
"""

import re
import pytest
from playwright.sync_api import Page, expect

# ===========================================================================
# 설정값 — 환경에 맞게 수정
# ===========================================================================
BASE_URL       = "https://dot.apps-dotincorp.com/"
VALID_USER     = "hhj"
VALID_PASSWORD = "guru133//"
ERROR_MSG      = "The username or password do"   # 로그인 실패 시 오류 문구 (앞부분)


# ===========================================================================
# 공통 헬퍼 함수
# ===========================================================================

def close_popup_if_exists(page: Page, timeout: int = 5000) -> None:
    """페이지 진입 시 팝업 모달이 있으면 닫는다. 없으면 그냥 넘어간다."""
    try:
        modal = page.locator(".modal.show")
        modal.wait_for(timeout=timeout)
        modal.locator(".a11y-footer-noShow").click()
        modal.wait_for(state="hidden", timeout=timeout)
    except Exception:
        pass


def open_login_modal(page: Page) -> None:
    """헤더의 '로그인' 버튼을 눌러 로그인 페이지(또는 모달)를 연다.
    사이트는 외부 SSO(account.dot.apps-dotincorp.com)로 리다이렉트하므로
    domcontentloaded 완료까지 대기한다.
    """
    page.get_by_role("button", name="로그인").click()
    page.wait_for_load_state("domcontentloaded")


def do_login(page: Page, username: str = VALID_USER, password: str = VALID_PASSWORD) -> None:
    """로그인 모달 열기 → 아이디/비밀번호 입력 → Login 버튼 클릭."""
    open_login_modal(page)
    page.get_by_role("textbox", name="Username").fill(username)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(1000)


def open_settings(page: Page) -> None:
    """헤더 설정 버튼 클릭 → 설정 모달 오픈."""
    page.get_by_role("button", name="설정").click()
    page.wait_for_timeout(500)


def open_device(page: Page) -> None:
    """헤더 기기연결 버튼 클릭 → 기기연결 모달 오픈."""
    page.get_by_role("button", name="기기 연결").click()
    page.wait_for_timeout(500)


# ===========================================================================
# Fixture — 매 테스트 전 홈으로 이동 + 애니메이션 비활성화
# ===========================================================================

@pytest.fixture(autouse=True)
def setup(page: Page):
    """
    모든 테스트에 자동 적용되는 준비 단계.
    1) 애니메이션/트랜지션을 0s로 → 타이밍 오류 방지
    2) 홈 페이지로 이동
    3) 팝업이 있으면 닫기
    """
    page.add_style_tag(content="""
        *, *::before, *::after {
            animation-duration: 0s !important;
            transition-duration: 0s !important;
        }
    """)
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(800)
    close_popup_if_exists(page)
    yield


# ===========================================================================
# TC001 ~ TC003: 홈페이지 기본
# ===========================================================================

def test_TC001_home_title(page: Page) -> None:
    """[홈] 페이지 타이틀에 'Dot Apps' 포함"""
    expect(page).to_have_title(re.compile("Dot Apps", re.IGNORECASE))


def test_TC002_logo_click_stays_home(page: Page) -> None:
    """[홈] 로고 클릭 → BASE_URL 유지"""
    page.locator("header a[href='/']").first.click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(BASE_URL)


def test_TC003_hero_heading_visible(page: Page) -> None:
    """[홈] 히어로 헤딩 'Read, Listen and Feel' 노출"""
    expect(
        page.get_by_role("heading", name=re.compile("Read, Listen and Feel", re.IGNORECASE))
    ).to_be_visible()


# ===========================================================================
# TC004 ~ TC008: 네비게이션
# ===========================================================================

def test_TC004_nav_home_button(page: Page) -> None:
    """[네비] Home 버튼 → BASE_URL 유지"""
    page.get_by_role("button", name="Home").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(BASE_URL)


def test_TC005_nav_canvas_requires_login(page: Page) -> None:
    """[네비] 비로그인 상태에서 Dot Canvas 클릭 → 로그인 페이지로 리다이렉트"""
    page.get_by_role("button", name="Dot Canvas").click()
    page.wait_for_load_state("domcontentloaded")
    # 로그인이 필요한 페이지 — account 도메인 또는 login 경로로 이동해야 함
    expect(page).to_have_url(re.compile(r"login"))


def test_TC006_nav_cloud_requires_login(page: Page) -> None:
    """[네비] 비로그인 상태에서 Dot Cloud 클릭 → 로그인 페이지로 리다이렉트"""
    page.get_by_role("button", name="Dot Cloud").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"login"))


def test_TC007_nav_support(page: Page) -> None:
    """[네비] Support 버튼 → /support 이동"""
    page.get_by_role("button", name="Support").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/support"))


def test_TC008_accessible_link_href(page: Page) -> None:
    """[네비] Accessible 링크 href에 '/easy' 포함"""
    link = page.get_by_role("link", name="Accessible")
    expect(link).to_be_visible()
    href = link.get_attribute("href")
    assert href and "/easy" in href, f"href 불일치: {href}"


# ===========================================================================
# TC009 ~ TC014: 로그인
# ===========================================================================

def test_TC009_login_modal_open(page: Page) -> None:
    """[로그인] 로그인 버튼 → SSO 로그인 페이지 이동, Username·Password·Login 버튼 노출"""
    open_login_modal(page)
    # 외부 SSO 페이지로 이동 후 필드 로딩 대기
    expect(page.get_by_role("textbox", name="Username")).to_be_visible(timeout=10_000)
    expect(page.get_by_role("textbox", name="Password")).to_be_visible(timeout=10_000)
    expect(page.get_by_role("button",  name="Login")).to_be_visible(timeout=10_000)


def test_TC010_login_success(page: Page) -> None:
    """[로그인] 정상 계정 → 로그인 버튼 사라지고 오류 메시지 없음"""
    do_login(page)
    expect(page).to_have_url(BASE_URL)
    expect(page.get_by_role("button", name="로그인")).not_to_be_visible()
    expect(page.get_by_text(ERROR_MSG)).not_to_be_visible()


def test_TC011_login_fail_wrong_password(page: Page) -> None:
    """[로그인] 올바른 아이디 + 틀린 비밀번호 → 오류 메시지 표시"""
    open_login_modal(page)
    page.get_by_role("textbox", name="Username").fill(VALID_USER)
    page.get_by_role("textbox", name="Password").fill("wrongpass")
    page.get_by_role("button",  name="Login").click()
    expect(page.get_by_text(ERROR_MSG)).to_be_visible()


def test_TC012_login_fail_wrong_username(page: Page) -> None:
    """[로그인] 틀린 아이디 + 틀린 비밀번호 → 오류 메시지 표시"""
    open_login_modal(page)
    page.get_by_role("textbox", name="Username").fill("nobody")
    page.get_by_role("textbox", name="Password").fill("wrongpass")
    page.get_by_role("button",  name="Login").click()
    # 서버 응답 대기 후 오류 메시지 확인 (timeout 10초)
    expect(page.get_by_text(ERROR_MSG)).to_be_visible(timeout=10_000)


def test_TC013_login_fail_empty_fields(page: Page) -> None:
    """[로그인] 빈 값 제출 → 로그인 폼 그대로 유지"""
    open_login_modal(page)
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_role("textbox", name="Username")).to_be_visible()
    expect(page.get_by_role("button",  name="Login")).to_be_visible()


def test_TC014_login_fail_keeps_login_button(page: Page) -> None:
    """[로그인] 실패 후 Login 버튼 여전히 노출 (폼 닫히지 않음)"""
    open_login_modal(page)
    page.get_by_role("textbox", name="Username").fill("bad")
    page.get_by_role("textbox", name="Password").fill("bad")
    page.get_by_role("button",  name="Login").click()
    expect(page.get_by_role("button", name="Login")).to_be_visible()


# ===========================================================================
# TC015 ~ TC022: 설정 모달
# ===========================================================================

def test_TC015_settings_modal_open(page: Page) -> None:
    """[설정] 설정 버튼 → '설정' 모달 타이틀 헤딩 노출"""
    open_settings(page)
    # exact=True: '언어설정' 등 '설정'을 포함하는 다른 heading과 구분
    expect(page.get_by_role("heading", name="설정", exact=True)).to_be_visible()


def test_TC016_settings_close_button(page: Page) -> None:
    """[설정] 닫기 버튼 → 설정 모달 숨김"""
    open_settings(page)
    # 설정 모달은 dialog 요소 안에 있으므로 dialog 내 닫기 버튼을 클릭
    page.get_by_role("dialog").get_by_role("button", name="닫기").click()
    page.wait_for_timeout(500)
    expect(page.get_by_role("heading", name="설정")).not_to_be_visible()


def test_TC017_settings_cancel_button(page: Page) -> None:
    """[설정] 취소 버튼 → 설정 모달 닫힘"""
    open_settings(page)
    page.get_by_role("button", name="취소").click()
    page.wait_for_timeout(500)
    expect(page.get_by_role("heading", name="설정")).not_to_be_visible()


def test_TC018_settings_language_section(page: Page) -> None:
    """[설정] 언어설정 섹션 헤딩 노출"""
    open_settings(page)
    expect(page.get_by_role("heading", name="언어설정")).to_be_visible()


def test_TC019_settings_braille_section(page: Page) -> None:
    """[설정] 점자 서식 섹션 헤딩 노출"""
    open_settings(page)
    expect(page.get_by_role("heading", name="점자 서식")).to_be_visible()


def test_TC020_settings_line_spacing_radio(page: Page) -> None:
    """[설정] 행간 2 라디오 선택 → checked"""
    open_settings(page)
    radio = page.get_by_role("radio", name="행간 2")
    radio.evaluate("el => el.click()")
    assert radio.is_checked(), "행간 2 라디오가 체크되지 않음"


def test_TC021_settings_char_spacing_radio(page: Page) -> None:
    """[설정] 자간 1 라디오 선택 → checked"""
    open_settings(page)
    radio = page.get_by_role("radio", name="자간 1")
    radio.evaluate("el => el.click()")
    assert radio.is_checked(), "자간 1 라디오가 체크되지 않음"


def test_TC022_settings_save_button(page: Page) -> None:
    """[설정] 변경 사항 저장 버튼 클릭 → 모달 닫힘"""
    open_settings(page)
    page.get_by_role("button", name="변경 사항 저장").click()
    page.wait_for_timeout(500)
    expect(page.get_by_role("heading", name="설정")).not_to_be_visible()


# ===========================================================================
# TC023 ~ TC027: 기기 연결 모달
# ===========================================================================

def test_TC023_device_modal_open(page: Page) -> None:
    """[기기연결] 기기 연결 버튼 → '기기연결' 헤딩 노출"""
    open_device(page)
    expect(page.get_by_role("heading", name="기기연결")).to_be_visible()


def test_TC024_device_bluetooth_radio(page: Page) -> None:
    """[기기연결] Bluetooth LE 라디오 선택 → checked"""
    open_device(page)
    radio = page.get_by_role("radio", name="Bluetooth LE")
    radio.evaluate("el => el.click()")
    assert radio.is_checked(), "Bluetooth LE 라디오가 체크되지 않음"


def test_TC025_device_usb_radio(page: Page) -> None:
    """[기기연결] USB 라디오 선택 → checked"""
    open_device(page)
    radio = page.get_by_role("radio", name="USB")
    radio.evaluate("el => el.click()")
    assert radio.is_checked(), "USB 라디오가 체크되지 않음"


def test_TC026_device_search_button_visible(page: Page) -> None:
    """[기기연결] Search Device 버튼 노출 확인 (클릭 생략 — Bluetooth 네이티브 다이얼로그 유발)"""
    open_device(page)
    btn = page.get_by_role("button", name="Search Device")
    expect(btn).to_be_visible()


def test_TC027_device_modal_close(page: Page) -> None:
    """[기기연결] 닫기 버튼 → 기기연결 모달 숨김"""
    open_device(page)
    expect(page.get_by_role("heading", name="기기연결")).to_be_visible()
    # 기기연결 모달의 닫기 버튼은 DOM 순서상 .first (설정 dialog보다 먼저 등장)
    page.get_by_role("button", name="닫기").first.click()
    page.wait_for_timeout(500)
    expect(page.get_by_role("heading", name="기기연결")).not_to_be_visible()


# ===========================================================================
# TC028 ~ TC030: 메인 서비스 카드
# ===========================================================================

def test_TC028_card_dot_canvas_visible(page: Page) -> None:
    """[카드] Move To Dot Canvas 버튼 노출"""
    expect(page.get_by_role("button", name="Move To Dot Canvas")).to_be_visible()


def test_TC029_card_dot_cloud_visible(page: Page) -> None:
    """[카드] Move To Dot Cloud 버튼 노출"""
    expect(page.get_by_role("button", name="Move To Dot Cloud")).to_be_visible()


def test_TC030_card_support_visible(page: Page) -> None:
    """[카드] Move To Dot Support 버튼 노출"""
    expect(page.get_by_role("button", name="Move To Dot Support")).to_be_visible()


# ===========================================================================
# TC031 ~ TC033: Move To 버튼 — 페이지 이동
# ===========================================================================

def test_TC031_move_to_canvas_after_login(page: Page) -> None:
    """[이동] 로그인 후 Move To Dot Canvas → /canvas 이동"""
    do_login(page)
    page.get_by_role("button", name="Move To Dot Canvas").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/canvas"))


def test_TC032_move_to_cloud_after_login(page: Page) -> None:
    """[이동] 로그인 후 Move To Dot Cloud → /cloud 이동"""
    do_login(page)
    page.get_by_role("button", name="Move To Dot Cloud").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/cloud"))


def test_TC033_move_to_support(page: Page) -> None:
    """[이동] Move To Dot Support → URL에 /support 포함"""
    page.get_by_role("button", name="Move To Dot Support").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page).to_have_url(re.compile(r"/support"))


# ===========================================================================
# TC034 ~ TC038: 푸터
# ===========================================================================

def test_TC034_footer_copyright(page: Page) -> None:
    """[푸터] Copyright Dot Incorporation 텍스트 노출"""
    expect(page.get_by_text("Copyright Dot Incorporation")).to_be_visible()


def test_TC035_footer_terms_href(page: Page) -> None:
    """[푸터] 이용약관 링크 href에 'terms' 포함"""
    href = page.locator("a[href*='terms']").first.get_attribute("href")
    assert href and "terms" in href, f"terms href 없음: {href}"


def test_TC036_footer_privacy_href(page: Page) -> None:
    """[푸터] 개인정보처리방침 링크 href에 'privacy' 포함"""
    href = page.locator("a[href*='privacy']").first.get_attribute("href")
    assert href and "privacy" in href, f"privacy href 없음: {href}"


def test_TC037_footer_family_sites(page: Page) -> None:
    """[푸터] 패밀리 사이트 버튼 클릭 → dotincorp.com 링크 노출"""
    page.get_by_role("button", name="이용 가능한 패밀리 사이트").click()
    page.wait_for_timeout(500)
    expect(page.locator("a[href='https://www.dotincorp.com']").first).to_be_visible()


def test_TC038_footer_easy_link(page: Page) -> None:
    """[푸터] 패밀리 사이트 내 /easy 링크 href 확인"""
    page.get_by_role("button", name="이용 가능한 패밀리 사이트").click()
    page.wait_for_timeout(500)
    href = page.locator("a[href*='/easy']").first.get_attribute("href")
    assert href and "/easy" in href, f"/easy href 없음: {href}"


# ===========================================================================
# TC039 ~ TC042: 반응형 뷰포트
# ===========================================================================

def test_TC039_responsive_1920(page: Page) -> None:
    """[반응형] 1920×1080 데스크탑 — 로고·버튼 노출"""
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(500)
    expect(page.get_by_role("img", name="Dot Incorporation Logo")).to_be_visible()
    expect(page.get_by_role("button", name="로그인")).to_be_visible()


def test_TC040_responsive_1280(page: Page) -> None:
    """[반응형] 1280×800 데스크탑 — 로고·버튼 노출"""
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(500)
    expect(page.get_by_role("img", name="Dot Incorporation Logo")).to_be_visible()
    expect(page.get_by_role("button", name="로그인")).to_be_visible()


def test_TC041_responsive_768(page: Page) -> None:
    """[반응형] 768×1024 태블릿 — 로고 노출"""
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(500)
    expect(page.get_by_role("img", name="Dot Incorporation Logo")).to_be_visible()


def test_TC042_responsive_375(page: Page) -> None:
    """[반응형] 375×812 모바일 — 로고 노출"""
    page.set_viewport_size({"width": 375, "height": 812})
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(500)
    expect(page.get_by_role("img", name="Dot Incorporation Logo")).to_be_visible()


# ===========================================================================
# TC043 ~ TC044: 기타
# ===========================================================================

def test_TC043_no_console_errors(page: Page) -> None:
    """[기타] 홈 페이지 로드 시 예기치 않은 콘솔 에러 없음
    (401 Unauthorized는 비로그인 API 호출의 정상 동작 — 제외)
    """
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)
    # 401은 로그인 전 API 호출 시 정상적으로 발생 → 필터링
    unexpected = [e for e in errors if "401" not in e]
    assert len(unexpected) == 0, f"예기치 않은 콘솔 에러: {unexpected}"


def test_TC044_page_title_not_empty(page: Page) -> None:
    """[기타] 페이지 타이틀이 비어있지 않음 (len > 2)"""
    title = page.title()
    assert len(title) > 2, f"타이틀이 너무 짧음: '{title}'"
