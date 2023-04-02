import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from io import BytesIO
import random

class Model:
    def __init__(self, 
                 device: str = "cpu", 
                 repo_id: str = "runwayml/stable-diffusion-v1-5", 
                 seed: int = None) -> None:
        self.device = device
        self.repo_id = repo_id
        
        print("Loading model...")
        self.model = StableDiffusionPipeline.from_pretrained(self.repo_id, torch_dtype=torch.float16).to(self.device)
        print(f"Loaded {self.model}.")
        
        self.seed = seed
        
    def generate(self, 
                 prompt: str,
                 width: int = 224, 
                 height: int = 224) -> Image:
        if self.seed is None:
            seed = random.randint(0, 4096)
            
            return self.model(
                prompt=list[prompt], 
                generator=seed, 
                width=width, 
                height=height
            )
    
    def img2bytes(self, 
                  image: Image) -> BytesIO:
        bytes = BytesIO()
        bytes.name = "generated_image.jpeg"
        image.save(bytes, "JPEG")
        
        return bytes
    
class Bot:
    def __init__(self, 
                 token: str, 
                 model: Model) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.model = model
        
    async def generate_and_send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = await update.message.reply_text("Image is generating by StableDiffusion...", 
                                                       reply_to_message_id=update.message.message_id)
        
        image = self.model.generate(prompt=update.message.text)
        
        await context.bot.delete_message(chat_id=progress_msg.chat_id, 
                                         message_id=progress_msg.message_id)
        await context.bot.send_photo(
            update.effective_user.id, 
            self.model.img2bytes(image)
        )
        
    def run(self) -> None:
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_and_send_photo))
        
        print("Running bot...")
        self.app.run_polling()