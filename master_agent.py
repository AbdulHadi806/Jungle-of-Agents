"""
Master Agent implementation.
Handles user requests, delegates tasks to specialized agents, and manages agent creation.
"""

import json
import logging
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
import os

from base_agent import BaseAgent
from agent_storage import AgentStorage
from similarity_search import SimilaritySearch


class MasterAgent(BaseAgent):
    """
    Master agent that coordinates task delegation and agent management.
    """
    
    def __init__(self):
        """Initialize the master agent with storage and similarity search."""
        super().__init__(
            name="MasterAgent",
            description="Master coordinator agent that delegates tasks to specialized agents"
        )
        
        self.agent_storage = AgentStorage()
        self.similarity_search = SimilaritySearch()
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        logging.info("Master agent initialized")
    
    def process_request(self, request: str) -> str:
        """
        Process user request by analyzing it and delegating to appropriate agents.
        
        Args:
            request: The user's input request
            
        Returns:
            Response from the delegated agent or master agent
        """
        logging.info(f"Processing user request: {request[:100]}...")
        
        try:
            # Analyze the request to determine task requirements
            task_analysis = self._analyze_task(request)
            
            # Find or create appropriate agent
            agent = self._find_or_create_agent(task_analysis)
            
            # Delegate task to the agent
            if agent:
                print(f"🔄 Delegating to agent: {agent['name']}")
                response = self._delegate_task(agent, request, task_analysis)
            else:
                # Handle the task directly if no specialized agent is needed
                response = self._handle_directly(request)
            
            return response
            
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return f"I encountered an error while processing your request: {e}"
    
    def _analyze_task(self, user_prompt: str) -> Dict[str, Any]:
        """
        Analyze the user prompt to understand task requirements.
        
        Args:
            user_prompt: The user's input
            
        Returns:
            Dictionary containing task analysis
        """
        analysis_prompt = f"""
        Analyze this user request and determine what type of specialized agent would be best suited to handle it.
        
        User Request: {user_prompt}
        
        Please provide a JSON response with:
        1. task_type: The category/type of task (e.g., "writing", "coding", "research", "math", "creative", "analysis")
        2. agent_description: A brief description of what kind of agent would handle this (e.g., "Python programming assistant", "Creative writing helper")
        3. complexity: "simple" or "complex" 
        4. requires_delegation: true if this needs a specialized agent, false if master can handle directly
        
        Respond only with valid JSON.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=analysis_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                analysis = json.loads(response.text)
                logging.info(f"Task analysis: {analysis}")
                return analysis
            else:
                raise ValueError("Empty response from analysis")
                
        except Exception as e:
            logging.error(f"Error analyzing task: {e}")
            # Fallback analysis
            return {
                "task_type": "general",
                "agent_description": "General purpose assistant",
                "complexity": "simple",
                "requires_delegation": False
            }
    
    def _find_or_create_agent(self, task_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find existing agent or create new one based on task analysis.
        
        Args:
            task_analysis: Analysis of the task requirements
            
        Returns:
            Agent dictionary or None if master should handle directly
        """
        if not task_analysis.get("requires_delegation", False):
            return None
        
        agent_description = task_analysis.get("agent_description", "")
        print(agent_description, ' ::::::::agent_description')
        # Search for existing similar agent
        existing_agent = self.similarity_search.find_similar_agent(
            agent_description, 
            self.agent_storage.list_agents()
        )
        
        if existing_agent:
            print(f"📋 Found existing agent: {existing_agent['name']}")
            logging.info(f"Using existing agent: {existing_agent['name']}")
            return existing_agent
        
        # Create new agent if none found
        print(f"🔨 Creating new specialized agent...")
        new_agent = self._create_new_agent(task_analysis)
        
        if new_agent:
            self.agent_storage.save_agent(new_agent)
            print(f"✅ Created and saved new agent: {new_agent['name']}")
            logging.info(f"Created new agent: {new_agent['name']}")
        
        return new_agent
    
    def _create_new_agent(self, task_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new specialized agent based on task analysis.
        
        Args:
            task_analysis: Analysis of the task requirements
            
        Returns:
            New agent dictionary
        """
        agent_creation_prompt = f"""
        Create a specialized AI agent based on this task analysis:
        
        Task Type: {task_analysis.get('task_type', 'general')}
        Agent Description: {task_analysis.get('agent_description', 'General assistant')}
        Complexity: {task_analysis.get('complexity', 'simple')}
        
        Please provide a JSON response with:
        1. name: A concise name for the agent (e.g., "PythonCodingAgent", "CreativeWritingAgent")
        2. description: Detailed description of the agent's capabilities and specialization
        3. system_prompt: A comprehensive system prompt that defines the agent's role, expertise, and behavior
        4. task_type: The type of tasks this agent specializes in
        
        Make the agent highly specialized and expert in its domain.
        Respond only with valid JSON.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=agent_creation_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                agent_data = json.loads(response.text)
                agent_data['created_by'] = 'MasterAgent'
                return agent_data
            else:
                raise ValueError("Empty response from agent creation")
                
        except Exception as e:
            logging.error(f"Error creating new agent: {e}")
            # Fallback agent creation
            return {
                "name": f"{task_analysis.get('task_type', 'General')}Agent",
                "description": task_analysis.get('agent_description', 'General purpose assistant'),
                "system_prompt": f"You are a helpful assistant specializing in {task_analysis.get('task_type', 'general tasks')}.",
                "task_type": task_analysis.get('task_type', 'general'),
                "created_by": "MasterAgent"
            }
    
    def _delegate_task(self, agent: Dict[str, Any], user_prompt: str, task_analysis: Dict[str, Any]) -> str:
        """
        Delegate task to a specialized agent.
        
        Args:
            agent: The agent to delegate to
            user_prompt: Original user prompt
            task_analysis: Analysis of the task
            
        Returns:
            Response from the delegated agent
        """
        delegation_prompt = f"""
        {agent.get('system_prompt', '')}
        
        You are {agent.get('name', 'SpecializedAgent')} and you specialize in: {agent.get('description', '')}
        
        Please handle this user request with your specialized expertise:
        
        User Request: {user_prompt}
        
        Provide a helpful, detailed, and expert response based on your specialization.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=delegation_prompt
            )
            
            if response.text:
                return response.text
            else:
                return "The specialized agent was unable to provide a response."
                
        except Exception as e:
            logging.error(f"Error delegating to agent {agent.get('name')}: {e}")
            return f"Error occurred while delegating to {agent.get('name')}: {e}"
    
    def _handle_directly(self, user_prompt: str) -> str:
        """
        Handle simple requests directly without delegation.
        
        Args:
            user_prompt: The user's request
            
        Returns:
            Direct response from master agent
        """
        direct_prompt = f"""
        You are the Master Agent of an AI agents system. Handle this request directly:
        
        User Request: {user_prompt}
        
        Provide a helpful and comprehensive response.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=direct_prompt
            )
            
            if response.text:
                return response.text
            else:
                return "I'm unable to process your request at the moment."
                
        except Exception as e:
            logging.error(f"Error handling request directly: {e}")
            return f"I encountered an error: {e}"
