import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from telegraph import Telegraph
import wikipediaapi

API_TOKEN = "7381074902:AAEpR28Q9HDGDd0dYfQ4yAJqFPTSRzM2xos"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

telegraph = Telegraph()
telegraph.create_account(short_name='WikiBot')

wiki = wikipediaapi.Wikipedia(language='fa', user_agent='WikiTeleBot/1.0 (https://t.me/YourBot)')

@dp.inline_query()
async def inline_wiki_handler(inline_query: types.InlineQuery):
    query = inline_query.query.strip()
    results = []

    if not query:
        return

    page = wiki.page(query)
    if page.exists():
        title = page.title
        content = page.text

        # ساخت صفحه تلگراف (می‌تونی برای عکس‌ها و صداها هم اضافه کنی)
        response = telegraph.create_page(
            title=title,
            html_content=f"<p>{content}</p>"
        )
        page_url = 'https://telegra.ph/' + response['path']

        results.append(
            InlineQueryResultArticle(
                id='1',
                title=f"📘 {title}",
                description="نمایش لینک صفحه در تلگراف",
                input_message_content=InputTextMessageContent(
                    message_text=f"📖 [{title}]({page_url})",
                    parse_mode="Markdown"
                )
            )
        )
    else:
        results.append(
            InlineQueryResultArticle(
                id='2',
                title="❌ مقاله‌ای پیدا نشد",
                description="هیچ نتیجه‌ای برای این عبارت یافت نشد.",
                input_message_content=InputTextMessageContent(
                    message_text="هیچ مقاله‌ای پیدا نشد."
                )
            )
        )

    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())