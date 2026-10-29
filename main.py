import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("9037204212:AAGsox9wS3VfP2SsN96dNYLgg-BJWzZEFfU")
ADMIN_ID = 8903953398
CASH_NUMBER = "01110768571"
PRICE = 42.5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👑 اهلا يا ملك في ملوك التمويل\n💵 1000 متابع = {PRICE}ج\n📲 فودافون كاش: {CASH_NUMBER}\n\nابعت: @قناتك المبلغ\nمثال: @mychannel 100")

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        p = update.message.text.split()
        link, total = p[0], float(p[1])
        followers = int(total/PRICE*1000)
        await update.message.reply_text(f"📢 طلبك اتبعت يا ملك! 👑\nدفعت {total}ج 💵\nهيوصلك {followers} متابع 👥\nحول على: {CASH_NUMBER}\n⏳ قيد التنفيذ")
        context.bot_data[f"order_{update.effective_user.id}"] = {"link":link,"total":total,"followers":followers}
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"طلب جديد @{update.effective_user.username}\n{link}\n{total}ج = {followers}\n/approve {update.effective_user.id}")
    except:
        await update.message.reply_text("ابعت بالشكل ده: @القناة المبلغ\nمثال: @test 85")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    uid = int(context.args[0])
    d = context.bot_data.get(f"order_{uid}")
    await context.bot.send_message(chat_id=uid, text=f"✅ تم تنفيذ طلبك! {d['followers']} متابع 👑\n🔗 {d['link']}")
    await update.message.reply_text("تم ✅")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order))
    print("Bot running")
    app.run_polling()

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Koko Bot Running 👑"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
