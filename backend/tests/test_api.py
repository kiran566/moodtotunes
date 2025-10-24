import json
from app import create_app

app = create_app()
client = app.test_client()

def test_analyze_route():
    res = client.post('/api/analyze', json={"text": "I feel awesome!"})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "sentiment" in data
    assert "songs" in data
