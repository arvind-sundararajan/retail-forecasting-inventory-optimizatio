```json
{
    "tests/test_data_loader.py": {
        "content": "
import logging
from langchain import MemoryGraph, ToolNode, AgentNode, Graph
from langchain.chat_models import ChatOpenAI
import numpy as np
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_non_stationary_drift_index(data: List[float]) -> float:
    """
    Calculate the non-stationary drift index for a given dataset.

    Args:
    - data (List[float]): The input dataset.

    Returns:
    - float: The non-stationary drift index.
    """
    try:
        # Calculate the mean and standard deviation of the data
        mean = np.mean(data)
        std_dev = np.std(data)
        
        # Calculate the non-stationary drift index
        non_stationary_drift_index = np.abs(mean - std_dev)
        
        logger.info(f'Non-stationary drift index: {non_stationary_drift_index}')
        return non_stationary_drift_index
    except Exception as e:
        logger.error(f'Error calculating non-stationary drift index: {e}')
        return None

def stochastic_regime_switch(data: List[float], threshold: float) -> bool:
    """
    Determine if a stochastic regime switch has occurred.

    Args:
    - data (List[float]): The input dataset.
    - threshold (float): The threshold for the regime switch.

    Returns:
    - bool: True if a regime switch has occurred, False otherwise.
    """
    try:
        # Calculate the mean of the data
        mean = np.mean(data)
        
        # Check if the mean exceeds the threshold
        if mean > threshold:
            logger.info('Stochastic regime switch detected')
            return True
        else:
            logger.info('No stochastic regime switch detected')
            return False
    except Exception as e:
        logger.error(f'Error detecting stochastic regime switch: {e}')
        return False

def create_memory_graph() -> MemoryGraph:
    """
    Create a memory graph with short-term and long-term memory.

    Returns:
    - MemoryGraph: The created memory graph.
    """
    try:
        # Create a memory graph with short-term and long-term memory
        memory = MemoryGraph(short_term=5, long_term_path='vector://chroma')
        logger.info('Memory graph created')
        return memory
    except Exception as e:
        logger.error(f'Error creating memory graph: {e}')
        return None

def create_tool_node() -> ToolNode:
    """
    Create a tool node for calculating the NPV.

    Returns:
    - ToolNode: The created tool node.
    """
    try:
        # Define the NPV function
        def npv(amount: float, years: int, rate: float = 0.07) -> float:
            return amount / ((1 + rate) ** years)
        
        # Create a tool node for the NPV function
        calc_tool = ToolNode(func=npv, name='npv')
        logger.info('Tool node created')
        return calc_tool
    except Exception as e:
        logger.error(f'Error creating tool node: {e}')
        return None

def create_agent_node(llm: ChatOpenAI, tools: List[ToolNode]) -> AgentNode:
    """
    Create an agent node with the given LLM and tools.

    Args:
    - llm (ChatOpenAI): The LLM to use.
    - tools (List[ToolNode]): The tools to use.

    Returns:
    - AgentNode: The created agent node.
    """
    try:
        # Create an agent node with the given LLM and tools
        assistant = AgentNode(llm=llm, tools=tools)
        logger.info('Agent node created')
        return assistant
    except Exception as e:
        logger.error(f'Error creating agent node: {e}')
        return None

def create_graph(memory: MemoryGraph, agent: AgentNode) -> Graph:
    """
    Create a graph with the given memory and agent.

    Args:
    - memory (MemoryGraph): The memory to use.
    - agent (AgentNode): The agent to use.

    Returns:
    - Graph: The created graph.
    """
    try:
        # Create a graph with the given memory and agent
        graph = Graph().add_edges(memory >> agent >> memory).compile()
        logger.info('Graph created')
        return graph
    except Exception as e:
        logger.error(f'Error creating graph: {e}')
        return None

if __name__ == '__main__':
    # Create a memory graph
    memory = create_memory_graph()
    
    # Create a tool node for the NPV function
    calc_tool = create_tool_node()
    
    # Create an LLM
    llm = ChatOpenAI(model_name='gpt-4o-mini')
    
    # Create an agent node with the LLM and tool node
    assistant = create_agent_node(llm, [calc_tool])
    
    # Create a graph with the memory and agent
    graph = create_graph(memory, assistant)
    
    # Invoke the graph with a question
    result = graph.invoke('What\'s the NPV of $1 M over 5 years at 7 %?')
    logger.info(f'Result: {result}')
",
        "commit_message": "feat: implement specialized test_data_loader logic"
    }
}
```