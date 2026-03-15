```json
{
    "utils/utils.py": {
        "content": "
import logging
from typing import Tuple, List
from langchain import MemoryGraph, ToolNode, AgentNode, Graph
from langchain.chat_models import ChatOpenAI
import openai
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
        drift_index = np.abs(mean - std_dev)
        
        logger.info(f'Non-stationary drift index: {drift_index}')
        return drift_index
    except Exception as e:
        logger.error(f'Error calculating non-stationary drift index: {e}')
        return None

def stochastic_regime_switch(data: List[float], threshold: float) -> Tuple[List[float], List[float]]:
    """
    Perform stochastic regime switch for a given time series data.

    Args:
    - data (List[float]): Time series data
    - threshold (float): Threshold for regime switch

    Returns:
    - Tuple[List[float], List[float]]: Regime switched data
    """
    try:
        # Initialize lists to store regime switched data
        regime_switched_data = []
        original_data = []
        
        # Perform stochastic regime switch
        for i in range(len(data)):
            if data[i] > threshold:
                regime_switched_data.append(data[i] * np.random.uniform(0.9, 1.1))
                original_data.append(data[i])
            else:
                regime_switched_data.append(data[i])
                original_data.append(data[i])
        
        logger.info(f'Regime switched data: {regime_switched_data}')
        return regime_switched_data, original_data
    except Exception as e:
        logger.error(f'Error performing stochastic regime switch: {e}')
        return None, None

def create_memory_graph(short_term: int, long_term_path: str) -> MemoryGraph:
    """
    Create a memory graph with short-term and long-term memory.

    Args:
    - short_term (int): Short-term memory size
    - long_term_path (str): Long-term memory path

    Returns:
    - MemoryGraph: Memory graph
    """
    try:
        # Create a memory graph
        memory = MemoryGraph(short_term=short_term, long_term_path=long_term_path)
        
        logger.info(f'Memory graph created: {memory}')
        return memory
    except Exception as e:
        logger.error(f'Error creating memory graph: {e}')
        return None

def create_tool_node(func, name: str) -> ToolNode:
    """
    Create a tool node with a given function and name.

    Args:
    - func: Function to be used in the tool node
    - name (str): Name of the tool node

    Returns:
    - ToolNode: Tool node
    """
    try:
        # Create a tool node
        tool_node = ToolNode(func=func, name=name)
        
        logger.info(f'Tool node created: {tool_node}')
        return tool_node
    except Exception as e:
        logger.error(f'Error creating tool node: {e}')
        return None

def create_agent_node(llm, tools: List[ToolNode]) -> AgentNode:
    """
    Create an agent node with a given language model and tools.

    Args:
    - llm: Language model to be used in the agent node
    - tools (List[ToolNode]): List of tool nodes

    Returns:
    - AgentNode: Agent node
    """
    try:
        # Create an agent node
        agent_node = AgentNode(llm=llm, tools=tools)
        
        logger.info(f'Agent node created: {agent_node}')
        return agent_node
    except Exception as e:
        logger.error(f'Error creating agent node: {e}')
        return None

def create_graph(memory: MemoryGraph, agent: AgentNode) -> Graph:
    """
    Create a graph with a given memory and agent.

    Args:
    - memory (MemoryGraph): Memory graph
    - agent (AgentNode): Agent node

    Returns:
    - Graph: Graph
    """
    try:
        # Create a graph
        graph = Graph().add_edges(memory >> agent >> memory).compile()
        
        logger.info(f'Graph created: {graph}')
        return graph
    except Exception as e:
        logger.error(f'Error creating graph: {e}')
        return None

if __name__ == '__main__':
    # Create a memory graph
    memory = create_memory_graph(short_term=5, long_term_path='vector://chroma')
    
    # Create a tool node
    def npv(amount: float, years: int, rate: float = 0.07) -> float:
        return amount / ((1 + rate) ** years)
    tool_node = create_tool_node(func=npv, name='npv')
    
    # Create an agent node
    llm = ChatOpenAI(model_name='gpt-4o-mini')
    agent_node = create_agent_node(llm=llm, tools=[tool_node])
    
    # Create a graph
    graph = create_graph(memory=memory, agent=agent_node)
    
    # Invoke the graph
    result = graph.invoke('What\'s the NPV of $1 M over 5 years at 7 %?')
    logger.info(f'Result: {result}')
",
        "commit_message": "feat: implement specialized utils logic"
    }
}
```