#!/usr/bin/env python3
"""
Test script to demonstrate the AI Agents System functionality.
"""

import os
import sys
from master_agent import MasterAgent
from utils import setup_logging

def test_ai_agents_system():
    """Test the AI agents system with sample requests."""
    
    # Setup logging
    setup_logging()
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.")
        return False
    
    print("🔧 Testing AI Agents System")
    print("=" * 50)
    
    try:
        # Initialize master agent
        master_agent = MasterAgent()
        print("✅ Master agent initialized")
        
        # Test requests
        test_requests = [
            "Write a Python function to calculate fibonacci numbers",
            "Explain quantum computing in simple terms",
            "Create a creative story about a robot learning to paint",
            "Help me solve this math problem: What is 15% of 240?"
        ]
        
        for i, request in enumerate(test_requests, 1):
            print(f"\n🔹 Test {i}: {request}")
            print("-" * 40)
            
            try:
                response = master_agent.process_request(request)
                print(f"📤 Response: {response[:200]}...")
                print("✅ Test completed successfully")
            except Exception as e:
                print(f"❌ Test failed: {e}")
        
        # Show storage stats
        print(f"\n📊 Final Storage Stats:")
        stats = master_agent.agent_storage.get_storage_stats()
        print(f"   Total Agents Created: {stats['total_agents']}")
        for agent_type, count in stats.get('agents_by_type', {}).items():
            print(f"   - {agent_type}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_agents_system()
    sys.exit(0 if success else 1)