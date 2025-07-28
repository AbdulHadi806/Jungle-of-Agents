#!/usr/bin/env python3
"""
Example usage scenarios for the AI Agents System.
This file demonstrates various ways to interact with the system.
"""

import os
from master_agent import MasterAgent
from utils import setup_logging, print_system_stats

def example_programming_tasks():
    """Examples of programming-related requests."""
    print("🖥️  Programming Task Examples")
    print("-" * 40)
    
    programming_requests = [
        "Write a Python function to sort a list of dictionaries by a specific key",
        "Create a JavaScript function that validates email addresses",
        "Show me how to implement a binary search algorithm in Python",
        "Write a SQL query to find the top 5 customers by total orders",
        "Create a REST API endpoint in Python using Flask"
    ]
    
    return programming_requests

def example_creative_tasks():
    """Examples of creative writing requests."""
    print("🎨 Creative Writing Examples")
    print("-" * 40)
    
    creative_requests = [
        "Write a short poem about artificial intelligence",
        "Create a story about a time traveler who visits ancient Rome",
        "Write a product description for a smart home device",
        "Create dialogue for a scene between two detectives",
        "Write a blog post introduction about sustainable living"
    ]
    
    return creative_requests

def example_educational_tasks():
    """Examples of educational and explanatory requests."""
    print("📚 Educational Examples")
    print("-" * 40)
    
    educational_requests = [
        "Explain how photosynthesis works in simple terms",
        "What is the difference between machine learning and deep learning?",
        "Explain the concept of compound interest with examples",
        "How does blockchain technology work?",
        "What are the main causes of climate change?"
    ]
    
    return educational_requests

def example_analysis_tasks():
    """Examples of analytical and research requests."""
    print("🔍 Analysis Examples")
    print("-" * 40)
    
    analysis_requests = [
        "Analyze the pros and cons of remote work",
        "Compare different programming paradigms",
        "What are the key factors to consider when choosing a database?",
        "Analyze the impact of social media on modern communication",
        "Compare renewable energy sources and their efficiency"
    ]
    
    return analysis_requests

def example_math_tasks():
    """Examples of mathematical problem-solving requests."""
    print("🧮 Mathematics Examples")
    print("-" * 40)
    
    math_requests = [
        "Solve this quadratic equation: x² + 5x + 6 = 0",
        "Calculate the compound interest on $1000 at 5% for 3 years",
        "What is the area of a triangle with sides 3, 4, and 5?",
        "Convert 150 kilometers to miles",
        "Find the derivative of f(x) = 3x² + 2x + 1"
    ]
    
    return math_requests

def run_interactive_examples():
    """Run examples interactively with user choice."""
    
    # Setup logging
    setup_logging()
    
    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not set")
        print("Please set your API key first:")
        print("export GEMINI_API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize master agent
        print("🤖 Initializing AI Agents System...")
        master_agent = MasterAgent()
        print("✅ System ready!")
        
        # Get all example categories
        example_categories = {
            "1": ("Programming", example_programming_tasks),
            "2": ("Creative Writing", example_creative_tasks),
            "3": ("Educational", example_educational_tasks),
            "4": ("Analysis", example_analysis_tasks),
            "5": ("Mathematics", example_math_tasks)
        }
        
        print("\n📋 Available Example Categories:")
        for key, (name, _) in example_categories.items():
            print(f"   {key}. {name}")
        print("   0. Run all examples")
        print("   q. Quit")
        
        while True:
            choice = input("\n🔢 Choose a category (0-5, q to quit): ").strip()
            
            if choice.lower() == 'q':
                break
            
            if choice == "0":
                # Run all examples
                print("\n🚀 Running all examples...")
                for category_name, get_examples in example_categories.values():
                    print(f"\n{'='*50}")
                    print(f"Testing {category_name} Examples")
                    print(f"{'='*50}")
                    examples = get_examples()
                    
                    for i, request in enumerate(examples[:2], 1):  # Run first 2 from each category
                        print(f"\n📝 Example {i}: {request}")
                        print("-" * 60)
                        try:
                            response = master_agent.process_request(request)
                            print(f"🤖 Response: {response[:300]}...")
                        except Exception as e:
                            print(f"❌ Error: {e}")
                
                break
            
            elif choice in example_categories:
                category_name, get_examples = example_categories[choice]
                examples = get_examples()
                
                print(f"\n📋 {category_name} Examples:")
                for i, example in enumerate(examples, 1):
                    print(f"   {i}. {example}")
                
                example_choice = input(f"\nChoose an example (1-{len(examples)}): ").strip()
                
                try:
                    idx = int(example_choice) - 1
                    if 0 <= idx < len(examples):
                        request = examples[idx]
                        print(f"\n🔄 Processing: {request}")
                        print("-" * 60)
                        
                        response = master_agent.process_request(request)
                        print(f"\n🤖 Response:\n{response}")
                    else:
                        print("❌ Invalid example number")
                        
                except (ValueError, IndexError):
                    print("❌ Invalid input")
                except Exception as e:
                    print(f"❌ Error processing request: {e}")
            
            else:
                print("❌ Invalid choice")
        
        # Show final stats
        print(f"\n📊 Final Statistics:")
        print_system_stats(master_agent.agent_storage)
        
    except Exception as e:
        print(f"❌ System error: {e}")

def batch_test_examples():
    """Run a batch test of different example types."""
    
    print("🧪 Running Batch Test Examples")
    print("=" * 50)
    
    # Setup
    setup_logging()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not set")
        return
    
    try:
        master_agent = MasterAgent()
        
        # Test one example from each category
        test_requests = [
            "Write a Python function to calculate factorial",
            "Write a haiku about technology",
            "Explain what artificial intelligence is",
            "Compare the advantages of Python vs JavaScript",
            "Calculate 25% of 80"
        ]
        
        categories = ["Programming", "Creative", "Educational", "Analysis", "Math"]
        
        for i, (request, category) in enumerate(zip(test_requests, categories), 1):
            print(f"\n🔍 Test {i} ({category}): {request}")
            print("-" * 50)
            
            try:
                response = master_agent.process_request(request)
                print(f"✅ Success: {response[:200]}...")
            except Exception as e:
                print(f"❌ Failed: {e}")
        
        # Show agent creation summary
        stats = master_agent.agent_storage.get_storage_stats()
        print(f"\n📈 Test Results:")
        print(f"   Total Agents Created: {stats['total_agents']}")
        for agent_type, count in stats.get('agents_by_type', {}).items():
            print(f"   - {agent_type}: {count} agent(s)")
        
    except Exception as e:
        print(f"❌ Batch test failed: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        batch_test_examples()
    else:
        run_interactive_examples()