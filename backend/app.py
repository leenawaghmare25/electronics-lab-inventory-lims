"""
Electronics Lab Inventory - LIMS Backend
Main Flask application entry point
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """
    Application factory pattern for creating Flask app instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['DEBUG'] = True
    
    # Enable CORS for frontend communication
    CORS(app)
    
    # Register routes
    register_routes(app)
    
    return app

def register_routes(app):
    """
    Register all application routes
    """

    @app.route('/', methods=['GET'])
    def home():
        """
        Root endpoint providing a styled HTML welcome page
        """
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Electronics Lab Inventory - LIMS API</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }
                
                .container {
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                    padding: 3rem;
                    max-width: 800px;
                    width: 100%;
                    text-align: center;
                }
                
                .logo {
                    font-size: 4rem;
                    margin-bottom: 1rem;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                
                h1 {
                    color: #333;
                    margin-bottom: 1rem;
                    font-size: 2.5rem;
                    font-weight: 700;
                }
                
                .subtitle {
                    color: #666;
                    font-size: 1.2rem;
                    margin-bottom: 2rem;
                    line-height: 1.6;
                }
                
                .api-section {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 2rem;
                    margin: 2rem 0;
                    text-align: left;
                }
                
                .api-section h2 {
                    color: #333;
                    margin-bottom: 1.5rem;
                    font-size: 1.5rem;
                    text-align: center;
                }
                
                .endpoints {
                    list-style: none;
                    padding: 0;
                }
                
                .endpoints li {
                    background: white;
                    margin: 1rem 0;
                    padding: 1rem 1.5rem;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    transition: transform 0.2s ease;
                }
                
                .endpoints li:hover {
                    transform: translateX(5px);
                }
                
                .endpoint-method {
                    display: inline-block;
                    background: #667eea;
                    color: white;
                    padding: 0.3rem 0.8rem;
                    border-radius: 4px;
                    font-size: 0.8rem;
                    font-weight: bold;
                    margin-right: 1rem;
                    min-width: 60px;
                    text-align: center;
                }
                
                .endpoint-method.post {
                    background: #28a745;
                }
                
                .endpoint-path {
                    font-family: 'Courier New', monospace;
                    font-weight: bold;
                    color: #333;
                    margin-right: 1rem;
                }
                
                .endpoint-desc {
                    color: #666;
                    font-style: italic;
                }
                
                .github-link {
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    padding: 1rem 2rem;
                    border-radius: 50px;
                    font-weight: bold;
                    margin-top: 2rem;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }
                
                .github-link:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                }
                
                .status-badge {
                    display: inline-block;
                    background: #28a745;
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    margin-bottom: 1rem;
                }
                
                .footer {
                    margin-top: 2rem;
                    padding-top: 2rem;
                    border-top: 1px solid #eee;
                    color: #999;
                    font-size: 0.9rem;
                }
                
                @media (max-width: 768px) {
                    .container {
                        padding: 2rem;
                        margin: 1rem;
                    }
                    
                    h1 {
                        font-size: 2rem;
                    }
                    
                    .logo {
                        font-size: 3rem;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">🔬⚡</div>
                <h1>Electronics Lab Inventory – LIMS API</h1>
                <div class="status-badge">🟢 API Online</div>
                
                <p class="subtitle">
                    A comprehensive Laboratory Information Management System API designed to streamline 
                    electronics component inventory management. This RESTful API provides endpoints for 
                    authentication, component tracking, and inventory management.
                </p>
                
                <div class="api-section">
                    <h2>📡 Available API Endpoints</h2>
                    <ul class="endpoints">
                        <li>
                            <span class="endpoint-method">GET</span>
                            <span class="endpoint-path">/health</span>
                            <span class="endpoint-desc">System health check and status monitoring</span>
                        </li>
                        <li>
                            <span class="endpoint-method post">POST</span>
                            <span class="endpoint-path">/login</span>
                            <span class="endpoint-desc">User authentication and token generation</span>
                        </li>
                        <li>
                            <span class="endpoint-method">GET</span>
                            <span class="endpoint-path">/components</span>
                            <span class="endpoint-desc">Retrieve electronics components inventory</span>
                        </li>
                    </ul>
                </div>
                
                <div class="api-section">
                    <h2>🚀 Quick Start</h2>
                    <p style="margin-bottom: 1rem; color: #666;">Test the API endpoints:</p>
                    <div style="background: #2d3748; color: #e2e8f0; padding: 1rem; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.9rem; text-align: left;">
                        <div style="margin-bottom: 0.5rem;"># Health Check</div>
                        <div style="color: #68d391;">curl http://localhost:5000/health</div>
                        <br>
                        <div style="margin-bottom: 0.5rem;"># Get Components</div>
                        <div style="color: #68d391;">curl http://localhost:5000/components</div>
                        <br>
                        <div style="margin-bottom: 0.5rem;"># Login (POST)</div>
                        <div style="color: #68d391;">curl -X POST http://localhost:5000/login \\<br>
                        &nbsp;&nbsp;-H "Content-Type: application/json" \\<br>
                        &nbsp;&nbsp;-d '{"username": "admin", "password": "password"}'</div>
                    </div>
                </div>
                
                <a href="https://github.com/your-username/electronics-lab-inventory-lims" class="github-link" target="_blank">
                    📚 View on GitHub
                </a>
                
                <div class="footer">
                    <p>Electronics Lab Inventory LIMS v0.1.0 | Built with Flask & Python</p>
                    <p>For API documentation and support, visit our GitHub repository</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint for monitoring
        """
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'Electronics Lab Inventory LIMS'
        }), 200

    @app.route('/login', methods=['POST'])
    def login():
        """
        User authentication endpoint
        TODO: Implement actual authentication logic
        """
        try:
            data = request.get_json()
            
            # Dummy validation - replace with real authentication
            if not data or 'username' not in data or 'password' not in data:
                return jsonify({
                    'error': 'Username and password required'
                }), 400
            
            # Dummy response - replace with JWT token generation
            response_data = {
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': 1,
                    'username': data.get('username'),
                    'role': 'admin'
                },
                'token': 'dummy-jwt-token-replace-with-real-implementation'
            }
            
            logger.info(f"Login attempt for user: {data.get('username')}")
            return jsonify(response_data), 200
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return jsonify({
                'error': 'Internal server error'
            }), 500

    @app.route('/components', methods=['GET'])
    def get_components():
        """
        Retrieve all components from inventory
        TODO: Connect to actual database
        """
        try:
            # Dummy data - replace with database queries
            dummy_components = [
                {
                    'id': 1,
                    'name': 'Arduino Uno R3',
                    'part_number': 'ARD-UNO-R3',
                    'category': 'Microcontrollers',
                    'quantity': 15,
                    'location': 'Shelf A1',
                    'unit_price': 25.99,
                    'low_threshold': 5
                },
                {
                    'id': 2,
                    'name': 'Resistor 220Ω',
                    'part_number': 'RES-220-1/4W',
                    'category': 'Passive Components',
                    'quantity': 100,
                    'location': 'Drawer B2',
                    'unit_price': 0.05,
                    'low_threshold': 20
                },
                {
                    'id': 3,
                    'name': 'LED Red 5mm',
                    'part_number': 'LED-RED-5MM',
                    'category': 'LEDs',
                    'quantity': 3,
                    'location': 'Drawer C1',
                    'unit_price': 0.15,
                    'low_threshold': 10
                }
            ]
            
            # Add low stock warnings
            for component in dummy_components:
                component['low_stock'] = component['quantity'] <= component['low_threshold']
            
            response_data = {
                'success': True,
                'components': dummy_components,
                'total_count': len(dummy_components),
                'low_stock_count': sum(1 for c in dummy_components if c['low_stock'])
            }
            
            logger.info(f"Retrieved {len(dummy_components)} components")
            return jsonify(response_data), 200
            
        except Exception as e:
            logger.error(f"Components retrieval error: {str(e)}")
            return jsonify({
                'error': 'Internal server error'
            }), 500

    @app.errorhandler(404)
    def not_found(error):
        """
        Handle 404 errors
        """
        return jsonify({
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """
        Handle 500 errors
        """
        return jsonify({
            'error': 'Internal server error'
        }), 500

# Create app instance
app = create_app()

if __name__ == '__main__':
    logger.info("Starting Electronics Lab Inventory LIMS Backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)
