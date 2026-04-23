import asyncio
import nest_asyncio
from pyrogram import Client, filters, enums
import g4f
from g4f.client import Client as AIClient

# Asinxron muammolarni tuzatish
nest_asyncio.apply()

# --- SOZLAMALAR ---
API_ID = 30858730
API_HASH = "25106c9d80e8d8354053c1da9391edb8"
SESSION_STRING = "AgHW3eoAWDXXaXdJX8NT0NgzVkdo2rKEZHtjzcdnoGW-kCsIbAAlLMASRuBmUy2u5XGebAD8Jro6lDU2Att8j50lsdbI2Zna_hKXznC88T4tsBxTnY-Wp3Ph0htYU-8_8wID8YOmvJH16aiTxHDT1qjpB9ic1I3a-DZIlbqDYnPkDdI1Nfw9xLV7DGJDaiexEfQL8cOapVOViSvNKgk-XfIaCPLn2GIQyQDkIx2_ldg18Nw50pU2qSb0EfYdsYSw4bbRVne0vfWDg8jy2OAl4PdXGKCJpb5UWmiXXYBrOoyfcvYha09Ki13leCU3YQLXGz-EXVqdLReiSlaG8mX9GuONGrutpgAAAAHGLuF8AA"

app = Client(
    "ai_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# AI Clientni yaratishda xatoliklarni kamaytirish uchun modelni dinamik tanlaymiz
ai_client = AIClient()

print("--- Userbot Railway-da ISHLAMOQDA! ---")

@app.on_message(filters.private & ~filters.me & filters.text)
async def ai_handler(client, message):
    try:
        # Typing status yuborish
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        
        # AI dan javob olish - bir nechta modelni sinab ko'rish (Fallback)
        try:
            response = ai_client.chat.completions.create(
                model=g4f.models.default, # Eng yaxshi ishlaydigan modelni avtomatik tanlaydi
                messages=[
                    {"role": "system", "content": "Siz aqlli yordamchisiz. O'zbek tilida qisqa javob bering."},
                    {"role": "user", "content": message.text}
                ]
            )
            answer = response.choices[0].message.content
        except Exception:
            # Agar default model xato bersa, muqobil modelni sinaymiz
            response = ai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.text}]
            )
            answer = response.choices[0].message.content

        if answer and len(answer) > 0:
            await asyncio.sleep(1)
            await message.reply_text(answer)
        else:
            print("AI bo'sh javob qaytardi.")

    except Exception as e:
        print(f"Xatolik: {e}")
        # Server bloklangan bo'lsa yoki boshqa xatolikda foydalanuvchiga bildirish (ixtiyoriy)
        # await message.reply_text("Kechirasiz, hozirda javob berishda texnik muammo yuzaga keldi.")

if __name__ == "__main__":
    app.run()
    
