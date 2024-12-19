import operator
from pathlib import Path
from time import sleep
from typing import Annotated, TypedDict

from langgraph.constants import START

from langchain_core.messages import AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


def _create_llm_agent():
    llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0)
    return llm


class State(TypedDict):
    final_answer: list[Path] | None
    messages: Annotated[list[AnyMessage], operator.add]


class Nodes:

    @staticmethod
    def node_1(state: State) -> dict:

        sleep(3)

        return {
            "messages": ["messages_with_tool_response"],
            "final_answer": []
        }

    @staticmethod
    def node_2(state: State) -> dict[str, list[Path]]:
        return {"final_answer": []}


class MyGraph(StateGraph):
    def __init__(self):
        super().__init__(State)

        self.add_node(Nodes.node_1.__name__, Nodes.node_1)
        self.add_node(Nodes.node_2.__name__, Nodes.node_2)

        self.add_edge(START, Nodes.node_1.__name__)
        self.add_edge(Nodes.node_1.__name__, Nodes.node_2.__name__)
        self.add_edge(Nodes.node_2.__name__, END)

        self.compiled = self.compile()

    @staticmethod
    def create_init_state() -> State:
        return State(
            messages=[],
            final_answer=None,
        )

    def __call__(self) -> list[Path]:
        initial_state = self.create_init_state()
        resp: State = self.compiled.invoke(initial_state)
        return resp["final_answer"]


my_graph = MyGraph()
