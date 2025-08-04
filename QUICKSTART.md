# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup Environment
```bash
# Run the setup script
python setup.py

# Or on Windows, double-click:
setup.bat
```

### Step 2: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Run the Backend
```bash
cd backend
python app.py
```

## 🧪 Test the API

### Health Check
```bash
curl http://localhost:5000/health
```

### Get Components
```bash
curl http://localhost:5000/components
```

### Login (Dummy)
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

## 🌐 Access Points

- **Backend API**: http://localhost:5000
- **Frontend**: Open `frontend/index.html` in browser
- **API Documentation**: Available in README.md

## 🔧 Development

### Run Tests
```bash
cd backend
python -m pytest test_app.py -v
```

### Code Formatting
```bash
cd backend
black *.py
flake8 *.py
```

## 📁 Key Files

- `backend/app.py` - Main Flask application
- `backend/models.py` - Database models
- `backend/config.py` - Configuration settings
- `backend/requirements.txt` - Python dependencies
- `frontend/index.html` - Frontend placeholder

## 🆘 Troubleshooting

### Python Not Found
- Install Python 3.8+ from https://python.org
- Make sure Python is in your PATH

### Module Not Found
- Activate virtual environment first
- Run `pip install -r backend/requirements.txt`

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

## 📚 Next Steps

1. Implement database connection
2. Add user authentication
3. Build React frontend
4. Add more API endpoints
5. Write comprehensive tests