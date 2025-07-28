"""
Agent Storage System.
Manages persistence and retrieval of AI agents using JSON storage.
"""

import json
import logging
import os
from typing import Dict, List, Any, Optional


class AgentStorage:
    """
    Handles storage and retrieval of AI agents in a JSON file.
    """
    
    def __init__(self, storage_file: str = "agents_storage.json"):
        """
        Initialize agent storage.
        
        Args:
            storage_file: Path to the JSON storage file
        """
        self.storage_file = storage_file
        self._ensure_storage_file()
        logging.info(f"Agent storage initialized with file: {storage_file}")
    
    def _ensure_storage_file(self):
        """Ensure the storage file exists and is properly formatted."""
        if not os.path.exists(self.storage_file):
            # Create empty storage file
            with open(self.storage_file, 'w') as f:
                json.dump({"agents": []}, f, indent=2)
            logging.info(f"Created new storage file: {self.storage_file}")
        else:
            # Validate existing file
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    if "agents" not in data:
                        data["agents"] = []
                        with open(self.storage_file, 'w') as f:
                            json.dump(data, f, indent=2)
            except (json.JSONDecodeError, IOError) as e:
                logging.warning(f"Storage file corrupted, creating new one: {e}")
                with open(self.storage_file, 'w') as f:
                    json.dump({"agents": []}, f, indent=2)
    
    def save_agent(self, agent: Dict[str, Any]) -> bool:
        """
        Save an agent to storage.
        
        Args:
            agent: Agent dictionary containing name, description, etc.
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Load existing agents
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            # Check if agent already exists (by name)
            existing_agent_index = None
            for i, existing_agent in enumerate(data["agents"]):
                if existing_agent.get("name") == agent.get("name"):
                    existing_agent_index = i
                    break
            
            if existing_agent_index is not None:
                # Update existing agent
                data["agents"][existing_agent_index] = agent
                logging.info(f"Updated existing agent: {agent.get('name')}")
            else:
                # Add new agent
                data["agents"].append(agent)
                logging.info(f"Added new agent: {agent.get('name')}")
            
            # Save back to file
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
            
        except Exception as e:
            logging.error(f"Error saving agent {agent.get('name', 'Unknown')}: {e}")
            return False
    
    def get_agent(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an agent by name.
        
        Args:
            agent_name: Name of the agent to retrieve
            
        Returns:
            Agent dictionary if found, None otherwise
        """
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            for agent in data["agents"]:
                if agent.get("name") == agent_name:
                    return agent
            
            return None
            
        except Exception as e:
            logging.error(f"Error retrieving agent {agent_name}: {e}")
            return None
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        Get all stored agents.
        
        Returns:
            List of all agent dictionaries
        """
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            return data.get("agents", [])
            
        except Exception as e:
            logging.error(f"Error listing agents: {e}")
            return []
    
    def delete_agent(self, agent_name: str) -> bool:
        """
        Delete an agent from storage.
        
        Args:
            agent_name: Name of the agent to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            # Find and remove agent
            original_count = len(data["agents"])
            data["agents"] = [agent for agent in data["agents"] 
                            if agent.get("name") != agent_name]
            
            if len(data["agents"]) < original_count:
                # Agent was found and removed
                with open(self.storage_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                logging.info(f"Deleted agent: {agent_name}")
                return True
            else:
                # Agent not found
                logging.warning(f"Agent not found for deletion: {agent_name}")
                return False
            
        except Exception as e:
            logging.error(f"Error deleting agent {agent_name}: {e}")
            return False
    
    def get_agents_by_type(self, task_type: str) -> List[Dict[str, Any]]:
        """
        Get all agents that specialize in a specific task type.
        
        Args:
            task_type: The type of task to filter by
            
        Returns:
            List of agents that match the task type
        """
        try:
            all_agents = self.list_agents()
            matching_agents = [
                agent for agent in all_agents 
                if agent.get("task_type", "").lower() == task_type.lower()
            ]
            
            return matching_agents
            
        except Exception as e:
            logging.error(f"Error getting agents by type {task_type}: {e}")
            return []
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the agent storage.
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            agents = self.list_agents()
            
            # Count agents by type
            type_counts = {}
            for agent in agents:
                task_type = agent.get("task_type", "unknown")
                type_counts[task_type] = type_counts.get(task_type, 0) + 1
            
            return {
                "total_agents": len(agents),
                "agents_by_type": type_counts,
                "storage_file": self.storage_file,
                "file_exists": os.path.exists(self.storage_file)
            }
            
        except Exception as e:
            logging.error(f"Error getting storage stats: {e}")
            return {
                "total_agents": 0,
                "agents_by_type": {},
                "storage_file": self.storage_file,
                "file_exists": False,
                "error": str(e)
            }
