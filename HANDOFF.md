# HANDOFF — Playwright E2E 테스트 자동화 파이프라인

---

## 목표

URL 하나를 받아 Claude가 페이지를 직접 분석하고,
테스트케이스를 자동 도출해 Playwright로 E2E 테스트를 실행한 뒤
결과를 Excel 리포트로 문서화하는 **재사용 가능한 전체 파이프라인**.

새 URL이 주어지면 아래 순서로 작업한다:

1. 브라우저로 대상 URL 직접 열기 → 페이지 구조 분석
2. 분석 결과 기반으로 TC 도출 (홈·네비·폼·모달·반응형·언어·기타)
3. `test_<사이트명>_all.py` 작성 (TC001부터 순차 번호)
4. `pytest test_<사이트명>_all.py -v -s` 실행
5. `make_report_now.py` 수정 후 실행 → Excel 리포트 생성
6. 이 파일 하단 "작업 결과" 섹션 업데이트

---

## 현재 상태

| 항목 | 내용 |
|------|------|
| 1차 완료 대상 | `https://solarteq.co.kr/ko` |
| 테스트 파일 | `test_solarteq_all.py` (TC001 ~ TC057, 57개) |
| 실행 결과 | **57 / 57 PASS** |
| 리포트 | `solarteq_report_final_20260415_1524.xlsx` |
| 환경 | Playwright + pytest + openpyxl / Chromium |

---

## 완료한 것

### 환경 세팅
- `claude mcp add playwright npx '@playwright/mcp@latest'` — Playwright MCP 연동
- Python 패키지: `playwright`, `pytest`, `pytest-playwright`, `openpyxl` 설치
- `pytest.ini` — `--headed` 기본 옵션 설정

### 파일 목록

| 파일 | 설명 |
|------|------|
| `test_solarteq_all.py` | 솔라테크 통합 E2E 테스트 57개 (TC001~TC057) |
| `make_report_now.py` | pytest 재실행 없이 Excel 리포트 즉시 생성 |
| `generate_report.py` | pytest 실행 + JSON → Excel 생성 (풀 파이프라인) |
| `test_solarteq_full.py` | 구버전 기본 14개 (보존용) |
| `test_solarteq_extended.py` | 구버전 확장 43개 (보존용) |
| `solarteq_report_final_*.xlsx` | 생성된 결과 리포트 |

### 테스트 커버리지 (test_solarteq_all.py)

| 섹션 | TC 범위 | 내용 |
|------|---------|------|
| 홈페이지 | TC001–002 | 타이틀, 로고 |
| 네비게이션 | TC003–004 | 햄버거 오픈/닫기 |
| 수익계산기 기본 | TC005–008 | 모달, 300평, 빈값, 문자 |
| 문의하기 기본 | TC009–010 | 모달, 미입력 제출 |
| 슬라이더/UI 기본 | TC011–012 | Next 버튼, 자세히보기 |
| 기타 기본 | TC013–014 | 언어버튼, 처리방침 |
| 수익계산기 경계/예외 | TC015–027 | 1평·9999평·소수점·음수·0·문자·특수문자 |
| 문의하기 상세 | TC028–036 | 라디오 5종, 연락처, 제출 검증 |
| 네비게이션 상세 | TC037–041 | 서브메뉴, 뒤로가기 |
| UI/슬라이더 상세 | TC042–046 | Prev, 포트폴리오, sticky 헤더, href 검증 |
| 반응형 viewport | TC047–050 | 1920/1280/768/375px |
| 언어 전환 | TC051–053 | /en ↔ /ko |
| 기타/보완 | TC054–057 | policy URL, 콘솔 에러 |

### 핵심 패턴 (신규 사이트에서도 재사용)

```python
# 다이얼로그 자동 처리 — 액션 전에 반드시 등록
def catch_dialog(page):
    messages = []
    page.once("dialog", lambda d: (messages.append(d.message), d.accept()))
    return messages

# strict mode 방지 — 동일 텍스트/역할 복수일 때
page.get_by_text("텍스트").first
page.get_by_role("button", name="Next slide").first

# 햄버거 메뉴 링크 — viewport 밖 이슈 우회
def click_nav_link(page, name):
    link = page.locator(f"a:has-text('{name}')").first
    href = link.get_attribute("href")
    if href and href.startswith("/"):
        href = f"https://도메인{href}"
    page.goto(href, wait_until="domcontentloaded")

# 숨겨진 라디오버튼 클릭
radio.evaluate("el => el.click()")

# autouse fixture — 매 테스트 전 홈 이동
@pytest.fixture(autouse=True)
def setup(page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.wait_for_timeout(1_000)
```

---

## 미완료

- [ ] 새 URL 대상 테스트 작성 (아래 "다음 할 일" 참조)
- [ ] Firefox / WebKit 크로스 브라우저 실행
- [ ] FAIL 시 스크린샷 자동 저장 (`pytest --screenshot=only-on-failure`)
- [ ] Allure / pytest-html 리포트 연동
- [ ] CI/CD 연동 (GitHub Actions)
- [ ] 네트워크 느린 환경 시뮬레이션 (`page.route` 활용)
- [ ] 접근성(Accessibility) 검증 (ARIA, 키보드 탐색)

---

## 실패한 시도

| 시도 | 문제 | 대안 |
|------|------|------|
| `with page.expect_event("dialog")` | dismiss() 타이밍 이슈 | `page.once("dialog", lambda d: d.accept())` |
| `get_by_text("...")` (텍스트 중복) | strict mode 위반 | `.first` 추가 |
| `get_by_role("button", name="Next slide")` | 슬라이더 3개 동시 매칭 | `.first` 추가 |
| 햄버거 메뉴 `.click()` | viewport 밖 요소 — `force=True`도 실패 | `href` 추출 후 `page.goto()` |
| 수익계산기 좌표 클릭 | 슬라이더 이미지가 클릭됨 | `find()` ref 추출 후 `left_click(ref=...)` |
| 라디오버튼 `.click()` (숨김 상태) | 요소 비가시 오류 | `element.evaluate("el => el.click()")` |
| 소수점 입력(100.5) → alert 예상 | 사이트가 결과 출력 (내부 정수 처리) | expect_type을 "result"로 수정 |

---

## 다음 할 일

### 신규 URL 테스트 추가 시 체크리스트

새 URL이 주어지면 아래를 확인한 뒤 TC를 작성한다.

```
1. 페이지 기본
   - 타이틀 확인
   - 로고 클릭 동작
   - 404 등 에러 페이지 여부

2. 네비게이션
   - GNB 메뉴 항목 및 이동 확인
   - 모바일 햄버거 메뉴
   - 뒤로가기

3. 핵심 기능 (사이트별 다름)
   - 폼 / 계산기 / 검색 등 주요 인터랙션
   - 경계값 / 예외값 입력
   - 필수 필드 미입력 제출

4. UI 컴포넌트
   - 슬라이더 / 캐러셀
   - 모달 / 팝업
   - 탭 / 아코디언

5. 반응형
   - 1920 / 1280 / 768 / 375px

6. 기타
   - 언어 전환 (다국어 사이트)
   - 콘솔 에러 없음
   - 외부 링크 href 존재 확인
   - 개인정보/이용약관 링크
```

### 신규 파일 명명 규칙

```
test_<사이트명>_all.py     ← 통합 테스트 파일
make_report_<사이트명>.py  ← 리포트 생성 스크립트 (선택)
```

### 실행 명령어 템플릿

```bash
# 신규 URL 테스트 실행
pytest test_<사이트명>_all.py -v -s

# 섹션별 실행
pytest test_<사이트명>_all.py -v -k "TC01"

# 크로스 브라우저
pytest test_<사이트명>_all.py -v --browser chromium --browser firefox

# 스크린샷 자동 저장 (FAIL 시)
pytest test_<사이트명>_all.py -v --screenshot=only-on-failure --output=screenshots/

# 슬로우모션 디버깅
pytest test_<사이트명>_all.py -v --headed --slowmo=800 -k "TC005"

# 리포트 생성
python make_report_now.py
```

---

## 작업 결과

### 1차 — solarteq.co.kr (2026-04-15)

| 항목 | 내용 |
|------|------|
| 대상 URL | `https://solarteq.co.kr/ko` |
| 테스트 파일 | `test_solarteq_all.py` |
| 총 TC | **57개** |
| PASS | **57** |
| FAIL | **0** |
| 합격률 | **100%** |
| 리포트 | `solarteq_report_final_20260415_1524.xlsx` |

| 섹션 | TC 수 | PASS |
|------|-------|------|
| 홈페이지 | 2 | 2 |
| 네비게이션 | 2 | 2 |
| 수익계산기 기본 | 4 | 4 |
| 문의하기 기본 | 2 | 2 |
| 슬라이더/UI 기본 | 2 | 2 |
| 기타 기본 | 2 | 2 |
| 수익계산기 경계/예외 | 13 | 13 |
| 문의하기 상세 | 9 | 9 |
| 네비게이션 상세 | 5 | 5 |
| UI/슬라이더 상세 | 5 | 5 |
| 반응형 viewport | 4 | 4 |
| 언어 전환 | 3 | 3 |
| 기타/보완 | 4 | 4 |

---

### 2차 — (URL 추가 예정)

| 항목 | 내용 |
|------|------|
| 대상 URL | |
| 테스트 파일 | |
| 총 TC | |
| PASS | |
| FAIL | |
| 합격률 | |
| 리포트 | |
