import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

db = sqlite3.connect("empire.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER,
    bank INTEGER,
    factory INTEGER,
    power INTEGER
)
""")
db.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)",
        (user_id, 100, 1, 1, 1)
    )
    db.commit()

    keyboard = [
        [InlineKeyboardButton("🏰 My Empire", callback_data="status")],
        [InlineKeyboardButton("🏗 Upgrade", callback_data="upgrade")]
    ]

    await update.message.reply_text(
        "👑 Welcome to EmpireBot!\nStart building your empire.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "status":
        cursor.execute(
            "SELECT coins, bank, factory, power FROM users WHERE user_id=?",
            (user_id,)
        )
        coins, bank, factory, power = cursor.fetchone()

        await query.answer()
        await query.message.reply_text(
            f"🏰 Your Empire:\n"
            f"🪙 Coins: {coins}\n"
            f"🏦 Bank: {bank}\n"
            f"🏭 Factory: {factory}\n"
            f"⚡ Power: {power}"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.run_polling()
