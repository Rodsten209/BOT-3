import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📦 Каталог"), KeyboardButton("🤖 AI-помощник")],
        [KeyboardButton("📞 Поддержка"), KeyboardButton("🛡️ Гарант")],
        [KeyboardButton("🚢 Заказ из Китая"), KeyboardButton("📦 Опт/дропшиппинг")]
    ]
    await update.message.reply_text(
        "Добро пожаловать в ShadyChinaBot! Выберите опцию:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📦 Каталог":
        kb = [
            [InlineKeyboardButton("👚 Каталог с одеждой", callback_data='catalog_clothes')],
            [InlineKeyboardButton("🛡️ Гарант", callback_data='catalog_guarantee')],
            [InlineKeyboardButton("🚢 Заказ из Китая", callback_data='catalog_order')],
            [InlineKeyboardButton("📦 Опт/дропшиппинг", callback_data='catalog_wholesale')],
            [InlineKeyboardButton("🔙 Назад", callback_data='back_main')]
        ]
        await update.message.reply_text(
            "📦 *Каталог услуг:*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(kb)
        )
    elif text == "🤖 AI-помощник":
        await update.message.reply_text("AI-помощник в разработке.")
    elif text == "📞 Поддержка":
        await update.message.reply_text("Связь с поддержкой: @shadychina_support")
    elif text == "🛡️ Гарант":
        await update.message.reply_text("Гарант: https://t.me/shadychina_guarantee")
    elif text == "🚢 Заказ из Китая":
        await update.message.reply_text("Нажмите 📦 Каталог → Заказ из Китая.")
    elif text == "📦 Опт/дропшиппинг":
        await update.message.reply_text("Опт/дропшиппинг скоро будет доступен.")
    else:
        await update.message.reply_text("Нажмите одну из кнопок меню.")

async def catalog_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == 'catalog_clothes':
        kb = [
            [InlineKeyboardButton("👔 Мужская", url='https://t.me/shadychina_men')],
            [InlineKeyboardButton("👗 Женская", url='https://t.me/shadychina_women')],
            [InlineKeyboardButton("👶 Детская", url='https://t.me/shadychina_kids')],
            [InlineKeyboardButton("🔙 Назад", callback_data='catalog')]
        ]
        await q.edit_message_text("Каталог с одеждой:", reply_markup=InlineKeyboardMarkup(kb))

    elif data == 'catalog_guarantee':
        await q.edit_message_text(
            "🛡️ *Гарант*
Мы гарантируем возврат денег при несоответствии товара.
"
            "Подробнее: https://t.me/shadychina_guarantee",
            parse_mode='Markdown'
        )

    elif data == 'catalog_order':
        kb = [
            [InlineKeyboardButton("1688", callback_data='plat_1688')],
            [InlineKeyboardButton("Taobao", callback_data='plat_taobao')],
            [InlineKeyboardButton("Poizon", callback_data='plat_poizon')],
            [InlineKeyboardButton("Другие", callback_data='plat_other')],
            [InlineKeyboardButton("🔙 Назад", callback_data='catalog')]
        ]
        await q.edit_message_text("Заказ из Китая — выберите платформу:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith('plat_'):
        platform = data.split('_')[1]
        await q.edit_message_text(
            f"Ваш заказ будет сделан через *{platform}*.
"
            "Уточните детали здесь: https://t.me/shadychina_order_form",
            parse_mode='Markdown'
        )

    elif data == 'catalog_wholesale':
        await q.edit_message_text(
            "📦 *Опт/дропшиппинг*
В разработке. Скоро автоматизируем процесс.",
            parse_mode='Markdown'
        )

    elif data == 'back_main':
        await start(update, context)

    elif data == 'catalog':
        await handle_text(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(catalog_callback))
    app.run_polling()

if __name__ == '__main__':
    main()
