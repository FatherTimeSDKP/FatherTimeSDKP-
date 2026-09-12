"""
X.AI Grok SDK Client Module
Provides a reusable interface for interacting with Grok models using the official X.AI SDK
"""

import os
from typing import Optional
from xai_sdk import Client
from xai_sdk.chat import user, assistant


class GrokClient:
    """Client for X.AI Grok API using the official SDK"""
    
    def __init__(self, api_key: Optional[str] = None, api_host: str = "api.x.ai"):
        """
        Initialize the Grok client
        
        Args:
            api_key: X.AI API key. If None, reads from XAI_API_KEY environment variable
            api_host: API host URL (default: api.x.ai)
        """
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "X.AI API key not provided. Set XAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = Client(api_key=self.api_key, api_host=api_host)
        self.model = "grok-4.6"
    
    def query(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Send a query to Grok model
        
        Args:
            prompt: The prompt/question to send
            model: Optional model override (defaults to grok-4.6)
        
        Returns:
            Response text from Grok
        """
        model = model or self.model
        
        try:
            chat = self.client.chat.create(model=model)
            chat.append(user(prompt))
            response = chat.sample()
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_code(self, code: str, task: str = "Fix bugs and explain") -> str:
        """
        Analyze code with Grok
        
        Args:
            code: Code to analyze
            task: Analysis task description
        
        Returns:
            Analysis result as string
        """
        prompt = f"{task}:\n\n```\n{code}\n```"
        return self.query(prompt)
    
    def explain_sdkp(self, concept: str) -> str:
        """
        Ask Grok to explain SDKP framework concepts
        
        Args:
            concept: SDKP concept to explain
        
        Returns:
            Explanation as string
        """
        prompt = f"Explain this concept from the SDKP Framework: {concept}"
        return self.query(prompt)
    
    def vibration_field_analysis(self, equation: str) -> str:
        """
        Analyze vibration field equations with Grok
        
        Args:
            equation: Vibration field equation to analyze
        
        Returns:
            Analysis result as string
        """
        prompt = f"""Analyze this vibration field equation from the context of SDKP framework:

{equation}

Provide:
1. Mathematical explanation
2. Physical interpretation
3. Relationship to Scale-Density-Kinematic Principle
4. Potential applications"""
        return self.query(prompt)


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = GrokClient()
    
    # Example 1: Fix a buggy function
    print("=== Code Analysis ===")
    buggy_code = "function median(a){a.sort();return a[a.length/2]}"
    result = client.analyze_code(buggy_code, "Fix this function and explain the bug")
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Ask about SDKP
    print("=== SDKP Concept Query ===")
    result = client.explain_sdkp("Scale-Density-Kinematic Principle")
    print(result)
