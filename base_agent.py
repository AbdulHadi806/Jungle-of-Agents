"""
Base Agent class.
Provides common functionality for all agents in the system.
"""

import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            description: Agent description
        """
        self.name = name
        self.description = description
        self.created_at = None
        self.last_used = None
        
        logging.info(f"Initialized agent: {name}")
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.
        
        Returns:
            Dictionary containing agent information
        """
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "last_used": self.last_used,
            "type": self.__class__.__name__
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert agent to dictionary for storage.
        
        Returns:
            Agent as dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "last_used": self.last_used,
            "type": self.__class__.__name__
        }
    
    @abstractmethod
    def process_request(self, request: str) -> str:
        """
        Process a request. Must be implemented by subclasses.
        
        Args:
            request: The request to process
            
        Returns:
            Response string
        """
        pass


class SpecializedAgent(BaseAgent):
    """
    A specialized agent created dynamically by the master agent.
    """
    
    def __init__(self, name: str, description: str, system_prompt: str, task_type: str):
        """
        Initialize specialized agent.
        
        Args:
            name: Agent name
            description: Agent description
            system_prompt: System prompt defining agent behavior
            task_type: Type of tasks this agent handles
        """
        super().__init__(name, description)
        self.system_prompt = system_prompt
        self.task_type = task_type
    
    def process_request(self, request: str) -> str:
        """
        Process request using the agent's specialization.
        
        Args:
            request: The request to process
            
        Returns:
            Response from the specialized agent
        """
        # This would typically use the AI model with the system prompt
        # For now, return a placeholder response
        return f"[{self.name}] Processing: {request}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert specialized agent to dictionary.
        
        Returns:
            Agent as dictionary including specialized fields
        """
        base_dict = super().to_dict()
        base_dict.update({
            "system_prompt": self.system_prompt,
            "task_type": self.task_type
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, agent_dict: Dict[str, Any]) -> 'SpecializedAgent':
        """
        Create specialized agent from dictionary.
        
        Args:
            agent_dict: Dictionary containing agent data
            
        Returns:
            SpecializedAgent instance
        """
        agent = cls(
            name=agent_dict.get("name", "UnknownAgent"),
            description=agent_dict.get("description", ""),
            system_prompt=agent_dict.get("system_prompt", ""),
            task_type=agent_dict.get("task_type", "general")
        )
        
        agent.created_at = agent_dict.get("created_at")
        agent.last_used = agent_dict.get("last_used")
        
        return agent
