#!/usr/bin/env python3
"""
Setup script for AI Agents System.
"""

import os
import sys

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        ('google.genai', 'google-genai'),
        ('numpy', 'numpy')
    ]
    
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} is installed")
        except ImportError:
            print(f"❌ {package_name} is missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print("\nTo install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_api_key():
    """Check if GEMINI_API_KEY is set."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY environment variable not set")
        print("\nTo set your API key:")
        print("1. Get an API key from https://aistudio.google.com/")
        print("2. Set the environment variable:")
        print("   export GEMINI_API_KEY='your_api_key_here'")
        return False
    
    if not api_key.startswith('AIza'):
        print("⚠️  API key format may be incorrect (should start with 'AIza')")
        return False
    
    print("✅ GEMINI_API_KEY is set")
    return True

def create_storage_structure():
    """Create necessary files and directories."""
    files_to_create = []
    
    # Check if storage file exists
    if not os.path.exists('agents_storage.json'):
        files_to_create.append('agents_storage.json')
    
    if files_to_create:
        print(f"\nCreating storage files: {', '.join(files_to_create)}")
        
        # Create agents storage file
        if 'agents_storage.json' in files_to_create:
            import json
            with open('agents_storage.json', 'w') as f:
                json.dump({"agents": []}, f, indent=2)
            print("✅ Created agents_storage.json")
    else:
        print("✅ All storage files exist")
    
    return True

def main():
    """Main setup function."""
    print("🔧 AI Agents System Setup")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("API Key", check_api_key),
        ("Storage Structure", create_storage_structure)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\nYou can now run the system with:")
        print("   python main.py")
        print("\nOr test it with:")
        print("   python test_system.py")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())