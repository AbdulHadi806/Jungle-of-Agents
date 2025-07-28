"""
Similarity Search System.
Implements vector-based similarity search to find the most suitable existing agent.
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional
import re


class SimilaritySearch:
    """
    Performs similarity search to find the best matching agent for a given task.
    Uses simple text-based similarity metrics.
    """
    
    def __init__(self, similarity_threshold: float = 0.09):
        """
        Initialize similarity search.
        
        Args:
            similarity_threshold: Minimum similarity score to consider a match
        """
        self.similarity_threshold = similarity_threshold
        logging.info(f"Similarity search initialized with threshold: {similarity_threshold}")
    
    def find_similar_agent(self, query_description: str, agents: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Find the most similar agent based on description.
        
        Args:
            query_description: Description of the needed agent capabilities
            agents: List of available agents
            
        Returns:
            Most similar agent if similarity exceeds threshold, None otherwise
        """
        if not agents:
            logging.info("No agents available for similarity search")
            return None
        
        best_agent = None
        best_score = 0.09
        
        logging.info(f"Searching for agent similar to: {query_description}")
        
        print(query_description, '::::::query_descriptionquery_description')
        for agent in agents:
            
            # Calculate similarity score
            score = self._calculate_similarity(query_description, agent)
            print(score, ' ::::::score')
            logging.debug(f"Agent '{agent.get('name', 'Unknown')}' similarity score: {score:.3f}")
            
            if score > best_score:
                best_score = score
                best_agent = agent
            print(best_agent, ' ::::::best_agent')
            print(self.similarity_threshold, ' ::::::self.similarity_threshold')
        # Check if best score meets threshold
        if best_score >= self.similarity_threshold and best_agent:
            logging.info(f"Found similar agent: {best_agent.get('name')} (score: {best_score:.3f})")
            return best_agent
        else:
            logging.info(f"No similar agent found (best score: {best_score:.3f}, threshold: {self.similarity_threshold})")
            return None
    
    def _calculate_similarity(self, query: str, agent: Dict[str, Any]) -> float:
        """
        Calculate similarity between query and agent.
        
        Args:
            query: Query description
            agent: Agent dictionary
            
        Returns:
            Similarity score between 0 and 1
        """
        # Combine agent description and task type for comparison
        agent_text = f"{agent.get('description', '')} {agent.get('task_type', '')} {agent.get('name', '')}"
        print(agent_text, ' ::::::agent_text')
        # Use multiple similarity metrics and average them
        scores = [
            self._jaccard_similarity(query, agent_text),
            self._keyword_overlap_similarity(query, agent_text),
            self._cosine_similarity_simple(query, agent_text)
        ]
        
        # Return weighted average
        weights = [0.4, 0.3, 0.3]
        weighted_score = sum(score * weight for score, weight in zip(scores, weights))
        print(weighted_score, ' ::::::weighted_score')
        return min(weighted_score, 1.0)  # Ensure score doesn't exceed 1.0
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate Jaccard similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Jaccard similarity score
        """
        # Normalize and tokenize
        tokens1 = set(self._normalize_text(text1).split())
        tokens2 = set(self._normalize_text(text2).split())
        
        if not tokens1 and not tokens2:
            return 1.0
        if not tokens1 or not tokens2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0.0
    
    def _keyword_overlap_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate keyword overlap similarity.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Keyword overlap score
        """
        # Extract keywords (words longer than 3 characters)
        keywords1 = set(word for word in self._normalize_text(text1).split() if len(word) > 3)
        keywords2 = set(word for word in self._normalize_text(text2).split() if len(word) > 3)
        
        if not keywords1 and not keywords2:
            return 1.0
        if not keywords1 or not keywords2:
            return 0.0
        
        # Calculate overlap
        overlap = len(keywords1.intersection(keywords2))
        max_possible = max(len(keywords1), len(keywords2))
        
        return overlap / max_possible if max_possible > 0 else 0.0
    
    def _cosine_similarity_simple(self, text1: str, text2: str) -> float:
        """
        Calculate simple cosine similarity based on word frequencies.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Cosine similarity score
        """
        # Get word frequency vectors
        words1 = self._normalize_text(text1).split()
        words2 = self._normalize_text(text2).split()
        
        # Create vocabulary
        vocab = list(set(words1 + words2))
        
        if not vocab:
            return 1.0
        
        # Create frequency vectors
        vec1 = np.array([words1.count(word) for word in vocab])
        vec2 = np.array([words2.count(word) for word in vocab])
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison.
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def get_similarity_scores(self, query_description: str, agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Get similarity scores for all agents (for debugging/analysis).
        
        Args:
            query_description: Description of needed capabilities
            agents: List of available agents
            
        Returns:
            List of agents with their similarity scores
        """
        results = []
        
        for agent in agents:
            score = self._calculate_similarity(query_description, agent)
            results.append({
                "agent": agent,
                "similarity_score": score,
                "meets_threshold": score >= self.similarity_threshold
            })
        
        # Sort by similarity score (descending)
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return results
