"""
Script which re-creates a dataset in LangSmith
account: https://smith.langchain.com/
"""

import langsmith
import langsmith.utils
from const import DATASET_NAME
from dotenv import load_dotenv
from langsmith import Client
from loguru import logger


load_dotenv()


class MyDataset:
    def __init__(self):
        self.client = Client()

    def create_remote(self) -> None:
        """Upload data to a dataset to make it match local data."""
        dataset = self.client.create_dataset(
            DATASET_NAME,
            description="Some description"
        )

        self.client.create_examples(
            inputs=[
                {"task_id": str(i)} for i in range(30)
            ],
            outputs=[
                {"task_value": str(100 + i)} for i in range(30)
            ],
            dataset_id=dataset.id,
        )
        logger.success(
            f"Dataset {dataset.name} created successfully"
        )

def run() -> None:
    """Sync remote datasets with local setup."""
    dataset = MyDataset()
    try:
        dataset.create_remote()
    except langsmith.utils.LangSmithNotFoundError:
        logger.info(f"Dataset {DATASET_NAME} already exists.")



if __name__ == "__main__":
    run()
