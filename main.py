import asyncio
import logging
import os
from aiogram import Bot
from vkbottle.user import User, Message

VK_TOKEN = os.getenv("VK_TOKEN")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = int(os.getenv("TG_CHAT_ID", "-1004326605635"))

logging.basicConfig(level=logging.INFO)

tg_bot = Bot(token=TG_BOT_TOKEN)
vk_user = User(token=VK_TOKEN)

@vk_user.on.message()
async def vk_message_handler(message: Message):
    sender = await message.get_user()
    sender_name = f"{sender.first_name} {sender.last_name}"
    text_content = message.text or "[Вложение/Медиа]"
    
    formatted_text = (
        f"📩 **Новое сообщение из ВК**\n"
        f"👤 **От:** {sender_name}\n"
        f"💬 **Текст:** {text_content}"
    )
    
    try:
        await tg_bot.send_message(
            chat_id=TG_CHAT_ID,
            text=formatted_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Ошибка отправки в Telegram: {e}")

async def main():
    print("Бот запущен...")
    await vk_user.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
