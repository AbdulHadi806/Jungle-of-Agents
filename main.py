#!/usr/bin/env python3
"""
Main entry point for the AI Agents System.
Provides a terminal-based interface for interacting with the master agent.
"""

import logging
import os
from dotenv import load_dotenv
import sys
from master_agent import MasterAgent
from utils import setup_logging

load_dotenv()

os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
    

"""
Meet Jungle of Agents, create a jungle of Agents
"""
def main():
    """Main function to run the AI Agents System."""
    # Setup logging
    setup_logging()
    
    print("=" * 60)
    print("🤖 AI Agents System - Terminal Interface")
    print("=" * 60)
    print("Welcome! You can interact with the master agent.")
    print("The master agent will delegate tasks to specialized agents.")
    print("Type 'quit', 'exit', or 'q' to exit the system.")
    print("-" * 60)
    
    # Initialize master agent
    try:
        master_agent = MasterAgent()
        print("✅ Master agent initialized successfully!")
        print("-" * 60)
    except Exception as e:
        print(f"❌ Failed to initialize master agent: {e}")
        sys.exit(1)
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("\n🗣️  You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye! Thanks for using the AI Agents System.")
                break
            
            if not user_input:
                print("Please enter a valid prompt.")
                continue
            
            print("\n🤖 Processing your request...")
            print("-" * 40)
            
            # Process the request through master agent
            response = master_agent.process_request(user_input)
            
            print(f"\n✨ Master Agent: {response}")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using the AI Agents System.")
            break
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            print(f"\n❌ Error: {e}")
            print("Please try again with a different request.")


if __name__ == "__main__":
    main()
