"""Utility for tracking OpenAI API costs."""
from typing import Dict
from datetime import datetime

class CostTracker:
    """Track costs of OpenAI API calls."""
    
    # Cost per 1K tokens in USD (as of December 2023)
    COST_PER_1K_TOKENS = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-0613": {"input": 0.03, "output": 0.06},
        "gpt-4o": {"input": 0.03, "output": 0.06},  # Using gpt-4 rates
        "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
        "o1-2024-12-17": {"input": 0.015, "output": 0.06}
    }
    
    def __init__(self):
        """Initialize the cost tracker."""
        self.total_cost = 0.0
        self.calls_history = []
    
    def add_call(self, model: str, input_tokens: int, output_tokens: int, operation: str):
        """
        Add an API call to the tracker.
        
        Args:
            model: The model used (e.g., "gpt-4")
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            operation: Type of operation (e.g., "generate", "revise", etc.)
        """
        # Get costs for the model
        model_costs = self.COST_PER_1K_TOKENS.get(model, self.COST_PER_1K_TOKENS["gpt-4"])
        
        # Calculate costs
        input_cost = (input_tokens / 1000) * model_costs["input"]
        output_cost = (output_tokens / 1000) * model_costs["output"]
        total_cost = input_cost + output_cost
        
        # Update total
        self.total_cost += total_cost
        
        # Record call
        self.calls_history.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": total_cost
        })
    
    def get_total_cost(self) -> float:
        """Get the total cost of all API calls."""
        return self.total_cost
    
    def get_cost_breakdown(self) -> Dict:
        """Get a breakdown of costs by operation."""
        breakdown = {}
        for call in self.calls_history:
            op = call["operation"]
            if op not in breakdown:
                breakdown[op] = 0.0
            breakdown[op] += call["cost"]
        return breakdown
    
    def print_summary(self):
        """Print a summary of all costs."""
        print("\nOpenAI API Cost Summary:")
        print(f"Total Cost: ${self.total_cost:.4f}")
        print("\nBreakdown by operation:")
        for op, cost in self.get_cost_breakdown().items():
            print(f"- {op}: ${cost:.4f}")
        print(f"\nTotal API calls: {len(self.calls_history)}")

# Global cost tracker instance
cost_tracker = CostTracker() 