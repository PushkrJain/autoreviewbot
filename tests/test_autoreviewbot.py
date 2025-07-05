import pytest
import json
import hmac
import hashlib
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WEBHOOK_SECRET = b"super_secret_token"  # Same as app config


def generate_signature(payload: dict) -> tuple[str, bytes]:
    body = json.dumps(payload).encode("utf-8")
    signature = 'sha256=' + hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()
    return signature, body


def build_pr_payload(file_name, content, pr_number=1):
    return {
        "action": "synchronize",
        "number": pr_number,
        "repository": {"full_name": "PushkrJain/Stirling-PDF"},
        "pull_request": {
            "number": pr_number,
            "head": {"sha": "mocksha"},
            "base": {"sha": "mockbasesha"},
            "user": {"login": "PushkrJain"},
            "body": "Test PR",
            "title": "Test PR for Rule",
            "url": "https://api.github.com/repos/PushkrJain/Stirling-PDF/pulls/1",
        },
        "sender": {"login": "PushkrJain"}
    }


class DummyResponse:
    def __init__(self, content: str, is_json=False):
        self.status_code = 200
        self._content = content
        self._is_json = is_json

    @property
    def content(self):
        return self._content.encode("utf-8")

    def json(self):
        if self._is_json:
            return [
                {
                    "filename": "src/Test.java",
                    "raw_url": "https://mocked-url/raw/Test.java"
                }
            ]
        return {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.mark.parametrize("rule_id,java_code", [
    ("JAVA-001", 'System.out.println("Test");'),
    ("JAVA-002", 'if (obj == null) {}'),
    ("JAVA-003", 'if (obj != null) {}'),
    ("JAVA-004", 'public class Test implements Serializable {}'),
    ("JAVA-005", 'try {} catch (Exception e) {}'),
    ("JAVA-006", 'List<String> list = new ArrayList<String>();'),
    ("JAVA-007", 'Vector<String> vector = new Vector<>();'),
    ("JAVA-008", 'public Test() {}'),
    ("JAVA-009", 'HashMap<String, String> map = new HashMap<>();'),
    ("JAVA-010", '@Nullable String s = null;'),
    ("JAVA-011", 'public class MyService implements UserService {}'),
    ("JAVA-012", 'public boolean equals(Object o) {}'),
    ("JAVA-013", 'for (int i = 0; i < 10; i++) { list.add(i); }'),
    ("JAVA-014", 'this.items = items;')
])
def test_rule_violation_detection(rule_id, java_code, monkeypatch):
    async def mock_get(self, url, *args, **kwargs):
        if url.endswith("/files"):
            return DummyResponse("ignored", is_json=True)  # For PR file list
        else:
            return DummyResponse(java_code)  # For raw Java code

    monkeypatch.setattr("tools.review.httpx.AsyncClient.get", mock_get)

    payload = build_pr_payload("Test.java", java_code)
    signature, body = generate_signature(payload)

    response = client.post(
        "/webhook",
        data=body,
        headers={
            "X-Hub-Signature-256": signature,
            "X-GitHub-Event": "pull_request",
            "Content-Type": "application/json"
        }
    )

    assert response.status_code == 200


def test_push_event_ignored():
    payload = {
        "ref": "refs/heads/main",
        "repository": {"full_name": "PushkrJain/Stirling-PDF"},
        "pusher": {"name": "PushkrJain"},
    }
    signature, body = generate_signature(payload)

    response = client.post(
        "/webhook",
        data=body,
        headers={
            "X-Hub-Signature-256": signature,
            "X-GitHub-Event": "push",
            "Content-Type": "application/json"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"].startswith("Ignored")

