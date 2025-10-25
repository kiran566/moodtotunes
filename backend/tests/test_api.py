import json
from app import create_app
from models.user import db, User

# Setup a test app
app = create_app()
# Use an in-memory database for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# Set a known test JWT secret
app.config['JWT_SECRET_KEY'] = 'test-secret-key' 
client = app.test_client()

def get_auth_token():
    """Helper function to register, login, and get a token."""
    with app.app_context():
        db.create_all()
        
        # 1. Register a user
        client.post('/api/auth/register', json={
            "username": "pytest_user",
            "password": "pytest_password"
        })
        
        # 2. Login
        res = client.post('/api/auth/login', json={
            "username": "pytest_user",
            "password": "pytest_password"
        })
        
        data = json.loads(res.data)
        return data['access_token']

def test_analyze_route():
    # 1. Get a valid token
    token = get_auth_token()
    auth_header = {'Authorization': f'Bearer {token}'}

    # 2. Test the analyze route with the token
    res = client.post('/api/analyze', 
                      json={"text": "I feel awesome!", "language": "tamil"},
                      headers=auth_header)
    
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "sentiment" in data
    assert "songs" in data
    assert data['sentiment'] == 'POSITIVE' # Model should detect this