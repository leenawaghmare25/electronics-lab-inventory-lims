#!/usr/bin/env python3
"""
Electronics Lab Inventory - LIMS
Setup script for development environment
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """
    Run a shell command and handle errors
    """
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """
    Check if Python version is compatible
    """
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_virtual_environment():
    """
    Create and activate virtual environment
    """
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print("📁 Virtual environment already exists")
        return True
    
    # Create virtual environment
    if not run_command(f"python -m venv {venv_path}", "Creating virtual environment"):
        return False
    
    return True

def install_dependencies():
    """
    Install Python dependencies
    """
    backend_path = os.path.join("backend", "requirements.txt")
    
    if not os.path.exists(backend_path):
        print(f"❌ Requirements file not found: {backend_path}")
        return False
    
    # Determine pip command based on OS
    if platform.system() == "Windows":
        pip_command = "venv\\Scripts\\pip"
    else:
        pip_command = "venv/bin/pip"
    
    # Install dependencies
    command = f"{pip_command} install -r {backend_path}"
    return run_command(command, "Installing Python dependencies")

def create_env_file():
    """
    Create .env file from template if it doesn't exist
    """
    env_file = os.path.join("backend", ".env")
    env_example = os.path.join("backend", ".env.example")
    
    if os.path.exists(env_file):
        print("📁 .env file already exists")
        return True
    
    if not os.path.exists(env_example):
        print("⚠️  .env.example file not found, skipping .env creation")
        return True
    
    try:
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ Created .env file from template")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    """
    Main setup function
    """
    print("=" * 60)
    print("🔬 Electronics Lab Inventory - LIMS Setup")
    print("=" * 60)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"📍 Working directory: {project_dir}")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("❌ Failed to setup virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Run the backend server:")
    print("   cd backend")
    print("   python app.py")
    
    print("\n3. Open your browser and visit:")
    print("   Backend API: http://localhost:5000")
    print("   Frontend: Open frontend/index.html")
    
    print("\n4. Test the API endpoints:")
    print("   Health check: GET http://localhost:5000/health")
    print("   Components: GET http://localhost:5000/components")
    print("   Login: POST http://localhost:5000/login")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()