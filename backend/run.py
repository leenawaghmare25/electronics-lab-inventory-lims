#!/usr/bin/env python3
"""
Electronics Lab Inventory - LIMS Backend
Development server runner script
"""

import os
import sys
from app import app

def main():
    """
    Main function to run the Flask development server
    """
    print("=" * 60)
    print("🔬 Electronics Lab Inventory - LIMS Backend")
    print("=" * 60)
    print(f"🚀 Starting development server...")
    print(f"📍 Server will be available at: http://localhost:5000")
    print(f"📊 Health check endpoint: http://localhost:5000/health")
    print(f"🔐 Login endpoint: POST http://localhost:5000/login")
    print(f"📦 Components endpoint: GET http://localhost:5000/components")
    print("=" * 60)
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Run the Flask development server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 Server stopped by user")
        print("=" * 60)
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()