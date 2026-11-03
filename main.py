import logging
import os
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Conversation States (ရဲတပ်သားသစ် လျှောက်လွှာအတွက် အဆင့်များ)
NAME, AGE, NRC, ADDRESS, FATHER, MOTHER, HEIGHT, WEIGHT, EDUCATION = range(9)

# ⚠️ ကိုယ့်ရဲ့ တကယ့် Telegram Chat ID ကို ထည့်ပါ
ADMIN_CHAT_ID = 123456789  # <--- ကိုယ့် ID အမှန်ထည့်ပါ

EXCEL_FILE = "recruitment_applications.xlsx"
USERS_FILE = "bot_users.txt"
GROUPS_FILE = "bot_groups.txt"

def save_user_id(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write(str(user_id) + "\n")
    else:
        with open(USERS_FILE, "r") as f:
            users = f.read().splitlines()
        if str(user_id) not in users:
            with open(USERS_FILE, "a") as f:
                f.write(str(user_id) + "\n")

def save_group_id(chat_id):
    if not os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "w") as f:
            f.write(str(chat_id) + "\n")
    else:
        with open(GROUPS_FILE, "r") as f:
            groups = f.read().splitlines()
        if str(chat_id) not in groups:
            with open(GROUPS_FILE, "a") as f:
                f.write(str(chat_id) + "\n")

# /start command (ပင်မ Menu ခလုတ်များပြသခြင်း)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.effective_chat.type
    if chat_type in ["group", "supergroup"]:
        save_group_id(update.effective_chat.id)
    else:
        save_user_id(update.effective_user.id)
    
    keyboard = [
        [InlineKeyboardButton("📰 သတင်းများ", callback_data="news"),
         InlineKeyboardButton("📚 အထွေထွေဗဟုသုတ", callback_data="knowledge")],
        [InlineKeyboardButton("⚖️ ဥပဒေအကြောင်းသိကောင်းစရာ", callback_data="law"),
         InlineKeyboardButton("🛡️ ရဲတပ်ဖွဲ့လုပ်ငန်းတာဝန်များ", callback_data="duties")],
        [InlineKeyboardButton("💪 စွမ်းရည်လေးရပ်", callback_data="skills"),
         InlineKeyboardButton("🚨 ရဲတပ်သားသစ် လျှောက်ထားရန်", callback_data="apply_now")],
        [InlineKeyboardButton("ℹ️ လိုအပ်ချက်များနှင့် စည်းကမ်းများ", callback_data="info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "မင်္ဂလာပါ! မြန်မာနိုင်ငံရဲတပ်ဖွဲ့ ဝင်ရောက်လိုသူများနှင့် သိရှိလိုသူများအတွက် လမ်းညွှန် Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "အောက်ပါ ခလုတ်များမှတစ်ဆင့် လိုအပ်သော အချက်အလက်များကို ရွေးချယ်ကြည့်ရှုနိုင်ပါသည် -"
    )
    
    if update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        
    return ConversationHandler.END

# မီနူးခလုတ်များ နှိပ်သည့်အခါ တုံ့ပြန်ပုံ
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    back_keyboard = [[InlineKeyboardButton("🔙 ပင်မမီနူးသို့ ပြန်သွားရန်", callback_data="back_to_home")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    if query.data == "news":
        await query.message.edit_text(
            "📰 **သတင်းများ**\n\n"
            "မြန်မာနိုင်ငံရဲတပ်ဖွဲ့၏ နောက်ဆုံးရ လှုပ်ရှားမှုများနှင့် သတင်းအချက်အလက်များကို ဤနေရာတွင် တင်ပြပေးသွားမည် ဖြစ်ပါသည်။",
            reply_markup=reply_markup
        )
    elif query.data == "knowledge":
        await query.message.edit_text(
            "📚 **အထွေထွေဗဟုသုတ**\n\n"
            "ပြည်သူများ သိသင့်သိထိုက်သော အထွေထွေဗဟုသုတများနှင့် လုံခြုံရေးဆိုင်ရာ သတိပြုဖွယ်ရာများ။",
            reply_markup=reply_markup
        )
    elif query.data == "law":
        await query.message.edit_text(
            "⚖️ **ဥပဒေအကြောင်းသိကောင်းစရာ**\n\n"
            "• ရာဇသတ်ကြီးဥပဒေ\n"
            "• ရဲအက်ဥပဒေနှင့် လုပ်ထုံးလုပ်နည်းများ\n"
            "• ပြည်သူများ သိရှိလိုက်နာရမည့် အခြေခံဥပဒေဆိုင်ရာ သိကောင်းစရာများ။",
            reply_markup=reply_markup
        )
    elif query.data == "duties":
        await query.message.edit_text(
            "🛡️ **ရဲတပ်ဖွဲ့ဆိုသည်မှာ နှင့် လုပ်ငန်းတာဝန်များ**\n\n"
            "၁။ တရားဥပဒေစိုးမိုးရေး၊ ရပ်ရွာအေးချမ်းသာယာရေးနှင့် တရားဥပဒေဖောက်ဖျက်မှုကို ကာကွယ်တားဆီးရန်။\n"
            "၂။ ပြစ်မှုများကို စုံစမ်းဖော်ထုတ် အရေးယူရန်။\n"
            "၃။ ပြည်သူ့အသက်အိုးအိမ်စည်းစိမ်ကို ကာကွယ်စောင့်ရှောက်ရန်။",
            reply_markup=reply_markup
        )
    elif query.data == "skills":
        await query.message.edit_text(
            "💪 **စွမ်းရည်လေးရပ် (Four Strengths)**\n\n"
            "၁။ **နိုင်ငံရေးစွမ်းရည်:** နိုင်ငံတော်အပေါ် သစ္စာစောင့်သိပြီး မူဝါဒလမ်းစဉ်များကို တိကျစွာ လိုက်နာခြင်း။\n"
            "၂။ **စစ်ရေးစွမ်းရည်:** စည်းကမ်းကောင်းမွန်ပြီး တိုက်စွမ်းရည်၊ ကွပ်ကဲစွမ်းရည် ရှိခြင်း။\n"
            "၃။ **လုပ်ငန်းစွမ်းရည်:** ပေးအပ်ထားသော တာဝန်များကို ကျွမ်းကျင်ပိုင်နိုင်စွာ ထမ်းဆောင်နိုင်ခြင်း။\n"
            "၄။ **စည်းရုံးရေးစွမ်းရည်:** ပြည်သူလူထုနှင့် ပူးပေါင်းဆောင်ရွက်နိုင်စွမ်း ရှိခြင်း။",
            reply_markup=reply_markup
        )
    elif query.data == "info":
        await query.message.edit_text(
            "📋 **လိုအပ်ချက်များနှင့် စည်းကမ်းများ:**\n\n"
            "၁။ ပြည်ထောင်စုသမ္မတ မြန်မာနိုင်ငံသား ဖြစ်ရမည်။\n"
            "၂။ အသက် ၁၈ နှစ်ပြည့်ပြီး ၂၅ နှစ်ထက် မကျော်လွန်ရ။\n"
            "၃။ အနည်းဆုံး အထက်တန်းအောင်မြင်ပြီးသူ ဖြစ်ရမည်။",
            reply_markup=reply_markup
        )
    elif query.data == "back_to_home":
        await start(update, context)

# လျှောက်လွှာစတင်ရန် (Apply Now Handler)
async def apply_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "apply_now":
        await query.message.reply_text("ကျေးဇူးပြု၍ သင်၏ **(၁) အမည်ရင်း** ကို ရိုက်ထည့်ပေးပါ။\n(ဖျက်သိမ်းလိုပါက /cancel ဟု ရိုက်နိုင်သည်)")
        return NAME

# အဆင့်ဆင့် အချက်အလက် ကောက်ယူခြင်း
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("ကျေးဇူးတင်ပါတယ်။ သင့်ရဲ့ **(၂) အသက်** ကို ထည့်ပေးပါ။")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = update.message.text
    await update.message.reply_text("ကျေးဇူးတင်ပါတယ်။ သင့်ရဲ့ **(၃) နိုင်ငံသားစိစစ်ရေးကတ်ပြားအမှတ် (မှတ်ပုံတင်)** ကို ထည့်ပေးပါ။")
    return NRC

async def get_nrc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nrc'] = update.message.text
    await update.message.reply_text("ကျေးဇူးတင်ပါတယ်။ သင်နေထိုင်ရာ **(၄) နေရပ်လိပ်စာ** ကို ထည့်ပေးပါ။")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("ကျေးဇူးတင်ပါတယ်။ သင့်ရဲ့ **(၅) ဖခင်အမည်** ကို ထည့်ပေးပါ။")
    return FATHER

async def get_father(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['father'] = update.message.text
    await update.message.reply_text("ကျေးဇူးတင်ပါတယ်။ သင့်ရဲ့ **(၆) မိခင်အမည်** ကို ထည့်ပေးပါ။")
    return MOTHER

async def get_mother(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mother'] = update.message.text
    await update.message.reply_text("ကျေးဇူးတင်ပါတယ်။ သင့်ရဲ့ **(၇) အရပ်အမြင့်** ကို ထည့်ပေးပါ (ဥပမာ - ၅ ပေ ၈ လက်မ)။")
    return HEIGHT

async def get_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['height'] = update.message.text
    await update.message.reply_text("ကျေးဇူးတင်ပါတယ်။ သင့်ရဲ့ **(၈) ကိုယ်အလေးချိန်** ကို ထည့်ပေးပါ (ဥပမာ - ပေါင် ၁၃၀)။")
    return WEIGHT

async def get_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['weight'] = update.message.text
    await update.message.reply_text("ကျေးဇူးတင်ပါတယ်။ နောက်ဆုံးအနေဖြင့် သင့်ရဲ့ **(၉) ပညာအရည်အချင်း** ကို ထည့်ပေးပါ။")
    return EDUCATION

async def get_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['education'] = update.message.text
    
    user_data = context.user_data
    user_telegram_id = update.effective_user.id
    user_username = update.effective_user.username or "No username"
    
    new_data = {
        "Telegram ID": [user_telegram_id],
        "Username": [f"@{user_username}"],
        "အမည်": [user_data.get('name')],
        "အသက်": [user_data.get('age')],
        "မှတ်ပုံတင်အမှတ်": [user_data.get('nrc')],
        "နေရပ်လိပ်စာ": [user_data.get('address')],
        "ဖခင်အမည်": [user_data.get('father')],
        "မိခင်အမည်": [user_data.get('mother')],
        "အရပ်အမြင့်": [user_data.get('height')],
        "ကိုယ်အလေးချိန်": [user_data.get('weight')],
        "ပညာအရည်အချင်း": [user_data.get('education')]
    }
    
    df_new = pd.DataFrame(new_data)
    
    if os.path.exists(EXCEL_FILE):
        df_old = pd.read_excel(EXCEL_FILE)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.to_excel(EXCEL_FILE, index=False)
    else:
        df_new.to_excel(EXCEL_FILE, index=False)
        
    summary = (
        f"✅ **လျှောက်လွှာတင်သွင်းမှု အောင်မြင်ပါသည်။**\n\n"
        f"👤 အမည်: {user_data.get('name')}\n"
        f"📅 အသက်: {user_data.get('age')}\n"
        f"🪪 မှတ်ပုံတင်: {user_data.get('nrc')}\n"
        f"🏠 နေရပ်လိပ်စာ: {user_data.get('address')}\n"
        f"👨 ဖခင်အမည်: {user_data.get('father')}\n"
        f"👩 မိခင်အမည်: {user_data.get('mother')}\n"
        f"📏 အရပ်အမြင့်: {user_data.get('height')}\n"
        f"⚖️ ကိုယ်အလေးချိန်: {user_data.get('weight')}\n"
        f"🎓 ပညာအရည်အချင်း: {user_data.get('education')}\n\n"
        f"ပင်မမီနူးသို့ ပြန်သွားရန် /start ကို နှိပ်ပါ။"
    )
    await update.message.reply_text(summary)
    
    try:
        admin_message = (
            f"🚨 **လျှောက်လွှာအသစ် ရောက်ရှိပါပြီ။**\n\n"
            f"👤 အမည်: {user_data.get('name')}\n"
            f"📅 အသက်: {user_data.get('age')}\n"
            f"🪪 မှတ်ပုံတင်: {user_data.get('nrc')}\n"
            f"🏠 နေရပ်လိပ်စာ: {user_data.get('address')}\n"
            f"👨 ဖခင်အမည်: {user_data.get('father')}\n"
            f"👩 မိခင်အမည်: {user_data.get('mother')}\n"
            f"📏 အရပ်အမြင့်: {user_data.get('height')}\n"
            f"⚖️ ကိုယ်အလေးချိန်: {user_data.get('weight')}\n"
            f"🎓 ပညာအရည်အချင်း: {user_data.get('education')}\n"
            f"💬 Telegram Username: @{user_username}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    except Exception as e:
        logging.error(f"Admin ထံသို့ စာပို့မရပါ: {e}")
        
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("လျှောက်လွှာတင်ခြင်းကို ဖျက်သိမ်းလိုက်ပါပြီ။ ပင်မမီနူးသို့ သွားရန် /start ကို နှိပ်ပါ။")
    return ConversationHandler.END

# Broadcast Command
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        await update.message.reply_text("ဤ கட்டளைကို Admin သာ အသုံးပြုနိုင်ပါသည်။")
        return

    message_text = " ".join(context.args)
    if not message_text:
        await update.message.reply_text("ကျေးဇူးပြု၍ ပို့လိုသော စာသားကို ထည့်ပါ (ဥပမာ: /broadcast အသိပေးချက်)")
        return

    success_count = 0
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = f.read().splitlines()
        for user_id in users:
            try:
                await context.bot.send_message(chat_id=int(user_id), text=message_text)
                success_count += 1
            except Exception as e:
                logging.error(f"User {user_id} ထံသို့ ပို့မရပါ: {e}")

    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            groups = f.read().splitlines()
        for group_id in groups:
            try:
                keyboard = [[InlineKeyboardButton("🚨 ရဲတပ်သားသစ် လျှောက်ထားရန်", url=f"https://t.me/{context.bot.username}?start=apply")]]
                await context.bot.send_message(chat_id=int(group_id), text=message_text, reply_markup=InlineKeyboardMarkup(keyboard))
                success_count += 1
            except Exception as e:
                logging.error(f"Group {group_id} ထံသို့ ပို့မရပါ: {e}")

    await update.message.reply_text(f"✅ မက်ဆေ့ခ်ျကို လူနှင့် Group စုစုပေါင်း {success_count} ခုထံ ပို့ပြီးပါပြီ။")

# Scheduled Auto-Posting (PTB JobQueue ဖြင့် အလုပ်လုပ်မည်)
async def scheduled_auto_post(context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(GROUPS_FILE):
        return
    with open(GROUPS_FILE, "r") as f:
        groups = f.read().splitlines()
        
    ad_text = (
        "🚨 **မြန်မာနိုင်ငံရဲတပ်ဖွဲ့ ဝင်ရောက်လိုသူများအတွက် လမ်းညွှန် Bot** 🚨\n\n"
        "သတင်းများ၊ ဥပဒေအကြောင်းသိကောင်းစရာများ၊ စွမ်းရည်လေးရပ်နှင့် ရဲတပ်သားသစ် လျှောက်ထားရန် အောက်ပါခလုတ်ကို နှိပ်ပါခင်ဗျာ။"
    )
    for group_id in groups:
        try:
            keyboard = [[InlineKeyboardButton("🤖 Bot သို့ ဝင်ရန်", url=f"https://t.me/{context.bot.username}")]]
            await context.bot.send_message(chat_id=int(group_id), text=ad_text, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception as e:
            logging.error(f"Scheduled post error for group {group_id}: {e}")

if __name__ == '__main__':
    TOKEN = "9165279241:AAG0H_tynn5aED2gaGe9g4z0zw2y_KHNRAw"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Python-Telegram-Bot ၏ Built-in JobQueue ကို အသုံးပြု၍ ၆ နာရီတစ်ကြိမ် ပို့ရန် သတ်မှတ်ခြင်း
    job_queue = application.job_queue
    job_queue.run_repeating(scheduled_auto_post, interval=21600, first=10) # 21600 seconds = 6 hours
    
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(apply_start_handler, pattern="^apply_now$")
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_name)],
            AGE: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_age)],
            NRC: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_nrc)],
            ADDRESS: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_address)],
            FATHER: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_father)],
            MOTHER: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_mother)],
            HEIGHT: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_height)],
            WEIGHT: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_weight)],
            EDUCATION: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_education)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('start', start)],
        per_message=False
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(menu_handler, pattern="^news$|^knowledge$|^law$|^duties$|^skills$|^info$|^back_to_home$"))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("broadcast", broadcast))
    
    print("🤖 အစုံသုံး ရဲတပ်ဖွဲ့ Bot အလုပ်လုပ်နေပါပြီ...")
    application.run_polling()