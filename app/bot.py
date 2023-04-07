"""
Module containing implementation of
launching a Telegram bot and model
inference using HuggingFace
Inference API inside it
"""
from io import BytesIO

import requests
from PIL import Image
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)


class Model:
    """
    Class just to make queries
    using HuggingFace Inference API
    to StableDiffusion V1.5 with
    Python requests
    """

    def __init__(self,
                 hf_token: str,
                 device: str = "cpu",
                 repo_id: str = "runwayml/stable-diffusion-v1-5",
                 seed: int = None) -> None:
        self.device = device
        self.repo_id = repo_id
        self.api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        self.headers = {"Authorization": f"Bearer {hf_token}",
                        "Content-Type": "application/json", "Accept": "image/png"}
        self.seed = seed

    def generate(self,
                 prompt: str) -> Image:
        """
        Method for getting
        image from a given prompt
        """
        payload = {"inputs": prompt}
        response = requests.post(
            self.api_url, headers=self.headers, json=payload)
        image = Image.open(BytesIO(response.content))
        return image

    @staticmethod
    def img2bytes(image: Image) -> BytesIO:
        """
        Convert image to bytes
        """
        image_bytes = BytesIO()
        image_bytes.name = "generated_image.jpeg"
        image.save(image_bytes, "JPEG")
        image_bytes.seek(0)
        return image_bytes


class Bot:
    """
    Telegram bot which can
    read prompt and simply get
    the result from specified model
    """

    def __init__(self,
                 token: str,
                 model: Model) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.model = model

    async def query(self,
                    update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Asynchronous query for
        getting image in bytes
        from model
        """
        message = await update.message.reply_text("Image is generating by StableDiffusion...",
                                                  reply_to_message_id=update.message.message_id)

        image = self.model.generate(prompt=update.message.text)

        await context.bot.delete_message(chat_id=message.chat_id,
                                         message_id=message.message_id)
        await context.bot.send_photo(
            update.effective_user.id,
            self.model.img2bytes(image)
        )

    def run(self) -> None:
        """
        Running infinite polling
        """
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.query))

        print("Running bot...")
        self.app.run_polling()
