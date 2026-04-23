import asyncio
import nest_asyncio
from pyrogram import Client, filters, enums
import g4f
from g4f.client import Client as AIClient

nest_asyncio.apply()

# --- SOZLAMALAR ---
API_ID = 30858730
API_HASH = "25106c9d80e8d8354053c1da9391edb8"
SESSION_STRING = "AgHW3eoAWDXXaXdJX8NT0NgzVkdo2rKEZHtjzcdnoGW-kCsIbAAlLMASRuBmUy2u5XGebAD8Jro6lDU2Att8j50lsdbI2Zna_hKXznC88T4tsBxTnY-Wp3Ph0htYU-8_8wID8YOmvJH16aiTxHDT1qjpB9ic1I3a-DZIlbqDYnPkDdI1Nfw9xLV7DGJDaiexEfQL8cOapVOViSvNKgk-XfIaCPLn2GIQyQDkIx2_ldg18Nw50pU2qSb0EfYdsYSw4bbRVne0vfWDg8jy2OAl4PdXGKCJpb5UWmiXXYBrOoyfcvYha09Ki13leCU3YQLXGz-EXVqdLReiSlaG8mX9GuONGrutpgAAAAHGLuF8AA"
BOT_TOKEN = "8769316813:AAGG_qt2faKYjXq8LxuiQhkBz56fsc6We3s"
GROUPS_ID = -1001549017357 

user_app = Client("user_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
bot_app = Client("official_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
ai_client = AIClient()

STRICT_PROMPT = "Siz aqlli yordamchisiz. Ismingizni aytmang. Faqat savollarga o'zbek tilida qisqa va aniq javob bering."

# --- GURUHDA SALOMLASHISH VA YO'NALTIRISH ---
salom_sozlar = ["salom", "assalom", "qalaysiz", "yordam", "admin", "aloqa", "kim bor"]

@bot_app.on_message(filters.chat(GROUPS_ID) & filters.text)
async def group_handler(client, message):
    text = message.text.lower()
    if any(word in text for word in salom_sozlar):
        await message.reply_text(
            f"Vaalaykum assalom, {message.from_user.mention}!\n\n"
            "Barcha savollar bo'yicha adminga murojaat qiling. "
            "Admin tez orada siz bilan bog'lanadi. 😊"
        )

# --- BOT SHAXSIYIDAGI AI AMALLARI (OLDINGIDEK) ---
@bot_app.on_message(filters.private & filters.text)
async def bot_private_ai(client, message):
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    try:
        response = ai_client.chat.completions.create(
            model=g4f.models.default,
            messages=[{"role": "system", "content": STRICT_PROMPT}, {"role": "user", "content": message.text}]
        )
        await message.reply_text(response.choices[0].message.content)
    except:
        await message.reply_text("Hozirda AI xizmati band. Birozdan so'ng yozing.")

# --- USERBOT SHAXSIYIDAGI AI AMALLARI (OLDINGIDEK) ---
@user_app.on_message(filters.private & ~filters.me & filters.text)
async def user_private_ai(client, message):
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    try:
        response = ai_client.chat.completions.create(
            model=g4f.models.default,
            messages=[{"role": "system", "content": STRICT_PROMPT}, {"role": "user", "content": message.text}]
        )
        await message.reply_text(response.choices[0].message.content)
    except:
        pass # Shaxsiyda xato bersa indamaydi

# --- ISHGA TUSHIRISH ---
async def start_all():
    await user_app.start()
    await bot_app.start()
    print("Tayyor! Guruhda navbatchilik, bot va profilingizda AI faol.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_all())
    
