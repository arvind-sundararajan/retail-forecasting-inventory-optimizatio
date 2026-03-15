```json
{
    "data_ingestion/data_preprocessor.py": {
        "content": "
import logging
from typing import List, Dict
from langchain import MemoryGraph, ToolNode, AgentNode, Graph
from langchain.chat_models import ChatOpenAI
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def non_stationary_drift_index(data: List[float]) -> float:
    """
    Calculate the non-stationary drift index for the given data.

    Args:
    - data (List[float]): The input data.

    Returns:
    - float: The non-stationary drift index.
    """
    try:
        # Calculate the mean and standard deviation of the data
        mean = np.mean(data)
        std_dev = np.std(data)
        
        # Calculate the non-stationary drift index
        drift_index = np.abs(mean - std_dev) / (mean + std_dev)
        
        logger.info(f'Non-stationary drift index: {drift_index}')
        return drift_index
    except Exception as e:
        logger.error(f'Error calculating non-stationary drift index: {e}')
        return None

def stochastic_regime_switch(data: List[float]) -> bool:
    """
    Determine if a stochastic regime switch has occurred in the given data.

    Args:
    - data (List[float]): The input data.

    Returns:
    - bool: True if a stochastic regime switch has occurred, False otherwise.
    """
    try:
        # Calculate the mean and standard deviation of the data
        mean = np.mean(data)
        std_dev = np.std(data)
        
        # Determine if a stochastic regime switch has occurred
        regime_switch = np.abs(mean - std_dev) > 2 * std_dev
        
        logger.info(f'Stochastic regime switch: {regime_switch}')
        return regime_switch
    except Exception as e:
        logger.error(f'Error determining stochastic regime switch: {e}')
        return False

def data_preprocessing(data: List[float]) -> List[float]:
    """
    Preprocess the given data by applying non-stationary drift index and stochastic regime switch checks.

    Args:
    - data (List[float]): The input data.

    Returns:
    - List[float]: The preprocessed data.
    """
    try:
        # Calculate the non-stationary drift index
        drift_index = non_stationary_drift_index(data)
        
        # Determine if a stochastic regime switch has occurred
        regime_switch = stochastic_regime_switch(data)
        
        # Preprocess the data based on the results
        if drift_index is not None and regime_switch:
            # Apply a transformation to the data if a stochastic regime switch has occurred
            data = [x * 2 for x in data]
        
        logger.info(f'Preprocessed data: {data}')
        return data
    except Exception as e:
        logger.error(f'Error preprocessing data: {e}')
        return []

def create_memory_graph() -> MemoryGraph:
    """
    Create a memory graph for the data preprocessing pipeline.

    Returns:
    - MemoryGraph: The created memory graph.
    """
    try:
        # Create a memory graph with short-term and long-term memory
        memory = MemoryGraph(short_term=5, long_term_path='vector://chroma')
        
        logger.info(f'Memory graph created: {memory}')
        return memory
    except Exception as e:
        logger.error(f'Error creating memory graph: {e}')
        return None

def create_tool_node() -> ToolNode:
    """
    Create a tool node for the data preprocessing pipeline.

    Returns:
    - ToolNode: The created tool node.
    """
    try:
        # Define a function for the tool node
        def npv(amount: float, years: int, rate: float = 0.07) -> float:
            return amount / ((1 + rate) ** years)
        
        # Create a tool node with the function
        tool = ToolNode(func=npv, name='npv')
        
        logger.info(f'Tool node created: {tool}')
        return tool
    except Exception as e:
        logger.error(f'Error creating tool node: {e}')
        return None

def create_agent_node(memory: MemoryGraph, tool: ToolNode) -> AgentNode:
    """
    Create an agent node for the data preprocessing pipeline.

    Args:
    - memory (MemoryGraph): The memory graph.
    - tool (ToolNode): The tool node.

    Returns:
    - AgentNode: The created agent node.
    """
    try:
        # Create a chat model for the agent node
        llm = ChatOpenAI(model_name='gpt-4o-mini')
        
        # Create an agent node with the chat model and tool node
        agent = AgentNode(llm=llm, tools=[tool])
        
        logger.info(f'Agent node created: {agent}')
        return agent
    except Exception as e:
        logger.error(f'Error creating agent node: {e}')
        return None

def create_graph(memory: MemoryGraph, agent: AgentNode) -> Graph:
    """
    Create a graph for the data preprocessing pipeline.

    Args:
    - memory (MemoryGraph): The memory graph.
    - agent (AgentNode): The agent node.

    Returns:
    - Graph: The created graph.
    """
    try:
        # Create a graph with the memory graph and agent node
        graph = Graph().add_edges(memory >> agent >> memory).compile()
        
        logger.info(f'Graph created: {graph}')
        return graph
    except Exception as e:
        logger.error(f'Error creating graph: {e}')
        return None

if __name__ == '__main__':
    # Create a sample dataset
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    # Preprocess the data
    preprocessed_data = data_preprocessing(data)
    
    # Create a memory graph
    memory = create_memory_graph()
    
    # Create a tool node
    tool = create_tool_node()
    
    # Create an agent node
    agent = create_agent_node(memory, tool)
    
    # Create a graph
    graph = create_graph(memory, agent)
    
    # Invoke the graph with a sample input
    result = graph.invoke('What is the NPV of $1M over 5 years at 7%?')
    
    logger.info(f'Result: {result}')
",
        "commit_message": "feat: implement specialized data_preprocessor logic"
    }
}
```