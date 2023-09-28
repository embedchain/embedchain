import os
from typing import Optional

from langchain.llms.octoai_endpoint import OctoAIEndpoint

from embedchain.config import BaseLlmConfig
from embedchain.helper.json_serializable import register_deserializable
from embedchain.llm.base import BaseLlm

"""
import os

os.environ["OCTOAI_API_TOKEN"] = <>
os.environ["ENDPOINT_URL"] = "https://mpt-7b-demo-kk0powt97tmb.octoai.run/generate"

from langchain.llms.octoai_endpoint import OctoAIEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


template = \"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n Instruction:\n{question}\n Response: \"""
prompt = PromptTemplate(template=template, input_variables=["question"])

llm = OctoAIEndpoint(
    model_kwargs={
        "max_new_tokens": 200,
        "temperature": 0.75,
        "top_p": 0.95,
        "seed": None,
        "stop": [],
    },
)

question = "Who was leonardo davinci?"

llm_chain = LLMChain(prompt=prompt, llm=llm)

llm_chain.run(question)
"""


@register_deserializable
class OctoAILlm(BaseLlm):
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        if "OCTOAI_API_TOKEN" not in os.environ:
            raise ValueError("Please set the OCTOAI_API_TOKEN environment variable.")

        # Set default config values specific to this llm
        if not config:
            config = BaseLlmConfig()
            # Add variables to this block that have a default value in the parent class
            config.max_tokens = 200
            config.temperature = 0.75
            config.top_p = 0.95
            config.repetition_penalty = 1

        # Add variables that are `none` by default to this block.
        if not config.endpoint_url:
            config.endpoint_url = "https://mpt-7b-demo-kk0powt97tmb.octoai.run/generate_stream"

        super().__init__(config=config)

    def get_llm_model_answer(self, prompt):
        # TODO: Move the model and other inputs into config
        if self.config.system_prompt:
            raise ValueError("OctoAIApp does not support `system_prompt`")
        llm = OctoAIEndpoint(
            model_kwargs={
                "max_new_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "repetition_penalty": self.config.repetition_penalty,
                "seed": None,
                "stop": [],
            },
        )
        return llm(prompt)
