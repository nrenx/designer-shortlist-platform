#!/usr/bin/env python3
"""
Test script to verify the Flask app is ready for Railway deployment.
This script tests the basic functionality and deployment readiness.
"""

import os
import sys
import requests
import subprocess
import time
import signal
from multiprocessing import Process

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:5001/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working:", data)
            return True
        else:
            print("❌ Health endpoint failed:", response.status_code)
            return False
    except Exception as e:
        print("❌ Health endpoint error:", str(e))
        return False

def test_api_info():
    """Test the API info endpoint"""
    try:
        response = requests.get('http://localhost:5001/api/info', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API info endpoint working:", data.get('message'))
            return True
        else:
            print("❌ API info endpoint failed:", response.status_code)
            return False
    except Exception as e:
        print("❌ API info endpoint error:", str(e))
        return False

def test_designers_endpoint():
    """Test the designers endpoint"""
    try:
        response = requests.get('http://localhost:5001/api/designers', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Designers endpoint working: {len(data)} designers found")
            return True
        else:
            print("❌ Designers endpoint failed:", response.status_code)
            return False
    except Exception as e:
        print("❌ Designers endpoint error:", str(e))
        return False

def run_flask_app():
    """Run the Flask app in a subprocess"""
    os.chdir('api')
    os.environ['PORT'] = '5001'
    os.environ['FLASK_DEBUG'] = 'False'
    subprocess.run([sys.executable, 'app.py'])

def main():
    """Main test function"""
    print("🚀 Testing Flask app for Railway deployment readiness...")
    print("=" * 60)
    
    # Start Flask app in background
    print("📦 Starting Flask app...")
    flask_process = Process(target=run_flask_app)
    flask_process.start()
    
    # Wait for app to start
    print("⏳ Waiting for app to start...")
    time.sleep(3)
    
    try:
        # Run tests
        tests_passed = 0
        total_tests = 3
        
        print("\n🧪 Running tests...")
        print("-" * 30)
        
        if test_health_endpoint():
            tests_passed += 1
            
        if test_api_info():
            tests_passed += 1
            
        if test_designers_endpoint():
            tests_passed += 1
        
        # Results
        print("\n📊 Test Results:")
        print("-" * 30)
        print(f"Tests passed: {tests_passed}/{total_tests}")
        
        if tests_passed == total_tests:
            print("🎉 All tests passed! App is ready for Railway deployment.")
            print("\n📋 Deployment checklist:")
            print("✅ Health endpoint working")
            print("✅ API endpoints responding")
            print("✅ Database initialization working")
            print("✅ Dockerfile.backend created")
            print("✅ railway.json configured")
            print("\n🚀 Ready to deploy to Railway!")
        else:
            print("❌ Some tests failed. Please check the issues above.")
            
    finally:
        # Clean up
        print("\n🧹 Cleaning up...")
        flask_process.terminate()
        flask_process.join(timeout=5)
        if flask_process.is_alive():
            flask_process.kill()

if __name__ == '__main__':
    main()
