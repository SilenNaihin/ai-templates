from __future__ import annotations

from typing import List, Optional, Union

import openai
from openai import Model

from ai_templates.oai.types.models import OPEN_AI_MODELS
from ai_templates.oai.types.Singleton import Singleton
from ai_templates.oai.types.base import TText


class ApiManager(metaclass=Singleton):
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
        self.models: Optional[list[Model]] = None

    def reset(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
        self.models = None

    def update_cost(self, prompt_tokens, completion_tokens, model: str):
        """
        Update the total cost, prompt tokens, and completion tokens.

        Args:
        prompt_tokens (int): The number of tokens used in the prompt.
        completion_tokens (int): The number of tokens used in the completion.
        model (str): The model used for the API call.
        """
        # if v2 is appended on to the end like with ada-embedding

        model = model[:-3] if model.endswith("-v2") else model

        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_cost += (
            prompt_tokens * OPEN_AI_MODELS[model].prompt_token_cost
            + completion_tokens * OPEN_AI_MODELS[model].completion_token_cost
        ) / 100  # convert to dollars from cents
        print(f"Total running cost: ${self.total_cost:.3f}")

    def check_model(self, model: str) -> str:
        """Check if model specified is available for use. If not, return gpt-3.5-turbo."""
        models = self.get_models()

        if any(model in m["id"] for m in models):
            return model

        print("You do not have access to {model}.")
        return "gpt-3.5-turbo"

    def get_total_prompt_tokens(self):
        """
        Get the total number of prompt tokens.

        Returns:
        int: The total number of prompt tokens.
        """
        return self.total_prompt_tokens

    def get_total_completion_tokens(self):
        """
        Get the total number of completion tokens.

        Returns:
        int: The total number of completion tokens.
        """
        return self.total_completion_tokens

    def get_total_cost(self):
        """
        Get the total cost of API calls.

        Returns:
        float: The total cost of API calls.
        """
        return self.total_cost

    def get_models(self) -> List[Model]:
        """
        Get list of available GPT models.

        Returns:
        list: List of available GPT models.

        """
        if self.models is None:
            all_models = openai.Model.list().data
            self.models = [model for model in all_models if "gpt" in model["id"]]

        return self.models
