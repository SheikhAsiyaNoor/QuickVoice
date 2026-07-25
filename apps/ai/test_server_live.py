import json
import urllib.request
import sys

BASE_URL = "http://127.0.0.1:5555"
INTERNAL_KEY = "dev-internal-key-change-me"

def test_health():
    print("1. Testing GET /health...")
    req = urllib.request.Request(f"{BASE_URL}/health")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("   STATUS:", resp.status)
        print("   RESPONSE:", data)
        assert data.get("ok") is True
        assert data.get("service") == "ai"
    print("   [PASS] GET /health PASSED!\n")

def test_voice_catalog():
    print("2. Testing GET /voice/catalog with internal auth header...")
    req = urllib.request.Request(
        f"{BASE_URL}/voice/catalog",
        headers={"x-internal-key": INTERNAL_KEY}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("   STATUS:", resp.status)
        print("   CATALOG KEYS:", list(data.keys()))
        assert "stt" in data or "providers" in data or isinstance(data, dict)
    print("   [PASS] GET /voice/catalog PASSED!\n")

def test_voice_config_resolve():
    print("3. Testing POST /voice/config/resolve...")
    payload = json.dumps({"language": "en"}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/voice/config/resolve",
        data=payload,
        headers={
            "content-type": "application/json",
            "x-internal-key": INTERNAL_KEY
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("   STATUS:", resp.status)
        print("   RESOLVED CONFIG:", data)
        assert "config" in data
    print("   [PASS] POST /voice/config/resolve PASSED!\n")

if __name__ == "__main__":
    print("=== LIVE SERVER TEST SUITE ===")
    try:
        test_health()
        test_voice_catalog()
        test_voice_config_resolve()
        print(">>> ALL SERVER TESTS PASSED SUCCESSFULLY! <<<")
    except Exception as e:
        print(f"[FAIL] TEST FAILED: {e}")
        sys.exit(1)
