import os
from openai import OpenAI


def get_provider_config(model_name: str):
    model = (model_name or "").strip()

    if model.startswith("moonshot/"):
        return {
            "provider": "moonshot",
            "base_url": os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1"),
            "api_key": os.getenv("MOONSHOT_API_KEY", ""),
            "model": model.replace("moonshot/", "", 1),
        }

    if model.startswith("deepseek/"):
        return {
            "provider": "deepseek",
            "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
            "model": model.replace("deepseek/", "", 1),
        }

    return {
        "provider": "openai",
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": model.replace("openai/", "", 1) if model.startswith("openai/") else model,
    }


def create_client_by_model(model_name: str):
    config = get_provider_config(model_name)
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
    )
    return client, config
