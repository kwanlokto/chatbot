from anthropic import Anthropic

class AnthropicClient:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def get_completion(self, prompt: str, model: str = "claude-3.5-sonnet", max_tokens: int = 500):
        response = self.client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens_to_sample=max_tokens
        )
        return response.completion