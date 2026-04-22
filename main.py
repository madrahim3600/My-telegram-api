import os
import asyncio
from pyrogram import Client, filters
from g4f.client import Client as AIClient

# --- SOZLAMALAR ---
API_ID = 30858730
API_HASH = "25106c9d80e8d8354053c1da9391edb8"
# Siz bergan Session String
SESSION_STRING = "AgHW3eoAWDXXaXdJX8NT0NgzVkdo2rKEZHtjzcdnoGW-kCsIbAAlLMASRuBmUy2u5XGebAD8Jro6lDU2Att8j50lsdbI2Zna_hKXznC88T4tsBxTnY-Wp3Ph0htYU-8_8wID8YOmvJH16aiTxHDT1qjpB9ic1I3a-DZIlbqDYnPkDdI1Nfw9xLV7DGJDaiexEfQL8cOapVOViSvNKgk-XfIaCPLn2GIQyQDkIx2_ldg18Nw50pU2qSb0EfYdsYSw4bbRVne0vfWDg8jy2OAl4PdXGKCJpb5UWmiXXYBrOoyfcvYha09Ki13leCU3YQLXGz-EXVqdLReiSlaG8mX9GuONGrutpgAAAAHGLuF8AA"

# Userbotni ishga tushirish
app = Client(
    "ai_userbot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

ai_client = AIClient()

print("Userbot Railway-da ishga tushmoqda...")

@app.on_message(filters.private & ~filters.me & filters.text)
async def ai_auto_reply(client, message):
    """
    Faqat shaxsiy xabarlarga javob beradi. 
    Bot o'zi yozgan xabarlarga javob bermaydi.
    """
    
    # "Yozilmoqda..." statusini ko'rsatish
    await client.send_chat_action(message.chat.id, "typing")
    
    try:
        # AI dan javob olish (Bepul GPT-3.5 modeli)
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Siz aqlli yordamchisiz. O'zbek tilida qisqa va mazmunli javob bering."},
                {"role": "user", "content": message.text}
            ]
        )
        
        answer = response.choices[0].message.content
        
        # Javobni 1 soniya kutib yuborish (tabiiyroq ko'rinishi uchun)
        await asyncio.sleep(1)
        await message.reply_text(answer)

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    app.run()
  
