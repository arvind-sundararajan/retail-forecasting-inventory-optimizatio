```json
{
    "deployment/deployment_script.py": {
        "content": "
import logging
from langchain import MemoryGraph, ToolNode, AgentNode, Graph
from langchain.chat_models import ChatOpenAI
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_memory_graph(short_term: int = 5, long_term_path: str = 'vector://chroma') -> MemoryGraph:
    """
    Create a memory graph with short-term and long-term memory.

    Args:
    - short_term (int): The number of short-term memory slots.
    - long_term_path (str): The path to the long-term memory storage.

    Returns:
    - MemoryGraph: The created memory graph.
    """
    try:
        memory = MemoryGraph(short_term=short_term, long_term_path=long_term_path)
        logger.info('Memory graph created successfully')
        return memory
    except Exception as e:
        logger.error(f'Error creating memory graph: {e}')
        raise

def create_npv_tool() -> ToolNode:
    """
    Create a tool node for calculating the net present value (NPV).

    Returns:
    - ToolNode: The created tool node.
    """
    try:
        def npv(amount: float, years: int, rate: float = 0.07) -> float:
            """
            Calculate the net present value (NPV) of an investment.

            Args:
            - amount (float): The initial investment amount.
            - years (int): The number of years the investment is held for.
            - rate (float): The annual interest rate (default: 0.07).

            Returns:
            - float: The calculated NPV.
            """
            return amount / ((1 + rate) ** years)

        calc_tool = ToolNode(func=npv, name='npv')
        logger.info('NPV tool created successfully')
        return calc_tool
    except Exception as e:
        logger.error(f'Error creating NPV tool: {e}')
        raise

def create_llm_agent(model_name: str = 'gpt-4o-mini') -> AgentNode:
    """
    Create an LLM reasoning agent.

    Args:
    - model_name (str): The name of the LLM model to use (default: 'gpt-4o-mini').

    Returns:
    - AgentNode: The created LLM agent.
    """
    try:
        llm = ChatOpenAI(model_name=model_name)
        assistant = AgentNode(llm=llm)
        logger.info('LLM agent created successfully')
        return assistant
    except Exception as e:
        logger.error(f'Error creating LLM agent: {e}')
        raise

def create_graph(memory: MemoryGraph, tool: ToolNode, agent: AgentNode) -> Graph:
    """
    Create a graph with the given memory, tool, and agent.

    Args:
    - memory (MemoryGraph): The memory graph to use.
    - tool (ToolNode): The tool node to use.
    - agent (AgentNode): The LLM agent to use.

    Returns:
    - Graph: The created graph.
    """
    try:
        graph = Graph().add_edges(memory >> agent >> memory).compile()
        logger.info('Graph created successfully')
        return graph
    except Exception as e:
        logger.error(f'Error creating graph: {e}')
        raise

def simulate_rocket_science(graph: Graph) -> None:
    """
    Simulate the 'Rocket Science' problem using the given graph.

    Args:
    - graph (Graph): The graph to use for simulation.
    """
    try:
        result = graph.invoke('What\'s the NPV of $1 M over 5 years at 7 %?')
        logger.info(f'Simulation result: {result}')
    except Exception as e:
        logger.error(f'Error simulating Rocket Science problem: {e}')
        raise

if __name__ == '__main__':
    memory = create_memory_graph()
    tool = create_npv_tool()
    agent = create_llm_agent()
    agent.tools = [tool]
    graph = create_graph(memory, tool, agent)
    simulate_rocket_science(graph)
",
        "commit_message": "feat: implement specialized deployment_script logic"
    }
}
```