import operator
from pathlib import Path
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
    def reasoner(state: State) -> dict:

        llm_with_tools = _create_llm_agent()

        messages_with_tool_response = [
            llm_with_tools.invoke(
                """
                You are an advanced codebase analysis agent designed to assist in identifying files within
                a software repository that are relevant to solving specific issues.

                Write a long nice essay about why icecream is the best food in the world.
                """
            )
        ]

        return {
            "messages": messages_with_tool_response,
            "final_answer": []
        }

    @staticmethod
    def parser(state: State) -> dict[str, list[Path]]:
        return {"final_answer": []}


class MyGraph(StateGraph):
    def __init__(self):
        super().__init__(State)

        self.add_node(Nodes.reasoner.__name__, Nodes.reasoner)
        self.add_node(Nodes.parser.__name__, Nodes.parser)

        self.add_edge(START, Nodes.reasoner.__name__)
        self.add_edge(Nodes.reasoner.__name__, Nodes.parser.__name__)
        self.add_edge(Nodes.parser.__name__, END)

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
