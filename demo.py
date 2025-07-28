#!/usr/bin/env python3
"""
Demo script for AI Agents System.
Demonstrates the complete workflow of the system.
"""

import json
import os
from master_agent import MasterAgent
from utils import setup_logging, print_system_stats

def demo_system_workflow():
    """Demonstrate the complete AI agents system workflow."""
    
    print("🎬 AI Agents System Demo")
    print("=" * 60)
    print("This demo shows how the master agent creates and delegates")
    print("tasks to specialized agents based on user requests.")
    print("=" * 60)
    
    # Setup
    setup_logging()
    
    # Check API key (will work when user provides valid key)
    api_key_status = "✅ Set" if os.getenv("GEMINI_API_KEY") else "❌ Not Set"
    print(f"API Key Status: {api_key_status}")
    
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  API key not set. Showing system architecture demo...")
        demo_architecture()
        return
    
    try:
        # Initialize the system
        print("\n🚀 Initializing Master Agent...")
        master_agent = MasterAgent()
        print("✅ Master Agent initialized successfully!")
        
        # Demo scenarios
        demo_scenarios = [
            {
                "category": "Programming",
                "request": "Create a Python function to validate email addresses",
                "expected_agent": "PythonCodingAgent or CodingAgent"
            },
            {
                "category": "Creative Writing", 
                "request": "Write a short story about AI becoming self-aware",
                "expected_agent": "CreativeWritingAgent"
            },
            {
                "category": "Mathematics",
                "request": "Solve this equation: 2x + 5 = 17",
                "expected_agent": "MathAgent"
            },
            {
                "category": "Research/Analysis",
                "request": "Explain the benefits and drawbacks of renewable energy",
                "expected_agent": "ResearchAgent or AnalysisAgent"
            }
        ]
        
        print("\n🎯 Running Demo Scenarios...")
        print("-" * 60)
        
        for i, scenario in enumerate(demo_scenarios, 1):
            print(f"\n📋 Scenario {i}: {scenario['category']}")
            print(f"Request: {scenario['request']}")
            print(f"Expected Agent Type: {scenario['expected_agent']}")
            print("-" * 40)
            
            try:
                # Show the delegation process
                print("🔍 Master agent analyzing request...")
                response = master_agent.process_request(scenario['request'])
                
                print(f"📤 Response Preview: {response[:150]}...")
                print("✅ Task completed successfully!")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Show agent reuse demonstration
        print(f"\n♻️  Testing Agent Reuse...")
        print("-" * 40)
        print("Making another programming request to test agent reuse...")
        
        try:
            response = master_agent.process_request("Write a Python function to calculate the area of a circle")
            print("✅ Agent reuse test completed!")
        except Exception as e:
            print(f"❌ Reuse test error: {e}")
        
        # Show final statistics
        print(f"\n📊 Demo Results:")
        print_system_stats(master_agent.agent_storage)
        
        # Show storage file contents
        try:
            with open('agents_storage.json', 'r') as f:
                storage_data = json.load(f)
                agents = storage_data.get('agents', [])
                
                print(f"\n💾 Agent Storage Details:")
                for agent in agents:
                    print(f"   🤖 {agent.get('name', 'Unknown')}")
                    print(f"      Type: {agent.get('task_type', 'Unknown')}")
                    print(f"      Description: {agent.get('description', 'No description')[:60]}...")
                    print()
        except Exception as e:
            print(f"Storage read error: {e}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def demo_architecture():
    """Show system architecture when API key is not available."""
    
    print("\n🏗️  System Architecture Overview")
    print("=" * 50)
    
    print("""
    User Request
         ↓
    ┌─────────────────────────────────────────────────┐
    │                Master Agent                     │
    │  • Analyzes request using Gemini AI            │
    │  • Determines if delegation is needed           │
    │  • Manages agent lifecycle                      │
    └─────────────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────────────┐
    │              Similarity Search                  │
    │  • Searches existing agents                     │  
    │  • Uses Jaccard + Cosine similarity            │
    │  • Threshold-based matching                     │
    └─────────────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────────────┐
    │           Agent Decision Logic                  │
    │                                                 │
    │  Found Similar Agent    │    No Similar Agent   │
    │         ↓              │           ↓            │
    │   Reuse Existing       │    Create New Agent    │
    └─────────────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────────────┐
    │              Agent Storage                      │
    │  • JSON-based persistence                       │
    │  • Automatic file management                    │
    │  • Error recovery and validation                │
    └─────────────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────────────┐
    │             Task Delegation                     │
    │  • Specialized agent processes request          │
    │  • Uses agent's system prompt                   │
    │  • Returns expert response                      │
    └─────────────────────────────────────────────────┘
    """)
    
    print("\n📁 File Structure:")
    files = [
        ("main.py", "Terminal interface and user interaction"),
        ("master_agent.py", "Core orchestration and delegation logic"),
        ("agent_storage.py", "JSON-based agent persistence layer"),
        ("similarity_search.py", "Agent matching algorithms"),
        ("base_agent.py", "Agent base classes and interfaces"),
        ("utils.py", "Logging and utility functions"),
        ("agents_storage.json", "Agent data storage (auto-created)"),
        ("setup.py", "System verification and setup"),
        ("examples.py", "Interactive examples and demos"),
        ("test_system.py", "Automated testing script")
    ]
    
    for filename, description in files:
        status = "✅" if os.path.exists(filename) else "❌"
        print(f"   {status} {filename:<20} - {description}")
    
    print(f"\n🔧 Quick Setup Steps:")
    print("1. Get API key from https://aistudio.google.com/")
    print("2. Set GEMINI_API_KEY environment variable")
    print("3. Run: python setup.py (to verify setup)")
    print("4. Run: python main.py (to start the system)")
    print("5. Run: python examples.py (for interactive examples)")

def show_usage_examples():
    """Show example usage patterns."""
    
    print("\n💡 Usage Examples")
    print("=" * 30)
    
    examples = {
        "Programming": [
            "Write a Python function to reverse a string",
            "Create a REST API endpoint using Flask",
            "Show me how to use decorators in Python"
        ],
        "Creative": [
            "Write a haiku about programming",
            "Create a short story about robots",
            "Write a product description for a smart watch"
        ],
        "Education": [
            "Explain machine learning in simple terms", 
            "What is quantum computing?",
            "How does blockchain work?"
        ],
        "Analysis": [
            "Compare Python vs JavaScript for web development",
            "Analyze the pros and cons of remote work",
            "What are the benefits of cloud computing?"
        ],
        "Mathematics": [
            "Calculate compound interest for $1000 at 5% for 3 years",
            "Solve: 2x + 5 = 15",
            "Find the area of a circle with radius 7"
        ]
    }
    
    for category, category_examples in examples.items():
        print(f"\n📚 {category}:")
        for example in category_examples:
            print(f"   • {example}")

if __name__ == "__main__":
    demo_system_workflow()
    show_usage_examples()