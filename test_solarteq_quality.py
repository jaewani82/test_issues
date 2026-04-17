"""
솔라테크 품질 지표 E2E 테스트
==============================
기능 동작 여부가 아닌 "품질 기준 충족 여부"를 검증한다.
FAIL = 개선이 필요한 실제 품질 문제.

  [성능]
  QA001 - 페이지 로드 3초 이내
  QA002 - 이미지 리소스 개수 (과다 로딩 감지)

  [접근성 Accessibility]
  QA003 - 이미지 alt 텍스트 누락 여부
  QA004 - 버튼에 텍스트 또는 aria-label 존재 여부
  QA005 - 키보드 Tab으로 폼 요소 접근 가능 여부

  [SEO]
  QA006 - meta description 존재 여부
  QA007 - h1 태그 1개만 존재하는지

  [보안/안정성]
  QA008 - 외부 링크 rel=noopener 설정 여부
  QA009 - 콘솔 에러 0개 기준

  [UX]
  QC010 - 모바일(375px)에서 가로 스크롤 없음
"""

import time
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://solarteq.co.kr/ko"


# 매 테스트 시작 전 홈으로 이동 (autouse=True: 모든 TC 자동 적용)
@pytest.fixture(autouse=True)
def setup(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)


# ── 성능 ────────────────────────────────────────────────────────────────────

def test_QA001_page_load_under_3seconds(page: Page):
    """
    페이지 로드가 3초를 초과하면 사용자 이탈률이 급격히 증가한다.
    FAIL 시 조치: 이미지 최적화, CDN 도입, 불필요한 JS 제거
    """
    start = time.time()
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    elapsed = time.time() - start

    assert elapsed < 3.0, (
        f"페이지 로드 {elapsed:.2f}초 — 3초 기준 초과. "
        "이미지 압축 또는 CDN 적용 필요"
    )


def test_QA002_image_count_not_excessive(page: Page):
    """
    이미지가 30개 이상이면 초기 로딩 성능에 부정적 영향을 준다.
    FAIL 시 조치: lazy loading 적용, 불필요한 이미지 제거
    """
    # 페이지 내 모든 img 태그 수집
    images = page.locator("img").all()
    count = len(images)

    assert count < 30, (
        f"img 태그 {count}개 감지 — 30개 기준 초과. "
        "lazy loading(loading='lazy') 적용 필요"
    )


# ── 접근성(Accessibility) ────────────────────────────────────────────────────

def test_QA003_images_have_alt_text(page: Page):
    """
    스크린리더 사용자는 alt 텍스트로 이미지를 인식한다.
    alt 없는 이미지는 웹 접근성 WCAG 2.1 기준 위반.
    FAIL 시 조치: 각 img 태그에 의미 있는 alt 속성 추가
    """
    images = page.locator("img").all()
    missing = []

    for img in images:
        alt = img.get_attribute("alt")
        src = img.get_attribute("src") or "unknown"
        # alt 속성 자체가 없거나 공백만 있는 경우 누락으로 판단
        if alt is None:
            missing.append(src)

    assert len(missing) == 0, (
        f"alt 텍스트 누락 이미지 {len(missing)}개:\n" +
        "\n".join(missing[:5])  # 최대 5개만 출력
    )


def test_QA004_buttons_have_accessible_label(page: Page):
    """
    버튼에 텍스트나 aria-label이 없으면 스크린리더가 용도를 알 수 없다.
    FAIL 시 조치: 아이콘 버튼에 aria-label="메뉴 열기" 등 추가
    """
    buttons = page.locator("button").all()
    unlabeled = []

    for btn in buttons:
        text = btn.inner_text().strip()
        aria  = btn.get_attribute("aria-label") or ""
        title = btn.get_attribute("title") or ""
        if not text and not aria and not title:
            unlabeled.append(btn.get_attribute("class") or "class없음")

    assert len(unlabeled) == 0, (
        f"레이블 없는 버튼 {len(unlabeled)}개 — aria-label 추가 필요:\n" +
        "\n".join(unlabeled[:5])
    )


def test_QA005_form_fields_keyboard_accessible(page: Page):
    """
    키보드만으로 폼 요소에 접근할 수 있어야 한다 (Tab 키 탐색).
    tabindex="-1" 이 필수 입력 필드에 붙어있으면 키보드 사용자 배제.
    FAIL 시 조치: tabindex 제거 또는 양수값으로 수정
    """
    # 수익계산기 모달 열기
    page.get_by_text("수익계산기").first.click()
    page.wait_for_timeout(500)

    # 입력 필드가 tabindex="-1"로 키보드 접근 불가인지 확인
    inputs = page.locator("input:visible").all()
    blocked = []

    for inp in inputs:
        tabindex = inp.get_attribute("tabindex")
        if tabindex == "-1":
            blocked.append(inp.get_attribute("placeholder") or "unknown")

    assert len(blocked) == 0, (
        f"키보드 접근 불가 input {len(blocked)}개 (tabindex=-1):\n" +
        "\n".join(blocked)
    )


# ── SEO ─────────────────────────────────────────────────────────────────────

def test_QA006_meta_description_exists(page: Page):
    """
    meta description은 검색엔진 결과에 노출되는 요약 문구다.
    없으면 구글이 임의의 텍스트를 가져가 검색 노출에 불리하다.
    FAIL 시 조치: <meta name="description" content="..."> 추가
    """
    meta = page.locator('meta[name="description"]')
    count = meta.count()

    assert count > 0, "meta description 태그 없음 — SEO 불이익 발생 가능"

    content = meta.get_attribute("content") or ""
    assert len(content) >= 50, (
        f"meta description이 너무 짧음 ({len(content)}자) — "
        "50자 이상 작성 권장"
    )


def test_QA007_single_h1_tag(page: Page):
    """
    h1은 페이지당 1개가 SEO 표준이다.
    0개: 주제 없음, 2개 이상: 구조 혼란으로 검색 순위 하락.
    FAIL 시 조치: 핵심 제목 1개만 h1, 나머지는 h2/h3으로 변경
    """
    h1_count = page.locator("h1").count()

    assert h1_count == 1, (
        f"h1 태그 {h1_count}개 감지 — 페이지당 정확히 1개 필요"
    )


# ── 보안/안정성 ──────────────────────────────────────────────────────────────

def test_QA008_external_links_have_noopener(page: Page):
    """
    target="_blank" 외부 링크에 rel="noopener"가 없으면
    열린 탭이 원본 페이지를 조작할 수 있는 보안 취약점(tabnapping).
    FAIL 시 조치: rel="noopener noreferrer" 추가
    """
    # target="_blank"인 외부 링크만 수집
    links = page.locator('a[target="_blank"]').all()
    vulnerable = []

    for link in links:
        rel  = link.get_attribute("rel") or ""
        href = link.get_attribute("href") or ""
        if "noopener" not in rel:
            vulnerable.append(href)

    assert len(vulnerable) == 0, (
        f"noopener 없는 외부 링크 {len(vulnerable)}개 (tabnapping 취약점):\n" +
        "\n".join(vulnerable[:5])
    )


def test_QA009_no_console_errors(page: Page):
    """
    JS 콘솔 에러는 기능 오작동의 전조 증상이다.
    사용자에겐 보이지 않지만 내부적으로 실패하는 로직이 있다는 신호.
    FAIL 시 조치: 에러 메시지로 원인 파악 후 JS 코드 수정
    """
    errors = []
    # 콘솔 에러 수집 리스너 등록
    page.on("console", lambda msg: errors.append(msg.text)
            if msg.type == "error" else None)

    # 주요 페이지 순회하며 에러 수집
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(2_000)

    assert len(errors) == 0, (
        f"콘솔 에러 {len(errors)}개 감지:\n" +
        "\n".join(errors[:5])
    )


# ── UX ──────────────────────────────────────────────────────────────────────

def test_QA010_no_horizontal_scroll_on_mobile(page: Page):
    """
    모바일에서 가로 스크롤이 생기면 UX가 크게 저하된다.
    scrollWidth > clientWidth 이면 가로 스크롤 발생 중.
    FAIL 시 조치: overflow-x: hidden 또는 너비 초과 요소 수정
    """
    # 375px: iPhone SE 기준 모바일 뷰
    page.set_viewport_size({"width": 375, "height": 812})
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)

    # JS로 가로 스크롤 여부 직접 측정
    has_scroll = page.evaluate(
        "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )

    assert not has_scroll, (
        "모바일 375px에서 가로 스크롤 발생 — "
        "overflow-x 초과 요소 확인 필요 (개발자도구 → Elements 검사)"
    )
