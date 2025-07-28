"""
Utility functions for the AI Agents System.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any


def setup_logging(log_level: str = "INFO", log_file: str = "agents_system.log"):
    """
    Setup logging configuration for the system.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Log file path
    """
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    
    # Setup console handler (only for WARNING and above to keep terminal clean)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        handlers=[file_handler, console_handler]
    )
    
    # Reduce noise from external libraries
    logging.getLogger('google').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)


def validate_environment():
    """
    Validate that required environment variables are set.
    
    Returns:
        True if environment is valid, False otherwise
    """
    required_vars = ["GEMINI_API_KEY"]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    return True


def format_agent_info(agent: Dict[str, Any]) -> str:
    """
    Format agent information for display.
    
    Args:
        agent: Agent dictionary
        
    Returns:
        Formatted string representation of agent
    """
    name = agent.get("name", "Unknown")
    description = agent.get("description", "No description")
    task_type = agent.get("task_type", "general")
    created_by = agent.get("created_by", "Unknown")
    
    return f"""
🤖 Agent: {name}
📋 Type: {task_type}
📝 Description: {description}
👤 Created by: {created_by}
"""


def print_system_stats(agent_storage):
    """
    Print system statistics.
    
    Args:
        agent_storage: AgentStorage instance
    """
    stats = agent_storage.get_storage_stats()
    
    print("\n📊 System Statistics:")
    print(f"   Total Agents: {stats['total_agents']}")
    
    if stats['agents_by_type']:
        print("   Agents by Type:")
        for agent_type, count in stats['agents_by_type'].items():
            print(f"     - {agent_type}: {count}")
    
    print(f"   Storage File: {stats['storage_file']}")
    print(f"   File Exists: {stats['file_exists']}")


def get_timestamp() -> str:
    """
    Get current timestamp as string.
    
    Returns:
        Current timestamp in ISO format
    """
    return datetime.now().isoformat()


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def sanitize_agent_name(name: str) -> str:
    """
    Sanitize agent name to ensure it's valid.
    
    Args:
        name: Original agent name
        
    Returns:
        Sanitized agent name
    """
    # Remove special characters and spaces
    import re
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '', name)
    
    # Ensure it starts with a letter
    if sanitized and not sanitized[0].isalpha():
        sanitized = 'Agent' + sanitized
    
    # Ensure minimum length
    if len(sanitized) < 3:
        sanitized = 'Agent' + sanitized
    
    return sanitized or 'DefaultAgent'


def print_welcome_banner():
    """Print welcome banner for the system."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🤖 AI Agents System                      ║
║              Dynamic Agent Creation & Delegation             ║
╚══════════════════════════════════════════════════════════════╝

Features:
  🎯 Master agent with intelligent task delegation
  🔍 Similarity search for existing agents
  ⚡ Dynamic agent creation when needed
  💾 Persistent agent storage
  📊 Hierarchical task management

Commands:
  • Enter any request to start delegation
  • Type 'quit', 'exit', or 'q' to exit
  • Use Ctrl+C for emergency exit

"""
    print(banner)


def handle_error(error: Exception, context: str = "") -> str:
    """
    Handle and format errors for user display.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
        
    Returns:
        User-friendly error message
    """
    error_msg = str(error)
    
    # Log the full error
    logging.error(f"Error in {context}: {error_msg}")
    
    # Return user-friendly message
    if "API" in error_msg or "key" in error_msg.lower():
        return "❌ API connection issue. Please check your GEMINI_API_KEY."
    elif "timeout" in error_msg.lower():
        return "⏰ Request timed out. Please try again."
    elif "json" in error_msg.lower():
        return "🔧 Data parsing error. The system will retry automatically."
    else:
        return f"❌ An error occurred: {error_msg}"
