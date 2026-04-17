"""
로그인 기능 자동화 테스트
=======================
이 파일은 웹사이트의 로그인 기능이 올바르게 동작하는지 확인합니다.
- 정상 로그인이 되는지 테스트
- 잘못된 정보로 로그인 시 오류가 표시되는지 테스트
"""

import pytest
from playwright.sync_api import Page, expect


# =============================================================================
# 테스트 설정값 (자신의 환경에 맞게 수정하세요)
# =============================================================================

# 테스트할 웹사이트 주소
BASE_URL = "https://dot.apps-dotincorp.com/"

# 정상 로그인에 사용할 계정 정보
VALID_USER     = "hhj"
VALID_PASSWORD = "guru133//"

# 로그인 실패 시 화면에 표시되는 오류 메시지 (일부만 입력해도 됩니다)
ERROR_MSG = "The username or password do"

# 로그인 실패 케이스 목록 (케이스 이름, 아이디, 비밀번호)
# 새로운 케이스를 추가하려면 아래 목록에 한 줄 추가하면 됩니다.
INVALID_CASES = [
    ("wrong_password", VALID_USER, "sdsd"),   # 올바른 아이디 + 틀린 비밀번호
    ("wrong_username", "adsd",     "sdsd"),   # 틀린 아이디 + 틀린 비밀번호
    ("empty_fields",   "",         ""),       # 아이디/비밀번호 모두 비워둠
]


# =============================================================================
# 공통 함수 (반복되는 동작을 함수로 분리)
# =============================================================================

def close_popup_if_exists(page: Page, timeout: int = 5000) -> None:
    """
    팝업(모달)이 떠 있으면 닫습니다.
    팝업이 없어도 오류 없이 넘어갑니다.
    """
    try:
        modal = page.locator(".modal.show")
        modal.wait_for(timeout=timeout)
        modal.locator(".a11y-footer-noShow").click()
        modal.wait_for(state="hidden", timeout=timeout)
    except Exception:
        # 팝업이 없거나 이미 닫혀 있으면 그냥 넘어감
        pass


def fill_login_form(page: Page, username: str, password: str) -> None:
    """
    아이디와 비밀번호를 입력하고 로그인 버튼을 누릅니다.
    """
    page.get_by_role("textbox", name="Username").fill(username)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button",  name="Login").click()


# =============================================================================
# 테스트 준비 (fixture)
# =============================================================================

@pytest.fixture
def login_page(page: Page) -> Page:
    """
    각 테스트가 시작되기 전에 실행되는 준비 단계입니다.
    1. 웹사이트에 접속
    2. 애니메이션 비활성화 (테스트 안정성 향상)
    3. 팝업 닫기
    4. 로그인 폼 열기
    """
    # 1. 웹사이트 접속
    page.goto(BASE_URL, wait_until="domcontentloaded")

    # 2. CSS 애니메이션/트랜지션을 즉시 완료되도록 설정
    #    → 페이드인 같은 애니메이션 때문에 테스트가 실패하는 상황을 방지
    page.add_style_tag(content="""
        *, *::before, *::after {
            animation-duration: 0s !important;
            transition-duration: 0s !important;
        }
    """)

    # 3. 화면에 팝업이 있으면 닫기
    close_popup_if_exists(page)

    # 4. 로그인 버튼 클릭 → 로그인 폼(모달) 열기
    page.get_by_role("button", name="로그인").click()

    return page


# =============================================================================
# 테스트 케이스
# =============================================================================

def test_login_success(login_page: Page) -> None:
    """
    [성공 케이스] 올바른 아이디/비밀번호로 로그인하면
    - 로그인 버튼이 사라져야 한다
    - 오류 메시지가 보이지 않아야 한다
    """
    # 올바른 계정 정보로 로그인 시도
    fill_login_form(login_page, VALID_USER, VALID_PASSWORD)

    # 로그인 후 URL이 그대로여야 함 (리다이렉트 없는 SPA 구조 기준)
    expect(login_page).to_have_url(BASE_URL)

    # 로그인 버튼이 더 이상 보이지 않아야 함 (로그인 성공 확인)
    expect(login_page.get_by_role("button", name="로그인")).not_to_be_visible()

    # 오류 메시지가 보이지 않아야 함
    expect(login_page.get_by_text(ERROR_MSG)).not_to_be_visible()


@pytest.mark.parametrize("case_id, username, password", INVALID_CASES)
def test_login_fail(login_page: Page, case_id: str, username: str, password: str) -> None:
    """
    [실패 케이스] 잘못된 정보로 로그인하면 오류가 표시되어야 한다.

    케이스별 동작:
    - empty_fields  : 빈 칸이므로 폼이 그대로 유지됨 (브라우저 기본 유효성 검사)
    - 그 외 케이스 : 오류 메시지가 표시되고 로그인 폼이 유지됨
    """
    # 잘못된 계정 정보로 로그인 시도
    fill_login_form(login_page, username, password)

    if case_id == "empty_fields":
        # 빈 칸으로 제출하면 폼이 닫히지 않고 그대로 유지되어야 함
        expect(login_page.get_by_role("textbox", name="Username")).to_be_visible()
        expect(login_page.get_by_role("button",  name="Login")).to_be_visible()
    else:
        # 오류 메시지가 화면에 표시되어야 함
        expect(login_page.get_by_text(ERROR_MSG)).to_be_visible()

        # 로그인 버튼이 아직 보여야 함 (로그인 폼이 유지 중)
        expect(login_page.get_by_role("button", name="Login")).to_be_visible()
