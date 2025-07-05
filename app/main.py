from fastapi import FastAPI, Request, Header, HTTPException
from starlette.responses import JSONResponse
import hmac, hashlib, yaml, os
from tools.review import analyze_and_comment
from tools.github_api import create_check_run
from tools.github_auth import get_installation_token
from metrics.logger import initialize_logs
initialize_logs()


app = FastAPI()

# Load config
with open("config/github_app.yaml") as f:
    cfg = yaml.safe_load(f)

WEBHOOK_SECRET = cfg["webhook_secret"].encode()

@app.post("/webhook")
async def webhook_listener(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None)
):
    print("\n🚀 Webhook triggered")
    print(f"🔔 GitHub Event Type: {x_github_event}")

    # Signature verification
    body = await request.body()
    signature = 'sha256=' + hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, x_hub_signature_256 or ""):
        print("❌ Signature mismatch")
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    print(f"📦 Payload Keys: {list(payload.keys())}")

    if x_github_event != "pull_request":
        print(f"⚠️ Ignored event type: {x_github_event}")
        return JSONResponse(content={"status": f"Ignored event: {x_github_event}"})

    action = payload.get("action")
    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})

    pr_number = pr.get("number")
    repo_fullname = repo.get("full_name")
    commit_sha = pr.get("head", {}).get("sha", "")

    print(f"📁 Repo: {repo_fullname}")
    print(f"🔢 PR #: {pr_number}")
    print(f"⚙️ Action: {action}")

    if action in ["opened", "reopened", "synchronize"]:
        print("✅ Valid PR event — processing...")
        try:
            github_token = get_installation_token()
            if not github_token:
                raise ValueError("❌ Failed to retrieve GitHub App token.")

            print(f"🔐 GitHub Token starts with: {github_token[:8]}...")

            results = await analyze_and_comment(repo_fullname, pr_number, github_token)

            summary = f"AutoReviewBot detected {len(results)} issue(s)."
            has_critical = any(v.get("severity") == "critical" for v in results)

            conclusion = "failure" if has_critical else "success"
            output_title = "Code Review: Issues Found" if has_critical else "Code Review: Passed"
            output_summary = "\n".join(
                [f"- [Line {v['line']}] `{v['message']}`" for v in results[:10]]
            ) or "No violations found."

            owner, repo = repo_fullname.split("/")
            status_code, _ = create_check_run(owner, repo, commit_sha,
                                              conclusion, output_title, output_summary, github_token)
            print(f"✅ Check Run posted: {status_code}")
            return JSONResponse(content={"status": "review complete"})

        except Exception as e:
            print(f"❌ Error: {e}")
            return JSONResponse(status_code=500, content={"error": str(e)})

    else:
        print(f"⚠️ PR action '{action}' not handled")
        return JSONResponse(content={"status": "ignored action"})

