# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Language

코드 내 주석은 한국어로 작성한다.

---

## Project Overview

> **E2E(End-to-End) 테스트란?**
> 실제 브라우저를 열어 사용자가 하는 행동(클릭, 입력, 이동)을 자동으로 재현하고,
> 화면이 올바르게 동작하는지 검증하는 테스트 방식이다.

Playwright + pytest 기반 E2E 테스트 자동화 파이프라인.
URL 하나를 입력하면 → 페이지 분석 → TC 도출 → 테스트 실행 → Excel 리포트 생성까지 자동화한다.

**새 사이트 작업 순서:**
1. 브라우저로 대상 URL 열기 → 페이지 구조 분석
2. 카테고리별 TC 도출 (홈 · 네비 · 폼 · 모달 · 반응형 · 언어 · 기타)
3. `test_<사이트명>_all.py` 작성 (TC001부터 순번)
4. pytest 실행
5. `make_report_now.py` 수정 후 실행 → Excel 리포트 생성
6. `HANDOFF.md` 결과 섹션 업데이트

---

## Commands

```bash
# 전체 테스트 실행 (-v: 결과 상세 출력, -s: print 출력 허용)
# pytest.ini에 --headed가 기본 설정되어 있어 브라우저 창이 열린다
pytest test_<사이트명>_all.py -v -s

# 특정 TC만 실행 (-k: 이름 필터)
pytest test_<사이트명>_all.py -v -k "TC005"

# 크로스 브라우저 실행 (여러 브라우저 동시 지정 가능)
pytest test_<사이트명>_all.py -v --browser chromium --browser firefox

# 실패 시 스크린샷 자동 저장
pytest test_<사이트명>_all.py -v --screenshot=only-on-failure --output=screenshots/

# 슬로우모션 디버깅 (--slowmo=800: 각 액션마다 800ms 딜레이)
# 실패 TC를 눈으로 확인할 때 사용
pytest test_<사이트명>_all.py -v --headed --slowmo=800 -k "TC005"

# Excel 리포트만 빠르게 생성 (pytest 재실행 없음, 가장 자주 씀)
python make_report_now.py

# 풀 파이프라인: pytest 실행 + JSON 파싱 + Excel 생성
python generate_report.py
```

---

## File Naming Convention

```
test_<사이트명>_all.py      # 통합 테스트 파일 (TC001~ 모두 포함)
make_report_<사이트명>.py   # 리포트 생성 스크립트 (선택)
```

---

## Key Code Patterns

> 새 사이트 작업 시 아래 패턴을 그대로 복사해서 사용한다.
> 직접 만들려 하면 타이밍·strict mode 오류가 반드시 발생한다.

```python
BASE_URL = "https://example.com/ko"

# ── autouse fixture ──────────────────────────────────────────
# autouse=True: 모든 테스트 함수 실행 전 자동으로 이 fixture가 먼저 실행됨
# 즉, 매 TC마다 항상 홈으로 이동한 상태에서 시작하게 된다
@pytest.fixture(autouse=True)
def setup(page):
    # wait_until="domcontentloaded": HTML 파싱 완료 시점까지만 기다림 (load보다 빠름)
    # timeout=30_000: 30초 안에 응답 없으면 오류 발생
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    # 페이지 이동 후 JS 렌더링 완료를 위해 1초 추가 대기
    page.wait_for_timeout(1_000)


# ── 다이얼로그(alert) 처리 ────────────────────────────────────
# 핵심: 액션(클릭·입력) 실행 BEFORE에 반드시 등록해야 한다
# 등록이 늦으면 dialog 이벤트가 이미 지나쳐서 타임아웃 발생
def catch_dialog(page):
    messages = []
    # page.once: 이벤트를 딱 한 번만 수신 (page.on은 계속 수신)
    # lambda: 익명 함수. dialog 메시지를 저장하고 자동으로 확인(accept) 클릭
    page.once("dialog", lambda d: (messages.append(d.message), d.accept()))
    return messages  # 반환된 리스트는 액션 후에 assert로 검증


# ── strict mode 방지 ──────────────────────────────────────────
# Playwright는 기본적으로 선택자가 2개 이상 매칭되면 오류(strict mode violation)를 낸다
# .first를 붙이면 첫 번째 요소만 선택하여 오류를 피한다
page.get_by_text("텍스트").first
page.get_by_role("button", name="Next slide").first


# ── viewport 밖 네비 링크 클릭 우회 ──────────────────────────
# 햄버거 메뉴 항목은 화면 밖에 있어 .click()이 실패한다
# force=True도 통하지 않으므로, href 속성을 꺼내서 직접 goto로 이동한다
def click_nav_link(page, name):
    link = page.locator(f"a:has-text('{name}')").first
    href = link.get_attribute("href")          # HTML의 href 속성값 추출
    if href and href.startswith("/"):           # 상대경로면 도메인 붙이기
        href = f"https://도메인{href}"
    page.goto(href, wait_until="domcontentloaded", timeout=30_000)


# ── 숨겨진 라디오/체크박스 클릭 ──────────────────────────────
# CSS로 숨겨진(visibility:hidden 등) 입력 요소는 .click()이 "not visible" 오류를 낸다
# .evaluate()로 JavaScript를 직접 실행하면 가시성 검사를 우회할 수 있다
radio.evaluate("el => el.click()")
```

---

## Known Failure Modes

> 처음 보면 원인을 찾기 어려운 오류 패턴 목록.
> 아래 증상이 보이면 Fix 열의 방법을 바로 적용한다.

| 증상 | 원인 | 해결 |
|------|------|------|
| `with page.expect_event("dialog")` 타임아웃 | dialog 이벤트 등록 타이밍 경쟁 | `page.once("dialog", lambda d: d.accept())` 로 교체 |
| `strict mode violation` 오류 | 같은 선택자에 요소가 2개 이상 매칭 | `.first` 추가 |
| `element outside viewport` (force=True도 실패) | 햄버거 메뉴 항목이 화면 밖에 위치 | `href` 추출 후 `page.goto()` 로 이동 |
| 좌표 클릭이 엉뚱한 요소에 걸림 | 슬라이더 이미지가 앞에서 가림 | `find()` 로 ref 추출 후 `left_click(ref=...)` 사용 |
| 소수점 입력(예: `100.5`)에서 alert 안 뜸 | 사이트가 내부적으로 정수 처리 | alert 대신 결과 화면 표시 여부로 assert |

---

## New Site Checklist

> 새 URL이 주어졌을 때 TC를 작성하기 전에 아래 항목을 직접 확인한다.
> 확인 없이 작성하면 사이트 특성을 놓쳐 TC가 누락되거나 잘못된다.

```
1. 페이지 기본     — 타이틀 확인, 로고 클릭 동작, 404 여부
2. 네비게이션      — GNB 메뉴 항목 및 이동, 햄버거 메뉴, 뒤로가기
3. 핵심 기능       — 폼·계산기·검색 등 주요 인터랙션, 경계값·예외값 입력, 필수 필드 미입력 제출
4. UI 컴포넌트     — 슬라이더·캐러셀, 모달·팝업, 탭·아코디언
5. 반응형          — 1920 / 1280 / 768 / 375 px
6. 기타            — 언어 전환, 콘솔 에러 없음, 외부 링크 href 존재, 개인정보·이용약관 링크
```
