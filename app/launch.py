"""
URLs for making requests
to inference models and
telegram bot easy launching
"""
from model import Model
from bot import Bot

model_api_url = {
    "StableDiffusion-v1-5": "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
    "StableDiffusion-2-1": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
    "OpenJourney": "https://api-inference.huggingface.co/models/prompthero/openjourney",
    "Van-Gogh-Diffusion": "https://api-inference.huggingface.co/models/dallinmackay/Van-Gogh-diffusion"
}

def launch_bot(telegram_token: str, huggingface_token: str) -> None:
    models = []
    for model_name, api_url in model_api_url.items():
        models.append(
            Model(
                hf_token=huggingface_token, 
                api_url=api_url, 
                name=model_name
            )
        )

    app = Bot(telegram_token, models)
    app.run()
