import asyncio

from nlu.test import run_evaluation
from rasa.nlu import train
from rasa.nlu.components import ComponentBuilder
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.model import Interpreter
from rasa.utils.tensorflow.constants import (
    INTENT_CLASSIFICATION,
    NUM_TRANSFORMER_LAYERS,
    BILOU_FLAG,
    EPOCHS,
)


async def run():
    _config = RasaNLUModelConfig(
        {
            "pipeline": [
                {"name": "WhitespaceTokenizer"},
                {"name": "CountVectorsFeaturizer"},
                {
                    "name": "CountVectorsFeaturizer",
                    "analyzer": "char_wb",
                    "max_ngram": 4,
                    "min_ngram": 1,
                },
                {
                    "name": "DIETClassifier",
                    NUM_TRANSFORMER_LAYERS: 1,
                    INTENT_CLASSIFICATION: False,
                    BILOU_FLAG: False,
                    EPOCHS: 3,
                },
            ],
            "language": "en",
        }
    )

    (trained, _, persisted_path) = await train(
        _config,
        path="output",
        data="/Users/tabergma/Repositories/training-data/intent_and_entity_datasets/SNIPS/train_multi.md",
        component_builder=ComponentBuilder(),
    )

    loaded = Interpreter.load(persisted_path, ComponentBuilder())

    run_evaluation(
        data_path="/Users/tabergma/Repositories/training-data/intent_and_entity_datasets/SNIPS/test_multi.md",
        model_path=persisted_path,
        output_directory="output",
        errors=True,
    )

    print(loaded.parse("2020 is a year with no snow."))


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(run())
