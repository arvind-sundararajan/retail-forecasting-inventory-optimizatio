```json
{
    "deployment/config.py": {
        "content": "
import logging
from langchain import MemoryGraph, ToolNode, AgentNode, Graph
from langchain.chat_models import ChatOpenAI
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_memory_graph(short_term: int = 5, long_term_path: str = 'vector://chroma') -> MemoryGraph:
    """
    Configure the memory graph for the agent.

    Args:
    - short_term (int): The short-term memory size.
    - long_term_path (str): The path to the long-term memory.

    Returns:
    - MemoryGraph: The configured memory graph.
    """
    try:
        memory = MemoryGraph(short_term=short_term, long_term_path=long_term_path)
        logger.info('Memory graph configured successfully')
        return memory
    except Exception as e:
        logger.error(f'Error configuring memory graph: {e}')
        raise

def create_npv_tool() -> ToolNode:
    """
    Create a tool node for calculating the net present value (NPV).

    Returns:
    - ToolNode: The NPV tool node.
    """
    try:
        def npv(amount: float, years: int, rate: float = 0.07) -> float:
            """
            Calculate the net present value (NPV).

            Args:
            - amount (float): The initial amount.
            - years (int): The number of years.
            - rate (float): The interest rate.

            Returns:
            - float: The NPV.
            """
            return amount / ((1 + rate) ** years)

        calc_tool = ToolNode(func=npv, name='npv')
        logger.info('NPV tool created successfully')
        return calc_tool
    except Exception as e:
        logger.error(f'Error creating NPV tool: {e}')
        raise

def create_llm_agent(llm_model_name: str = 'gpt-4o-mini') -> AgentNode:
    """
    Create an LLM agent node.

    Args:
    - llm_model_name (str): The name of the LLM model.

    Returns:
    - AgentNode: The LLM agent node.
    """
    try:
        llm = ChatOpenAI(model_name=llm_model_name)
        assistant = AgentNode(llm=llm)
        logger.info('LLM agent created successfully')
        return assistant
    except Exception as e:
        logger.error(f'Error creating LLM agent: {e}')
        raise

def create_graph(memory: MemoryGraph, agent: AgentNode, tool: ToolNode) -> Graph:
    """
    Create a graph with the memory, agent, and tool nodes.

    Args:
    - memory (MemoryGraph): The memory graph.
    - agent (AgentNode): The LLM agent.
    - tool (ToolNode): The NPV tool.

    Returns:
    - Graph: The created graph.
    """
    try:
        graph = Graph().add_edges(memory >> agent >> memory).add_node(tool)
        logger.info('Graph created successfully')
        return graph
    except Exception as e:
        logger.error(f'Error creating graph: {e}')
        raise

def simulate_rocket_science(graph: Graph) -> None:
    """
    Simulate the 'Rocket Science' problem.

    Args:
    - graph (Graph): The graph with the agent and tool nodes.
    """
    try:
        result = graph.invoke('What\'s the NPV of $1 M over 5 years at 7 %?')
        logger.info(f'NPV: {result}')
    except Exception as e:
        logger.error(f'Error simulating Rocket Science: {e}')
        raise

if __name__ == '__main__':
    memory = configure_memory_graph()
    tool = create_npv_tool()
    agent = create_llm_agent()
    graph = create_graph(memory, agent, tool)
    simulate_rocket_science(graph)
",
        "commit_message": "feat: implement specialized config logic"
    }
}
```