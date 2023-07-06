"""
Module containing implementation of
a Telegram bot launching, query 
processing and interface
"""
from typing import List
from model import Model
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler, 
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

class Bot(object):
    """
    Telegram bot which can
    read prompt and simply get
    the result from specified model
    """

    def __init__(
        self,
        token: str,
        models: List[Model]
    ) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.models = models
        self.current_model = 0 # idx of chosen model in list of models `self.models`
        self.keyboard = []
        
        for idx, model in enumerate(self.models):
            self.keyboard.append([InlineKeyboardButton(model.name, callback_data=idx)])
            
    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        reply_markup = InlineKeyboardMarkup(self.keyboard)
        await update.message.reply_text(
            "Hi! I can turn any of your text query into an image "
            "using popular generative neural networks. Please choose "
            "one of the suggested ones below", 
            reply_markup=reply_markup
        )
        
    async def help(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        reply_markup = InlineKeyboardMarkup(self.keyboard)
        await update.message.reply_text(
            "Just write new prompt to get new image\n"
            "If you want to change model for generating "
            "pictures just restart a bot",
            reply_markup=reply_markup
        )
    
    async def choose_model(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query

        await query.answer()

        self.current_model = int(query.data)

        await query.edit_message_text(
            text=f"Selected model: {self.models[self.current_model].name}\n"
                 f"Write your prompt:"
        )

    async def query(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Asynchronous query for
        getting image in bytes
        from model
        """
        message = await update.message.reply_text(
            f"Image is generating by {self.models[self.current_model].name}...",
            reply_to_message_id=update.message.message_id
        )

        image = self.models[self.current_model].generate(prompt=update.message.text)

        await context.bot.delete_message(
            chat_id=message.chat_id,
            message_id=message.message_id
        )
        await context.bot.send_photo(
            update.effective_user.id,
            Model.img2bytes(image)
        )

    def run(self) -> None:
        """
        Running infinite polling
        """
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(CallbackQueryHandler(self.choose_model))
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, self.query
            )
        )
        
        print("Running bot...")
        self.app.run_polling()
