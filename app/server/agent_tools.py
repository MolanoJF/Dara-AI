"""
Agent tools for the multimodal ADK server.
Contains all function tools that the agent can use.
"""

import logging
import time
from typing import Optional

# Import Mem0 for long-term memory
from mem0 import MemoryClient

# Import config components
from config.config import logger, get_order_status, MEM0_API_KEY    

# Initialize Mem0 client
mem0_client = MemoryClient(api_key=MEM0_API_KEY)


def order_status_tool(order_id: str):
    """Get the current status and details of an order.

    Args:
        order_id: The order ID to look up.

    Returns:
        Dictionary containing order status details
    """
    return get_order_status(order_id)


def search_memory(query: str, user_id: Optional[str] = None):
    """Search for relevant information in long-term memory."""
    try:
        # Check if Mem0 client is available
        if mem0_client is None:
            return {
                "status": "disabled",
                "memories": [],
                "count": 0,
                "message": "Memory features are disabled - MEM0_API_KEY not configured"
            }
        
        # Use user_id if provided, otherwise use a default
        USER_ID = user_id if user_id is not None else "default_user"
        
        # Search memories using Mem0 with higher threshold for relevance
        results = mem0_client.search(
            query=query,
            user_id=USER_ID,
            limit=5,
            threshold=0.7,  # Higher threshold for more relevant results
            output_format="v1.1"  # Use latest output format
        )
        
        # Format and return the results
        if results and len(results) > 0:
            memories = [memory["memory"] for memory in results]
            return {
                "status": "success",
                "memories": memories,
                "count": len(memories)
            }
        else:
            return {
                "status": "no_results",
                "memories": [],
                "count": 0
            }
    except Exception as e:
        logger.error(f"Error searching memory: {e}")
        return {"error": str(e), "memories": []}


def save_memory(text: str, user_id: Optional[str] = None, metadata: Optional[dict] = None):
    """Save important information to long-term memory.
    
    This function should only be used to save RELEVANT information such as:
    - Personal preferences (food, hobbies, family members)
    - Important details (allergies, health conditions, preferences)
    - Significant events or plans
    - User characteristics or traits
    
    DO NOT save every conversation or casual chat.
    """
    try:
        # Check if Mem0 client is available
        if mem0_client is None:
            return {
                "success": False,
                "error": "Memory features are disabled - MEM0_API_KEY not configured"
            }
        
        # Use user_id if provided, otherwise use a default
        USER_ID = user_id if user_id is not None else "default_user"
        
        # Add timestamp and source metadata
        enhanced_metadata = {
            "timestamp": int(time.time()),
            "source": "agent_tool",
            "type": "user_preference"
        }
        
        # Merge with provided metadata
        if metadata:
            enhanced_metadata.update(metadata)
        
        # Save memory using Mem0 with enhanced metadata
        result = mem0_client.add(
            messages=[{"role": "user", "content": text}],
            user_id=USER_ID,
            metadata=enhanced_metadata
        )
        
        logger.info(f"Saved important memory for {USER_ID}: {text[:50]}...")
        
        return {
            "success": True,
            "result": result,
            "user_id": USER_ID,
            "saved_text": text,
            "message": "Important information saved to memory"
        }
    except Exception as e:
        logger.error(f"Error saving memory: {e}")
        return {"success": False, "error": str(e)}





# Export all tools for easy importing
__all__ = [
    "order_status_tool",
    "search_memory", 
    "save_memory"
]
