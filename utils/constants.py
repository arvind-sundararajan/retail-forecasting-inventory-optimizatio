```json
{
    "utils/constants.py": {
        "content": "
import logging
from langchain import MemoryGraph, ToolNode, AgentNode, Graph
from langchain.chat_models import ChatOpenAI
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_non_stationary_drift_index(data: np.ndarray) -> float:
    """
    Calculate the non-stationary drift index for a given time series data.

    Args:
    - data (np.ndarray): Time series data

    Returns:
    - float: Non-stationary drift index
    """
    try:
        # Calculate the non-stationary drift index
        drift_index = np.std(data) / np.mean(data)
        logger.info(f'Non-stationary drift index: {drift_index}')
        return drift_index
    except Exception as e:
        logger.error(f'Error calculating non-stationary drift index: {e}')
        return None

def stochastic_regime_switch(probability: float) -> bool:
    """
    Perform a stochastic regime switch based on a given probability.

    Args:
    - probability (float): Probability of regime switch

    Returns:
    - bool: Whether the regime switch occurred
    """
    try:
        # Perform the stochastic regime switch
        switch_occurred = np.random.rand() < probability
        logger.info(f'Regime switch occurred: {switch_occurred}')
        return switch_occurred
    except Exception as e:
        logger.error(f'Error performing stochastic regime switch: {e}')
        return False

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
        # Create the memory graph
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
    - func: Function to use in the tool node
    - name (str): Name of the tool node

    Returns:
    - ToolNode: Tool node
    """
    try:
        # Create the tool node
        tool = ToolNode(func=func, name=name)
        logger.info(f'Tool node created: {tool}')
        return tool
    except Exception as e:
        logger.error(f'Error creating tool node: {e}')
        return None

def create_agent_node(llm, tools: list) -> AgentNode:
    """
    Create an agent node with a given language model and tools.

    Args:
    - llm: Language model to use in the agent node
    - tools (list): List of tools to use in the agent node

    Returns:
    - AgentNode: Agent node
    """
    try:
        # Create the agent node
        agent = AgentNode(llm=llm, tools=tools)
        logger.info(f'Agent node created: {agent}')
        return agent
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
        # Create the graph
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
        "commit_message": "feat: implement specialized constants logic"
    }
}
```