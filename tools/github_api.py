# tools/github_api.py
import httpx

GITHUB_API_URL = "https://api.github.com"

def create_check_run(owner, repo, commit_sha, conclusion, output_title, output_summary, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/check-runs"
    payload = {
        "name": "AutoReviewBot Quality Gate",
        "head_sha": commit_sha,
        "status": "completed",
        "conclusion": conclusion,
        "output": {
            "title": output_title,
            "summary": output_summary,
        }
    }

    response = httpx.post(url, json=payload, headers=headers)
    print(f"🔁 GitHub Check Run status: {response.status_code}")
    print(f"📩 Check Run response: {response.json()}")
    return response.status_code, response.json()

