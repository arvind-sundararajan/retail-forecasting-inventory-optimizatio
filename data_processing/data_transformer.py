```json
{
    "data_processing/data_transformer.py": {
        "content": "
import logging
from typing import List, Dict
from langchain import MemoryGraph, ToolNode, AgentNode, Graph
from langchain.chat_models import ChatOpenAI
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def non_stationary_drift_index(data: List[float]) -> float:
    """
    Calculate the non-stationary drift index for a given time series data.

    Args:
    - data (List[float]): Time series data

    Returns:
    - float: Non-stationary drift index
    """
    try:
        # Calculate the mean and standard deviation of the data
        mean = np.mean(data)
        std_dev = np.std(data)
        
        # Calculate the non-stationary drift index
        drift_index = np.abs(mean - np.mean(data[:len(data)//2])) / std_dev
        
        logger.info(f'Non-stationary drift index: {drift_index}')
        return drift_index
    except Exception as e:
        logger.error(f'Error calculating non-stationary drift index: {e}')
        return None

def stochastic_regime_switch(data: List[float], threshold: float) -> bool:
    """
    Determine if a stochastic regime switch has occurred based on the given data and threshold.

    Args:
    - data (List[float]): Time series data
    - threshold (float): Threshold value for regime switch

    Returns:
    - bool: True if regime switch has occurred, False otherwise
    """
    try:
        # Calculate the non-stationary drift index
        drift_index = non_stationary_drift_index(data)
        
        # Check if the drift index exceeds the threshold
        if drift_index is not None and drift_index > threshold:
            logger.info('Stochastic regime switch detected')
            return True
        else:
            logger.info('No stochastic regime switch detected')
            return False
    except Exception as e:
        logger.error(f'Error detecting stochastic regime switch: {e}')
        return False

def create_memory_graph(short_term: int, long_term_path: str) -> MemoryGraph:
    """
    Create a memory graph with the given short-term and long-term memory settings.

    Args:
    - short_term (int): Short-term memory size
    - long_term_path (str): Long-term memory path

    Returns:
    - MemoryGraph: Created memory graph
    """
    try:
        # Create the memory graph
        memory = MemoryGraph(short_term=short_term, long_term_path=long_term_path)
        logger.info(f'Memory graph created with short-term size {short_term} and long-term path {long_term_path}')
        return memory
    except Exception as e:
        logger.error(f'Error creating memory graph: {e}')
        return None

def create_tool_node(func, name: str) -> ToolNode:
    """
    Create a tool node with the given function and name.

    Args:
    - func: Function to be used in the tool node
    - name (str): Name of the tool node

    Returns:
    - ToolNode: Created tool node
    """
    try:
        # Create the tool node
        tool = ToolNode(func=func, name=name)
        logger.info(f'Tool node created with name {name}')
        return tool
    except Exception as e:
        logger.error(f'Error creating tool node: {e}')
        return None

def create_agent_node(llm, tools: List[ToolNode]) -> AgentNode:
    """
    Create an agent node with the given language model and tools.

    Args:
    - llm: Language model to be used in the agent node
    - tools (List[ToolNode]): List of tools to be used in the agent node

    Returns:
    - AgentNode: Created agent node
    """
    try:
        # Create the agent node
        agent = AgentNode(llm=llm, tools=tools)
        logger.info('Agent node created')
        return agent
    except Exception as e:
        logger.error(f'Error creating agent node: {e}')
        return None

def create_graph(memory: MemoryGraph, agent: AgentNode) -> Graph:
    """
    Create a graph with the given memory and agent nodes.

    Args:
    - memory (MemoryGraph): Memory node
    - agent (AgentNode): Agent node

    Returns:
    - Graph: Created graph
    """
    try:
        # Create the graph
        graph = Graph().add_edges(memory >> agent >> memory).compile()
        logger.info('Graph created')
        return graph
    except Exception as e:
        logger.error(f'Error creating graph: {e}')
        return None

if __name__ == '__main__':
    # Create a sample time series data
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    # Calculate the non-stationary drift index
    drift_index = non_stationary_drift_index(data)
    
    # Detect stochastic regime switch
    regime_switch = stochastic_regime_switch(data, threshold=0.5)
    
    # Create a memory graph
    memory = create_memory_graph(short_term=5, long_term_path='vector://chroma')
    
    # Create a tool node
    def npv(amount: float, years: int, rate: float = 0.07) -> float:
        return amount / ((1 + rate) ** years)
    tool = create_tool_node(func=npv, name='npv')
    
    # Create an agent node
    llm = ChatOpenAI(model_name='gpt-4o-mini')
    agent = create_agent_node(llm=llm, tools=[tool])
    
    # Create a graph
    graph = create_graph(memory=memory, agent=agent)
    
    # Invoke the graph
    result = graph.invoke('What\'s the NPV of $1 M over 5 years at 7 %?')
    logger.info(f'Result: {result}')
",
        "commit_message": "feat: implement specialized data_transformer logic"
    }
}
```