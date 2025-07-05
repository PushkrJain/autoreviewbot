import httpx
import tempfile
import os
from base64 import b64decode
from tools.linter import analyze_java_code
from tools.github_api import create_check_run
from metrics.logger import log_violation

GITHUB_API = "https://api.github.com"

def get_check_run_conclusion(violations):
    severities = [v.get("severity", "low") for v in violations]
    if "high" in severities:
        return "failure", "Critical violations found"
    elif "medium" in severities:
        return "neutral", "Medium-severity violations found"
    else:
        return "success", "No major issues found"

async def analyze_and_comment(repo_fullname: str, pr_number: int, github_token: str):
    print(f"🔍 Analyzing PR #{pr_number} in repo {repo_fullname}")

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    files_url = f"{GITHUB_API}/repos/{repo_fullname}/pulls/{pr_number}/files"
    pr_url = f"{GITHUB_API}/repos/{repo_fullname}/pulls/{pr_number}"

    async with httpx.AsyncClient() as client:
        files_resp = await client.get(files_url, headers=headers)
        pr_resp = await client.get(pr_url, headers=headers)

    if files_resp.status_code != 200 or pr_resp.status_code != 200:
        print("❌ Failed to fetch PR data")
        return []

    changed_files = files_resp.json()
    pr_data = pr_resp.json()
    head_sha = pr_data["head"]["sha"]
    ref = pr_data["head"]["ref"]
    owner, repo = repo_fullname.split("/")

    java_files = [f for f in changed_files if f["filename"].endswith(".java")]
    if not java_files:
        print("⚠️ No Java files in this PR")
        return []

    all_violations = []
    comments = []

    for file in java_files:
        filename = file["filename"]
        contents_url = f"{GITHUB_API}/repos/{repo_fullname}/contents/{filename}?ref={ref}"

        async with httpx.AsyncClient() as client:
            contents_resp = await client.get(contents_url, headers=headers)

        if contents_resp.status_code != 200:
            print(f"❌ Failed to fetch file content: {filename}")
            continue

        try:
            content_data = contents_resp.json()
            file_content = b64decode(content_data["content"]).decode("utf-8")
        except Exception as e:
            print(f"❌ Error decoding content for {filename}: {e}")
            continue

        print(f"📄 Fetched {filename} with {len(file_content.splitlines())} lines")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as tmp_file:
            tmp_file.write(file_content.encode())
            tmp_path = tmp_file.name

        violations = analyze_java_code(tmp_path)
        os.unlink(tmp_path)

        all_violations.extend(violations)

        for v in violations:
            severity = v.get("severity", "low")
            log_violation({
                "repo": repo_fullname,
                "pr_number": pr_number,
                "filename": filename,
                "line": v["line"],
                "rule_id": v["rule_id"],
                "severity": severity,
                "message": v["suggestion"]
            })

            comments.append({
                "path": filename,
                "line": v["line"],
                "side": "RIGHT",
                "body": f"⚠️ Rule `{v['rule_id']}` violated: {v['suggestion']}\n> `{v['code']}`"
            })

    # ✅ Post GitHub PR review comment
    review_url = f"{GITHUB_API}/repos/{repo_fullname}/pulls/{pr_number}/reviews"
    review_body = {
        "body": "🤖 **AutoReviewBot** analysis complete.",
        "event": "COMMENT",
        "comments": comments
    }

    async with httpx.AsyncClient() as client:
        review_resp = await client.post(review_url, headers=headers, json=review_body)
        print(f"🔁 Review status: {review_resp.status_code}")

    # ✅ Post Check Run
    conclusion, summary = get_check_run_conclusion(all_violations)
    status_code, _ = create_check_run(owner, repo, head_sha, conclusion,
                                      "AutoReviewBot Check", summary, github_token)
    print(f"🛡️ Check Run posted with conclusion: {conclusion} — Status Code: {status_code}")

    return all_violations

