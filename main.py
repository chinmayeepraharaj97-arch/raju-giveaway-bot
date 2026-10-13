import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7970417823  # Your Telegram ID
OWNER_USERNAME = "@RAJUCONFIGYT"

# ================== DATA ==================
channels = []  # Will store channel usernames
maintenance = False
total_users = set()

# ================== LOGGING ==================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================== HELPERS ==================
async def is_admin(user_id):
    return user_id == ADMIN_ID

async def check_membership(user_id, context):
    if not channels:
        return True, []
    
    not_joined = []
    for ch in channels:
        try:
            member = await context.bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status in ["left", "kicked"]:
                not_joined.append(ch)
        except Exception as e:
            logger.error(f"Error checking {ch}: {e}")
            not_joined.append(ch)
    return len(not_joined) == 0, not_joined

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    total_users.add(user.id)

    if maintenance and user.id != ADMIN_ID:
        await update.message.reply_text("Bot is under maintenance. Please try again later.")
        return

    text = (
        "🎁 *Welcome to Raju Config Giveaway Store!* 🎁\n\n"
        "Join all required channels to unlock free rewards.\n\n"
        "Tap the button below to continue."
    )
    keyboard = [
        [InlineKeyboardButton("✅ CONTINUE / VERIFY", callback_data="check_join")],
        [InlineKeyboardButton("📜 Full Rules (All Languages)", callback_data="full_rules")]
    ]
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# ================== FULL RULES ==================
async def full_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "📜 *GIVEAWAY BOT — HOW TO GET FREE ITEMS* 🎁\n\n"
        "🇬🇧 *ENGLISH*\n"
        "1. Join all required Telegram channels and groups.\n"
        "2. After joining, return to the bot.\n"
        "3. Tap the CONTINUE / VERIFY button.\n"
        "4. Once verified, your free rewards will be unlocked!\n\n"
        "🇮🇳 *HINDI*\n"
        "1. सभी जरूरी Telegram चैनल्स और ग्रुप्स जॉइन करें।\n"
        "2. जॉइन करने के बाद बॉट पर वापस आएं।\n"
        "3. CONTINUE / VERIFY बटन दबाएं।\n"
        "4. वेरिफिकेशन के बाद फ्री रिवॉर्ड्स अनलॉक हो जाएंगे!\n\n"
        "🇮🇳 *TAMIL*\n"
        "1. தேவையான அனைத்து Telegram சேனல்கள் மற்றும் குழுக்களில் இணையுங்கள்.\n"
        "2. அனைத்திலும் இணைந்த பிறகு மீண்டும் பாட்டிற்கு வாருங்கள்.\n"
        "3. CONTINUE / VERIFY பொத்தானை அழுத்துங்கள்.\n"
        "4. சரிபார்ப்பு வெற்றிகரமாக முடிந்ததும் இலவச வெகுமதிகள் திறக்கப்படும்!\n\n"
        "🇮🇳 *TELUGU*\n"
        "1. అవసరమైన అన్ని Telegram ఛానెల్‌లు మరియు గ్రూపుల్లో జాయిన్ అవ్వండి.\n"
        "2. అన్నింటిలో జాయిన్ అయిన తర్వాత బాట్‌కి తిరిగి రండి.\n"
        "3. CONTINUE / VERIFY బటన్‌ను నొక్కండి.\n"
        "4. వెరిఫికేషన్ విజయవంతమైన తర్వాత ఉచిత రివార్డులు అన్‌లాక్ అవుతాయి!\n\n"
        "🇮🇳 *MALAYALAM*\n"
        "1. ആവശ്യമായ എല്ലാ Telegram ചാനലുകളിലും ഗ്രൂപ്പുകളിലും ജോയിൻ ചെയ്യുക.\n"
        "2. ജോയിൻ ചെയ്ത ശേഷം ബോട്ടിലേക്ക് തിരികെ വരിക.\n"
        "3. CONTINUE / VERIFY ബട്ടൺ അമർത്തുക.\n"
        "4. സ്ഥിരീകരണം കഴിഞ്ഞാൽ റിവാർഡുകൾ അൺലോക്ക് ആകും!\n\n"
        "💎 Join all channels → Verify → Claim your rewards!"
    )
    await query.message.reply_text(text, parse_mode="Markdown")

# ================== CHECK JOIN ==================
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    is_member, not_joined = await check_membership(user_id, context)

    if is_member:
        text = (
            "✅ *Verification Successful!*\n\n"
            "You have joined all required channels.\n\n"
            f"🎁 To claim your free rewards, please DM the owner:\n"
            f"*{OWNER_USERNAME}*"
        )
        await query.message.reply_text(text, parse_mode="Markdown")
    else:
        buttons = []
        for ch in not_joined:
            username = ch.replace("@", "")
            buttons.append([InlineKeyboardButton(f"➕ Join {ch}", url=f"https://t.me/{username}")])
        buttons.append([InlineKeyboardButton("✅ Verify Membership", callback_data="check_join")])

        text = (
            "🔐 *Membership Verification Required*\n\n"
            "Please join the channel(s) below to unlock free rewards:\n\n"
            "After joining all channels, tap *Verify Membership*."
        )
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

# ================== ADMIN PANEL ==================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.effective_user.id):
        await update.message.reply_text("You are not admin.")
        return

    keyboard = [
        [InlineKeyboardButton("👤 Change Owner", callback_data="admin_change_owner")],
        [InlineKeyboardButton("➕ Add Channel", callback_data="admin_add_channel")],
        [InlineKeyboardButton("➖ Remove Channel", callback_data="admin_remove_channel")],
        [InlineKeyboardButton("📋 View Channels", callback_data="admin_view_channels")],
        [InlineKeyboardButton("🔧 Maintenance", callback_data="admin_maintenance")],
        [InlineKeyboardButton("👥 Total Users", callback_data="admin_total_users")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="admin_main")]
    ]
    await update.message.reply_text("⚡ *ADMIN PANEL*\n\nSelect an option:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# ================== ADMIN CALLBACKS ==================
async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if not await is_admin(query.from_user.id):
        return

    if data == "admin_view_channels":
        if not channels:
            await query.message.reply_text("No channels added yet.")
        else:
            text = "📋 *Current Channels:*\n\n" + "\n".join([f"{i+1}. {ch}" for i, ch in enumerate(channels)])
            await query.message.reply_text(text, parse_mode="Markdown")

    elif data == "admin_maintenance":
        global maintenance
        maintenance = not maintenance
        status = "ON" if maintenance else "OFF"
        await query.message.reply_text(f"Maintenance Mode is now: *{status}*", parse_mode="Markdown")

    elif data == "admin_total_users":
        await query.message.reply_text(f"👥 Total Users: *{len(total_users)}*", parse_mode="Markdown")

    elif data == "admin_main":
        await start(update, context)

    elif data == "admin_add_channel":
        context.user_data["admin_step"] = "add_channel"
        await query.message.reply_text("Send the channel username (example: @mychannel):")

    elif data == "admin_remove_channel":
        if not channels:
            await query.message.reply_text("No channels to remove.")
            return
        text = "Current Channels:\n\n" + "\n".join([f"{i+1}. {ch}" for i, ch in enumerate(channels)])
        text += "\n\nSend the number of the channel to remove:"
        context.user_data["admin_step"] = "remove_channel"
        await query.message.reply_text(text)

    elif data == "admin_change_owner":
        context.user_data["admin_step"] = "change_owner"
        await query.message.reply_text("Send the new Owner Username (example: @RAJUCONFIGYT):")

# ================== HANDLE ADMIN TEXT ==================
async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.effective_user.id):
        return

    step = context.user_data.get("admin_step")
    if not step:
        return

    text = update.message.text.strip()

    if step == "add_channel":
        if not text.startswith("@"):
            text = "@" + text
        if text not in channels:
            channels.append(text)
            await update.message.reply_text(f"✅ Channel added: {text}")
        else:
            await update.message.reply_text("This channel is already added.")
        context.user_data["admin_step"] = None

    elif step == "remove_channel":
        try:
            index = int(text) - 1
            if 0 <= index < len(channels):
                removed = channels.pop(index)
                await update.message.reply_text(f"✅ Channel removed: {removed}")
            else:
                await update.message.reply_text("Invalid number.")
        except:
            await update.message.reply_text("Please send a valid number.")
        context.user_data["admin_step"] = None

    elif step == "change_owner":
        global OWNER_USERNAME
        if not text.startswith("@"):
            text = "@" + text
        OWNER_USERNAME = text
        await update.message.reply_text(f"✅ Owner Username updated to: {OWNER_USERNAME}")
        context.user_data["admin_step"] = None

# ================== MAIN ==================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(full_rules, pattern="^full_rules$"))
    app.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))
    app.add_handler(CallbackQueryHandler(admin_callbacks, pattern="^admin_"))
    app.add_handler(MessageHandler(filters.TEXT & \~filters.COMMAND, handle_admin_text))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
