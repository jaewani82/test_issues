import os
import requests

# GitHub Actions에서 자동 주입되는 환경변수
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO  = os.getenv("GITHUB_REPO")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def find_open_issue(tc_name: str) -> int | None:
    """
    제목에 tc_name이 포함된 열린 이슈를 검색해 issue number를 반환한다.
    없으면 None 반환.
    PASS 시 기존 이슈를 닫기 위해 사용한다.
    """
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return None

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    # state=open: 열린 이슈만 검색
    resp = requests.get(url, headers=HEADERS, params={"state": "open"}, timeout=10)
    if resp.status_code != 200:
        return None

    for issue in resp.json():
        # [FAIL] tc_name 형태의 제목으로 매칭
        if f"[FAIL] {tc_name}" in issue.get("title", ""):
            return issue["number"]
    return None


def close_issue(issue_number: int, tc_name: str):
    """
    issue_number에 해당하는 이슈를 PASS 댓글과 함께 자동으로 닫는다.
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}"

    # 댓글로 PASS 기록 남기기
    comment_url = f"{url}/comments"
    requests.post(
        comment_url,
        headers=HEADERS,
        json={"body": f"✅ **PASS** — `{tc_name}` 재실행에서 통과. 자동으로 이슈를 닫습니다."},
        timeout=10,
    )

    # 이슈 Close
    resp = requests.patch(url, headers=HEADERS, json={"state": "closed"}, timeout=10)
    if resp.status_code == 200:
        print(f"\n[이슈 자동 Close] #{issue_number} {tc_name}")
    else:
        print(f"\n[이슈 Close 실패] {resp.status_code} {resp.text}")


def open_issue(tc_name: str, report):
    """
    FAIL한 TC를 GitHub Issues에 자동 등록한다.
    동일 TC 이슈가 이미 열려있으면 중복 등록하지 않는다.
    """
    # 이미 열린 이슈가 있으면 중복 등록 방지
    if find_open_issue(tc_name):
        print(f"\n[이슈 중복 방지] {tc_name} 이슈가 이미 존재함")
        return

    longrepr = str(report.longrepr) if report.longrepr else "원인 불명"
    if len(longrepr) > 2000:
        longrepr = longrepr[:2000] + "\n...(생략)"

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    payload = {
        "title": f"[FAIL] {tc_name}",
        "body": (
            f"## 실패한 테스트\n`{report.nodeid}`\n\n"
            f"## 실패 원인\n```\n{longrepr}\n```\n\n"
            f"---\n*pytest E2E 자동 등록*"
        ),
        "labels": ["bug"],  # automated-test 라벨은 기본 생성 안 되므로 bug만 사용
    }

    resp = requests.post(url, headers=HEADERS, json=payload, timeout=10)
    if resp.status_code == 201:
        print(f"\n[이슈 등록 완료] {resp.json().get('html_url')}")
    else:
        print(f"\n[이슈 등록 실패] {resp.status_code} {resp.text}")


def pytest_runtest_logreport(report):
    """
    pytest 훅: 각 TC 실행 결과가 나올 때마다 호출된다.

    FAIL → 이슈 자동 등록 (중복 방지)
    PASS → 기존 열린 이슈 자동 Close
    """
    # call 단계만 처리 (setup/teardown 제외)
    if report.when != "call":
        return
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return

    # TC 이름 추출 (예: test_TC005_calculator_modal_open[chromium])
    tc_name = report.nodeid.split("::")[-1]

    if report.failed:
        open_issue(tc_name, report)

    elif report.passed:
        # PASS 시 동일 TC의 열린 이슈가 있으면 자동 Close
        issue_number = find_open_issue(tc_name)
        if issue_number:
            close_issue(issue_number, tc_name)
