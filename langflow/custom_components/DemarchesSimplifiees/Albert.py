from langchain_openai import ChatOpenAI
from pydantic.v1 import SecretStr

from langflow.base.models.model import LCModelComponent
from langflow.field_typing import LanguageModel
from langflow.field_typing.range_spec import RangeSpec
from langflow.inputs import BoolInput, DictInput, DropdownInput, IntInput, SecretStrInput, SliderInput, StrInput


ALBERT_MODEL_NAMES = [
    'mistralai/Pixtral-12B-2409',
    'meta-llama/Llama-3.1-8B-Instruct',
    # 'BAAI/bge-m3',
    'google/gemma-2-9b-it',
    # 'openai/whisper-large-v3',
    # 'PleIAs/Cassandre-RAG',
    'neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8',
    'AgentPublic/llama3-instruct-guillaumetell',
    'AgentPublic/albert-spp-8b',
    # 'BAAI/bge-reranker-v2-m3',
    # 'intfloat/multilingual-e5-large'
]



class DemarchesSimplifieesAlbert(LCModelComponent):
    display_name = "Albert"
    description = "Generates text using Albert LLMs."
    icon = "Albert"
    name = "AlbertModel"

    inputs = [
        *LCModelComponent._base_inputs,
        IntInput(
            name="max_tokens",
            display_name="Max Tokens",
            advanced=True,
            info="The maximum number of tokens to generate. Set to 0 for unlimited tokens.",
            range_spec=RangeSpec(min=0, max=128000),
        ),
        DictInput(
            name="model_kwargs",
            display_name="Model Kwargs",
            advanced=True,
            info="Additional keyword arguments to pass to the model.",
        ),
        BoolInput(
            name="json_mode",
            display_name="JSON Mode",
            advanced=True,
            info="If True, it will output JSON regardless of passing a schema.",
        ),
        DropdownInput(
            name="model_name",
            display_name="Model Name",
            advanced=False,
            options=ALBERT_MODEL_NAMES,
            value=ALBERT_MODEL_NAMES[0],
        ),
        StrInput(
            name="albert_api_base",
            display_name="Albert API Base",
            advanced=False,
            value="https://albert.api.etalab.gouv.fr/v1",
            info="The base URL of the Albert API. "
            "Defaults to https://albert.api.etalab.gouv.fr/v1. "
            "You can change this to use other APIs like JinaChat, LocalAI and Prem.",
        ),
        SecretStrInput(
            name="api_key",
            display_name="Albert API Key",
            info="The Albert API Key to use for the Albert model.",
            advanced=False,
            value="OPENAI_API_KEY",
            required=True,
        ),
        SliderInput(
            name="temperature", display_name="Temperature", value=0.1, range_spec=RangeSpec(min=0, max=2, step=0.01)
        ),
        IntInput(
            name="seed",
            display_name="Seed",
            info="The seed controls the reproducibility of the job.",
            advanced=True,
            value=1,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        openai_api_key = self.api_key
        temperature = self.temperature
        model_name: str = self.model_name
        max_tokens = self.max_tokens
        model_kwargs = self.model_kwargs or {}
        albert_api_base = self.albert_api_base or "https://albert.api.etalab.gouv.fr/v1"
        json_mode = self.json_mode
        seed = self.seed

        api_key = SecretStr(openai_api_key).get_secret_value() if openai_api_key else None
        output = ChatOpenAI(
            max_tokens=max_tokens or None,
            model_kwargs=model_kwargs,
            model=model_name,
            base_url=albert_api_base,
            api_key=api_key,
            temperature=temperature if temperature is not None else 0.1,
            seed=seed,
        )
        if json_mode:
            output = output.bind(response_format={"type": "json_object"})

        return output

    def _get_exception_message(self, e: Exception):
        """Get a message from an Albert exception.

        Args:
            e (Exception): The exception to get the message from.

        Returns:
            str: The message from the exception.
        """
        try:
            from openai import BadRequestError
        except ImportError:
            return None
        if isinstance(e, BadRequestError):
            message = e.body.get("message")
            if message:
                return message
        return None
