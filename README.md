# Playwright E2E 테스트 자동화 파이프라인

URL 하나를 입력하면 페이지 분석 → TC 도출 → 테스트 실행 → Excel 리포트 생성까지 자동화하는 E2E 테스트 파이프라인.

---

## 기술 스택

| 항목 | 버전 |
|------|------|
| Python | 3.10+ |
| Playwright | 1.58.0 |
| pytest | 9.0.3 |
| pytest-playwright | 0.7.2 |
| openpyxl | 3.1.5 |

---

## 설치

```bash
# 패키지 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install chromium
```

---

## 빠른 시작

```bash
# 전체 테스트 실행
pytest test_solarteq_all.py -v -s

# Excel 리포트 생성 (pytest 재실행 없이 즉시)
python make_report_now.py

# 풀 파이프라인 (pytest 실행 + Excel 생성)
python generate_report.py
```

---

## 주요 명령어

```bash
# 특정 TC만 실행
pytest test_<사이트명>_all.py -v -k "TC005"

# 크로스 브라우저 실행
pytest test_<사이트명>_all.py -v --browser chromium --browser firefox

# 실패 시 스크린샷 자동 저장
pytest test_<사이트명>_all.py -v --screenshot=only-on-failure --output=screenshots/

# 슬로우모션 디버깅 (각 액션마다 800ms 딜레이)
pytest test_<사이트명>_all.py -v --headed --slowmo=800 -k "TC005"
```

---

## 파일 구조

```
.
├── test_solarteq_all.py          # 통합 E2E 테스트 (TC001 ~ TC057, 57개)
├── test_solarteq_quality.py      # 품질 지표 테스트 (성능·접근성·SEO·보안·UX)
├── make_report_now.py            # Excel 리포트 즉시 생성
├── generate_report.py            # 풀 파이프라인 (pytest + Excel)
├── conftest.py                   # pytest 공용 fixture
├── pytest.ini                    # pytest 기본 옵션 (--headed)
├── requirements.txt              # Python 패키지 목록
├── HANDOFF.md                    # 작업 인수인계 및 결과 기록
└── solarteq_report_final_*.xlsx  # 생성된 Excel 리포트
```

---

## 작업 결과 (최신)

### solarteq.co.kr — 2026-04-15

| 항목 | 내용 |
|------|------|
| 대상 URL | `https://solarteq.co.kr/ko` |
| 테스트 파일 | `test_solarteq_all.py` |
| 총 TC | 57개 |
| PASS | **57** |
| FAIL | **0** |
| 합격률 | **100%** |

| 섹션 | TC 범위 | PASS |
|------|---------|------|
| 홈페이지 | TC001–002 | 2 |
| 네비게이션 | TC003–004 | 2 |
| 수익계산기 기본 | TC005–008 | 4 |
| 문의하기 기본 | TC009–010 | 2 |
| 슬라이더/UI 기본 | TC011–012 | 2 |
| 기타 기본 | TC013–014 | 2 |
| 수익계산기 경계/예외 | TC015–027 | 13 |
| 문의하기 상세 | TC028–036 | 9 |
| 네비게이션 상세 | TC037–041 | 5 |
| UI/슬라이더 상세 | TC042–046 | 5 |
| 반응형 viewport | TC047–050 | 4 |
| 언어 전환 | TC051–053 | 3 |
| 기타/보완 | TC054–057 | 4 |

---

## 새 사이트 작업 순서

1. 브라우저로 대상 URL 열기 → 페이지 구조 분석
2. 카테고리별 TC 도출 (홈·네비·폼·모달·반응형·언어·기타)
3. `test_<사이트명>_all.py` 작성 (TC001부터 순번)
4. `pytest test_<사이트명>_all.py -v -s` 실행
5. `make_report_now.py` 수정 후 실행 → Excel 리포트 생성
6. `HANDOFF.md` 결과 섹션 업데이트

### 작업 전 체크리스트

```
1. 페이지 기본     — 타이틀, 로고 클릭, 404 여부
2. 네비게이션      — GNB 메뉴 항목 및 이동, 햄버거 메뉴, 뒤로가기
3. 핵심 기능       — 폼·계산기·검색, 경계값·예외값, 필수 필드 미입력 제출
4. UI 컴포넌트     — 슬라이더·캐러셀, 모달·팝업, 탭·아코디언
5. 반응형          — 1920 / 1280 / 768 / 375px
6. 기타            — 언어 전환, 콘솔 에러 없음, 외부 링크 href, 개인정보·이용약관
```

---

## 알려진 오류 패턴

| 증상 | 원인 | 해결 |
|------|------|------|
| `expect_event("dialog")` 타임아웃 | 이벤트 등록 타이밍 경쟁 | `page.once("dialog", lambda d: d.accept())` 사용 |
| `strict mode violation` | 선택자에 요소 2개 이상 매칭 | `.first` 추가 |
| `element outside viewport` | 햄버거 메뉴 항목이 화면 밖 위치 | `href` 추출 후 `page.goto()` 로 이동 |
| 좌표 클릭이 엉뚱한 요소에 걸림 | 슬라이더 이미지가 앞에서 가림 | `find()` ref 추출 후 `left_click(ref=...)` 사용 |

---

## CI/CD (GitHub Actions)

`.github/workflows/` 디렉터리에 워크플로우 파일이 있습니다.
테스트 PASS 시 관련 GitHub Issue가 자동으로 Close됩니다.
