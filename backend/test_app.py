"""
Electronics Lab Inventory - LIMS Backend
Basic test suite for API endpoints
"""

import pytest
import json
from app import create_app

@pytest.fixture
def app():
    """
    Create and configure a test app instance
    """
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """
    Create a test client for the Flask application
    """
    return app.test_client()

class TestHealthEndpoint:
    """
    Test cases for the health check endpoint
    """
    
    def test_health_check_success(self, client):
        """
        Test that health check endpoint returns success
        """
        response = client.get('/health')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert data['service'] == 'Electronics Lab Inventory LIMS'

class TestLoginEndpoint:
    """
    Test cases for the login endpoint
    """
    
    def test_login_success(self, client):
        """
        Test successful login with valid credentials
        """
        login_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'Login successful'
        assert 'user' in data
        assert 'token' in data
    
    def test_login_missing_credentials(self, client):
        """
        Test login failure with missing credentials
        """
        login_data = {
            'username': 'testuser'
            # Missing password
        }
        
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Username and password required' in data['error']
    
    def test_login_empty_request(self, client):
        """
        Test login failure with empty request body
        """
        response = client.post('/login',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400

class TestComponentsEndpoint:
    """
    Test cases for the components endpoint
    """
    
    def test_get_components_success(self, client):
        """
        Test successful retrieval of components
        """
        response = client.get('/components')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'components' in data
        assert 'total_count' in data
        assert 'low_stock_count' in data
        
        # Check that we have some dummy components
        assert len(data['components']) > 0
        
        # Check component structure
        component = data['components'][0]
        required_fields = ['id', 'name', 'part_number', 'category', 
                          'quantity', 'location', 'unit_price', 'low_threshold']
        
        for field in required_fields:
            assert field in component

class TestErrorHandling:
    """
    Test cases for error handling
    """
    
    def test_404_not_found(self, client):
        """
        Test 404 error handling for non-existent endpoints
        """
        response = client.get('/nonexistent-endpoint')
        
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Endpoint not found'

# Run tests with: python -m pytest test_app.py -v