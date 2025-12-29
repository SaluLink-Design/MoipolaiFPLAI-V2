#!/usr/bin/env python3
"""
Quick test script to verify the app can start and respond
Run this locally before deploying to Railway
"""
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask imported")
        import requests
        print("✓ Requests imported")
        import pydantic
        print("✓ Pydantic imported")
        import numpy
        print("✓ NumPy imported")
        import scipy
        print("✓ SciPy imported")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_creation():
    """Test that the Flask app can be created"""
    print("\nTesting app creation...")
    try:
        from app import create_app
        app = create_app()
        print("✓ Flask app created successfully")
        print(f"✓ Registered routes: {[str(rule) for rule in app.url_map.iter_rules()]}")
        return True, app
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_health_endpoint(app):
    """Test the health endpoint"""
    print("\nTesting health endpoint...")
    try:
        with app.test_client() as client:
            response = client.get('/health')
            print(f"✓ /health responded with status {response.status_code}")
            print(f"  Response: {response.get_json()}")
            
            response = client.get('/api/health')
            print(f"✓ /api/health responded with status {response.status_code}")
            print(f"  Response: {response.get_json()}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("FPL AI Backend - Pre-deployment Tests")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        sys.exit(1)
    
    # Test app creation
    success, app = test_app_creation()
    if not success:
        print("\n❌ App creation failed!")
        sys.exit(1)
    
    # Test health endpoint
    if not test_health_endpoint(app):
        print("\n❌ Health endpoint test failed!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! App is ready for deployment.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Fix Railway deployment'")
    print("3. git push")
    print("4. Deploy to Railway")

if __name__ == "__main__":
    main()

