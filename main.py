import asyncio
from pyrogram import Client, filters
from g4f.client import Client as AIClient

# --- SOZLAMALAR ---
API_ID = 30858730
API_HASH = "25106c9d80e8d8354053c1da9391edb8"
SESSION_STRING = "AgHW3eoAWDXXaXdJX8NT0NgzVkdo2rKEZHtjzcdnoGW-kCsIbAAlLMASRuBmUy2u5XGebAD8Jro6lDU2Att8j50lsdbI2Zna_hKXznC88T4tsBxTnY-Wp3Ph0htYU-8_8wID8YOmvJH16aiTxHDT1qjpB9ic1I3a-DZIlbqDYnPkDdI1Nfw9xLV7DGJDaiexEfQL8cOapVOViSvNKgk-XfIaCPLn2GIQyQDkIx2_ldg18Nw50pU2qSb0EfYdsYSw4bbRVne0vfWDg8jy2OAl4PdXGKCJpb5UWmiXXYBrOoyfcvYha09Ki13leCU3YQLXGz-EXVqdLReiSlaG8mX9GuONGrutpgAAAAHGLuF8AA"

# Clientni ishga tushirish
app = Client(
    "ai_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# AI Client obyektini yaratish
ai_client = AIClient()

print("--- Userbot Railway-da ishga tushdi! ---")

@app.on_message(filters.private & ~filters.me & filters.text)
async def ai_reply(client, message):
    # Chatda yozish holatini ko'rsatish
    await client.send_chat_action(message.chat.id, "typing")
    
    try:
        # AI dan javob so'rash
        # Xatolikni oldini olish uchun modelni aniq ko'rsatamiz
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Siz aqlli va foydali yordamchisiz. O'zbek tilida qisqa javob bering."},
                {"role": "user", "content": message.text}
            ]
        )
        
        # Javob matnini olish (Xatolikka chidamli usul)
        if hasattr(response.choices[0].message, 'content'):
            answer = response.choices[0].message.content
        else:
            answer = str(response.choices[0].message)

        # Telegramga javobni yuborish
        await message.reply_text(answer)

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        # Agar AI xato bersa, bot to'xtab qolmasligi uchun zaxira javob
        await message.reply_text("Hozirda biroz bandman, keyinroq javob beraman.")

if __name__ == "__main__":
    app.run()
    
