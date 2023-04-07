import random
import requests
import os
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from io import BytesIO


class Model:
    def __init__(self,
                 hf_token: str,
                 device: str = "cpu",
                 repo_id: str = "runwayml/stable-diffusion-v1-5",
                 seed: int = None) -> None:
        self.device = device
        self.repo_id = repo_id
        self.API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        self.headers = {"Authorization": f"Bearer {hf_token}",
                        "Content-Type": "application/json", "Accept": "image/png"}
        self.seed = seed

    def generate(self,
                 prompt: str,
                 width: int = 768,
                 height: int = 768) -> Image:
        payload = {"inputs": prompt}
        response = requests.post(
            self.API_URL, headers=self.headers, json=payload)
        # while response
        image = Image.open(BytesIO(response.content))
        return image

    def img2bytes(self,
                  image: Image) -> BytesIO:
        bytes = BytesIO()
        bytes.name = "generated_image.jpeg"
        image.save(bytes, "JPEG")
        bytes.seek(0)
        return bytes


class Bot:
    def __init__(self,
                 token: str,
                 model: Model) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.model = model

    async def query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.query))

        print("Running bot...")
        self.app.run_polling()
