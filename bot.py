import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot Token နှင့် Admin ရဲ့ Telegram ID ကို ထည့်ပါ
BOT_TOKEN = 9165279241:AAG0H_tynn5aED2gaGe9g4z0zw2y_KHNRAw
ADMIN_ID = @shinyam98  # <--- ကိုယ့်ရဲ့ Telegram ID ကို ထည့်ပါ (Admin သာ Broadcast လုပ်နိုင်ရန်)

# Bot ထဲ ရောက်လာဖူးသူများရဲ့ ID များကို သိမ်းဆည်းရန် Set တစ်ခု
known_users = set()

# /start အမိန့်
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    known_users.add(user.id) # User ရောက်လာတိုင်း သိမ်းထားမည်
    
    welcome_text = (
        f"မင်္ဂလာပါ {user.first_name}!\n\n"
        "🤖 ဤ Bot သည် အလိုအလျောက် ဝန်ဆောင်မှုများနှင့် ကြော်ငြာများကြည့်ရှုရန် ဖန်တီးထားသော Bot ဖြစ်ပါသည်။\n\n"
        "အောက်ပါခလုတ်များကို အသုံးပြုပါ။"
    )
    
    keyboard = [
        [InlineKeyboardButton("📢 ကြော်ငြာများ ကြည့်ရှုရန်", callback_data="view_ads")],
        [InlineKeyboardButton("💰 လက်ကျန်ငွေ စစ်ဆေးရန်", callback_data="check_balance")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Admin သီးသန့်သုံးရန် Broadcast လုပ်နည်း (/broadcast လို့ရေးပြီး ပို့ချင်တဲ့စာ ရိုက်ထည့်ပါ)
# ဥပမာ - /broadcast ယနေ့အတွက် အထူးကြော်ငြာအသစ် ရောက်ပါပြီ!
async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Admin ဟုတ်မဟုတ် စစ်ဆေးခြင်း
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ ဤအမိန့်ကို Admin သာ အသုံးပြုခွင့်ရှိပါသည်။")
        return

    # ပို့မယ့် စာသားကို ယူခြင်း
    message_text = " ".join(context.args)
    if not message_text:
        await update.message.reply_text("⚠️ ကျေးဇူးပြု၍ ပို့လိုသော စာသားကို တွဲလျက် ရိုက်ထည့်ပါ။\nဥပမာ: `/broadcast မင်္ဂလာပါ...`", parse_mode="Markdown")
        return

    success_count = 0
    fail_count = 0

    # Bot ထဲရောက်ဖူးသူ အားလုံးဆီသို့ စာပို့ခြင်း
    for uid in known_users:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 **အထူးကြော်ငြာ / အသိပေးချက်**\n\n{message_text}", parse_mode="Markdown")
            success_count += 1
        except Exception as e:
            fail_count += 1

    await update.message.reply_text(
        f"✅ **Broadcast ပြီးမြောက်ပါပြီ!**\n\n"
        f"📤 အောင်မြင်စွာ ပို့ူနိုင်သူ: {success_count} ဦး\n"
        f"❌ ပို့မရသူ (သို့မဟုတ် Bot ကို Block ထားသူ): {fail_count} ဦး"
    )

# ခလုတ်များအတွက် လုပ်ဆောင်ချက်
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "view_ads":
        text = "📢 လက်ရှိတွင် ကြော်ငြာအသစ်များ မရှိသေးပါ။ ကျေးဇူးပြု၍ ခဏစောင့်ဆိုင်းပေးပါ။"
        keyboard = [[InlineKeyboardButton("⬅️ ပင်မမီနူးသို့", callback_data="main_menu")]]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif query.data == "check_balance":
        text = "💰 သင့်အကောင့်လက်ကျန်ငွေ: **0 ကျပ်**"
        keyboard = [[InlineKeyboardButton("⬅️ ပင်မမီနူးသို့", callback_data="main_menu")]]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif query.data == "main_menu":
        user_name = query.from_user.first_name
        welcome_text = f"မင်္ဂလာပါ {user_name}! ပင်မမီနူးသို့ ပြန်ရောက်ပါပြီ။"
        keyboard = [
            [InlineKeyboardButton("📢 ကြော်ငြာများ ကြည့်ရှုရန်", callback_data="view_ads")],
            [InlineKeyboardButton("💰 လက်ကျန်ငွေ စစ်ဆေးရန်", callback_data="check_balance")]
        ]
        await query.message.edit_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('broadcast', broadcast_message))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("🚀 Broadcast & Ads Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    application.run_polling()
