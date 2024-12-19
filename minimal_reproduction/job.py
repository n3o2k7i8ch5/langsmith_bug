from langchain_core.tracers.context import tracing_v2_enabled
from langsmith import RunTree
from langsmith.evaluation import evaluate
from langsmith.schemas import Example

from const import DATASET_NAME
from loguru import logger

from graph import my_graph


def run_task(task_id: str) -> dict:

    logger.info(f"Running task {task_id}.")

    with tracing_v2_enabled():
        my_graph()

    logger.info(f"Finished task {task_id}.")

    return {"some_value": 1}


def evaluator(run_example: RunTree, defined_output_example: Example) -> dict:
    return {"key": "super score", "score": 1.0}


if __name__ == "__main__":
    from dotenv import load_dotenv
    assert load_dotenv()

    evaluate(
        lambda input: run_task(input["task_id"]),
        data=DATASET_NAME,
        evaluators=[evaluator],
        experiment_prefix=f"Evaluation experiment for dataset: {DATASET_NAME}.",
        max_concurrency=5
    )
