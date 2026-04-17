import os
import requests

# GitHub Issues 자동 등록 설정
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")   # GitHub Actions에서 자동 주입됨
GITHUB_REPO  = os.getenv("GITHUB_REPO")    # 예: "jaewani82/test_issues"

def pytest_runtest_logreport(report):
    """
    pytest 훅: 각 TC 실행 결과가 나올 때마다 호출된다.
    call 단계에서 FAILED면 GitHub Issue를 자동 등록한다.
    """
    # 'call' 단계만 처리 (setup/teardown 제외), 로컬 실행 시엔 토큰 없으므로 무시
    if report.when != "call" or not report.failed:
        return
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return

    # TC 이름에서 사이트명과 번호 추출 (예: test_solarteq_all.py::test_TC005_calculator)
    tc_name = report.nodeid.split("::")[-1]

    # 실패 원인 (트레이스백) 추출
    longrepr = str(report.longrepr) if report.longrepr else "원인 불명"
    # 너무 길면 잘라냄 (GitHub Issues 본문 제한 대비)
    if len(longrepr) > 2000:
        longrepr = longrepr[:2000] + "\n...(생략)"

    # 이슈 제목과 본문 구성
    title = f"[FAIL] {tc_name}"
    body  = (
        f"## 실패한 테스트\n`{report.nodeid}`\n\n"
        f"## 실패 원인\n```\n{longrepr}\n```\n\n"
        f"---\n*pytest E2E 자동 등록*"
    )

    # GitHub Issues API 호출
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    payload = {
        "title": title,
        "body": body,
        "labels": ["bug", "automated-test"],  # 이슈에 라벨 자동 부착
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    if resp.status_code == 201:
        print(f"\n[이슈 등록 완료] {resp.json().get('html_url')}")
    else:
        print(f"\n[이슈 등록 실패] {resp.status_code} {resp.text}")
