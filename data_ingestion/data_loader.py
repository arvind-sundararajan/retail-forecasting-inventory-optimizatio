```json
{
    "data_ingestion/data_loader.py": {
        "content": "
import logging
from langchain import MemoryGraph, ToolNode, AgentNode, Graph
from langchain.chat_models import ChatOpenAI
from typing import Dict, List
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_non_stationary_drift_index(data: Dict[str, List[float]]) -> np.ndarray:
    """
    Load non-stationary drift index from data.

    Args:
    - data (Dict[str, List[float]]): Data containing non-stationary drift index.

    Returns:
    - np.ndarray: Non-stationary drift index.
    """
    try:
        non_stationary_drift_index = np.array(data['non_stationary_drift_index'])
        logger.info('Loaded non-stationary drift index')
        return non_stationary_drift_index
    except Exception as e:
        logger.error(f'Error loading non-stationary drift index: {e}')
        raise

def load_stochastic_regime_switch(data: Dict[str, List[float]]) -> np.ndarray:
    """
    Load stochastic regime switch from data.

    Args:
    - data (Dict[str, List[float]]): Data containing stochastic regime switch.

    Returns:
    - np.ndarray: Stochastic regime switch.
    """
    try:
        stochastic_regime_switch = np.array(data['stochastic_regime_switch'])
        logger.info('Loaded stochastic regime switch')
        return stochastic_regime_switch
    except Exception as e:
        logger.error(f'Error loading stochastic regime switch: {e}')
        raise

def create_memory_graph(short_term: int, long_term_path: str) -> MemoryGraph:
    """
    Create memory graph.

    Args:
    - short_term (int): Short-term memory size.
    - long_term_path (str): Long-term memory path.

    Returns:
    - MemoryGraph: Memory graph.
    """
    try:
        memory = MemoryGraph(short_term=short_term, long_term_path=long_term_path)
        logger.info('Created memory graph')
        return memory
    except Exception as e:
        logger.error(f'Error creating memory graph: {e}')
        raise

def create_tool_node(func: callable, name: str) -> ToolNode:
    """
    Create tool node.

    Args:
    - func (callable): Function to be used in the tool node.
    - name (str): Name of the tool node.

    Returns:
    - ToolNode: Tool node.
    """
    try:
        tool = ToolNode(func=func, name=name)
        logger.info('Created tool node')
        return tool
    except Exception as e:
        logger.error(f'Error creating tool node: {e}')
        raise

def create_agent_node(llm: ChatOpenAI, tools: List[ToolNode]) -> AgentNode:
    """
    Create agent node.

    Args:
    - llm (ChatOpenAI): Language model to be used in the agent node.
    - tools (List[ToolNode]): List of tool nodes to be used in the agent node.

    Returns:
    - AgentNode: Agent node.
    """
    try:
        agent = AgentNode(llm=llm, tools=tools)
        logger.info('Created agent node')
        return agent
    except Exception as e:
        logger.error(f'Error creating agent node: {e}')
        raise

def create_graph(memory: MemoryGraph, agent: AgentNode) -> Graph:
    """
    Create graph.

    Args:
    - memory (MemoryGraph): Memory graph.
    - agent (AgentNode): Agent node.

    Returns:
    - Graph: Graph.
    """
    try:
        graph = Graph().add_edges(memory >> agent >> memory).compile()
        logger.info('Created graph')
        return graph
    except Exception as e:
        logger.error(f'Error creating graph: {e}')
        raise

def simulate_rocket_science(graph: Graph) -> None:
    """
    Simulate rocket science problem.

    Args:
    - graph (Graph): Graph to be used in the simulation.
    """
    try:
        result = graph.invoke('What is the optimal trajectory for a rocket?')
        logger.info(f'Simulation result: {result}')
    except Exception as e:
        logger.error(f'Error simulating rocket science: {e}')
        raise

if __name__ == '__main__':
    # Load data
    data = {
        'non_stationary_drift_index': [1.0, 2.0, 3.0],
        'stochastic_regime_switch': [4.0, 5.0, 6.0]
    }
    non_stationary_drift_index = load_non_stationary_drift_index(data)
    stochastic_regime_switch = load_stochastic_regime_switch(data)

    # Create memory graph
    memory = create_memory_graph(short_term=5, long_term_path='vector://chroma')

    # Create tool node
    def npv(amount: float, years: int, rate: float = 0.07) -> float:
        return amount / ((1 + rate) ** years)
    tool = create_tool_node(func=npv, name='npv')

    # Create agent node
    llm = ChatOpenAI(model_name='gpt-4o-mini')
    agent = create_agent_node(llm=llm, tools=[tool])

    # Create graph
    graph = create_graph(memory=memory, agent=agent)

    # Simulate rocket science
    simulate_rocket_science(graph=graph)
",
        "commit_message": "feat: implement specialized data_loader logic"
    }
}
```