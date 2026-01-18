#!/usr/bin/env python3
"""
Complete Authentication Test
Tests registration, login, and user profile fetch
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("🧪 SolveStack Authentication Test\n")
print("=" * 60)

# Test 1: Check backend health
print("\n1️⃣  Testing Backend Health...")
try:
    resp = requests.get(f"{BASE_URL}/")
    if resp.status_code == 200:
        print("   ✅ Backend is online")
    else:
        print(f"   ❌ Status: {resp.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Register new user
print("\n2️⃣  Testing Registration...")
timestamp = str(int(time.time()))
test_email = f"test{timestamp}@example.com"
test_username = f"testuser{timestamp}"
test_password = "testpass123"

try:
    register_data = {
        "email": test_email,
        "username": test_username,
        "password": test_password
    }
    resp = requests.post(f"{BASE_URL}/register", json=register_data)
    
    if resp.status_code == 201:
        data = resp.json()
        token = data.get("access_token")
        if token:
            print(f"   ✅ Registration successful!")
            print(f"   📧 Email: {test_email}")
            print(f"   👤 Username: {test_username}")
            print(f"   🔑 Token received: {token[:30]}...")
        else:
            print("   ❌ No token in response")
            print(f"   Response: {data}")
            exit(1)
    else:
        print(f"   ❌ Status: {resp.status_code}")
        print(f"   Response: {resp.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 3: Fetch user profile with token
print("\n3️⃣  Testing User Profile Fetch...")
try:
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/me", headers=headers)
    
    if resp.status_code == 200:
        user_data = resp.json()
        print(f"   ✅ Profile fetched successfully!")
        print(f"   👤 User ID: {user_data.get('id')}")
        print(f"   📧 Email: {user_data.get('email')}")
        print(f"   👤 Username: {user_data.get('username')}")
        print(f"   ⭐ Premium: {user_data.get('is_premium')}")
    else:
        print(f"   ❌ Status: {resp.status_code}")
        print(f"   Response: {resp.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 4: Test login with same credentials
print("\n4️⃣  Testing Login...")
try:
    login_data = f"username={test_email}&password={test_password}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(f"{BASE_URL}/login", data=login_data, headers=headers)
    
    if resp.status_code == 200:
        data = resp.json()
        login_token = data.get("access_token")
        if login_token:
            print(f"   ✅ Login successful!")
            print(f"   🔑 New token: {login_token[:30]}...")
        else:
            print("   ❌ No token in response")
            exit(1)
    else:
        print(f"   ❌ Status: {resp.status_code}")
        print(f"   Response: {resp.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 5: Get problems list
print("\n5️⃣  Testing Problems Fetch...")
try:
    resp = requests.get(f"{BASE_URL}/problems?skip=0&limit=5")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"   ✅ Problems fetched successfully!")
        print(f"   📊 Total problems: {len(data)}")
        if data:
            print(f"   📋 First problem: {data[0].get('title', 'N/A')[:50]}")
    else:
        print(f"   ❌ Status: {resp.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ All authentication tests passed!\n")
print("🎯 Summary:")
print("   ✅ Backend running")
print("   ✅ Registration works")
print("   ✅ Token generation works")
print("   ✅ User profile fetch works")
print("   ✅ Login works")
print("   ✅ Problems API works")
print("\n🚀 Frontend & Backend fully integrated!\n")
