import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


router = Router()


HOME_TEXT = (
    "<b>🟡 Gold Academy</b>\n\n"
    "A simple educational reference about gold, economics, and financial terminology.\n\n"
    "Explore short lessons, definitions, and general background information in one place.\n\n"
    "⚠️ <b>Educational information only.</b> This bot does not provide financial advice, "
    "trade signals, forecasts, recommendations, or promises of financial returns."
)


LESSONS = {
    "gold": (
        "<b>Gold: An Introduction</b>\n\n"
        "Gold is a precious metal used in jewelry, technology, central-bank reserves, and other applications.\n\n"
        "Its price can be discussed in relation to factors such as interest rates, inflation expectations, "
        "currency conditions, supply and demand, and broader economic conditions.\n\n"
        "This lesson provides general background only."
    ),
    "history": (
        "<b>Gold Through History</b>\n\n"
        "Gold has been used as money, a store of value, jewelry, and a reserve asset across many civilizations.\n\n"
        "Modern gold markets developed alongside changes in monetary systems, international trade, and financial institutions."
    ),
    "economics": (
        "<b>Basic Economics</b>\n\n"
        "Economics studies how people, businesses, and governments make choices about scarce resources.\n\n"
        "Useful concepts include supply and demand, inflation, interest rates, employment, productivity, and economic growth."
    ),
    "inflation": (
        "<b>Inflation</b>\n\n"
        "Inflation describes a sustained increase in the general level of prices over time.\n\n"
        "Inflation is commonly measured using price indexes. Changes in inflation can affect household spending, "
        "business costs, savings, and economic policy."
    ),
    "interest": (
        "<b>Interest Rates</b>\n\n"
        "An interest rate is the cost of borrowing money or the return paid on certain forms of saving and lending.\n\n"
        "Central banks use policy rates and other tools to influence financial and economic conditions."
    ),
    "markets": (
        "<b>How Markets Work</b>\n\n"
        "Markets bring buyers and sellers together. Prices can change as participants respond to information, "
        "supply, demand, expectations, and changing economic conditions.\n\n"
        "Past price movement does not establish what will happen next."
    ),
}

GLOSSARY = {
    "gold": "A precious metal with industrial, cultural, and monetary uses.",
    "inflation": "A sustained increase in the general level of prices.",
    "interest_rate": "The cost of borrowing or the return associated with lending or saving.",
    "supply": "The quantity of a good or service that producers are willing and able to provide.",
    "demand": "The quantity of a good or service that consumers are willing and able to purchase.",
    "gdp": "Gross domestic product, a measure of the value of final goods and services produced within an economy over a period.",
    "currency": "A medium of exchange issued or recognized as money within an economy.",
    "central_bank": "An institution responsible for monetary policy and other functions within a country's financial system.",
    "commodity": "A standardized basic good that can be bought and sold, such as certain metals or agricultural products.",
}


def home_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="🟡 About Gold")
    kb.button(text="📚 Learn")
    kb.button(text="📖 Glossary")
    kb.button(text="ℹ️ About")
    kb.adjust(2, 2)
    return kb.as_markup(resize_keyboard=True, is_persistent=True)


def learn_keyboard():
    kb = InlineKeyboardBuilder()
    items = [
        ("🟡 Gold Basics", "lesson:gold"),
        ("📜 Gold History", "lesson:history"),
        ("🌍 Economics", "lesson:economics"),
        ("📈 Inflation", "lesson:inflation"),
        ("🏦 Interest Rates", "lesson:interest"),
        ("📊 Markets", "lesson:markets"),
        ("↩️ Home", "home"),
    ]
    for label, data in items:
        kb.button(text=label, callback_data=data)
    kb.adjust(2, 2, 2, 1)
    return kb.as_markup()


def glossary_keyboard():
    kb = InlineKeyboardBuilder()
    items = [
        ("Gold", "glossary:gold"),
        ("Inflation", "glossary:inflation"),
        ("Interest Rate", "glossary:interest_rate"),
        ("Supply", "glossary:supply"),
        ("Demand", "glossary:demand"),
        ("GDP", "glossary:gdp"),
        ("Currency", "glossary:currency"),
        ("Central Bank", "glossary:central_bank"),
        ("Commodity", "glossary:commodity"),
        ("↩️ Home", "home"),
    ]
    for label, data in items:
        kb.button(text=label, callback_data=data)
    kb.adjust(2, 2, 2, 2, 1)
    return kb.as_markup()


def back_home_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="↩️ Home", callback_data="home")
    return kb.as_markup()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(HOME_TEXT, reply_markup=home_keyboard())


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "<b>Help</b>\n\n"
        "Use the menu buttons to explore educational topics.\n\n"
        "Commands:\n"
        "/start — Open the main menu\n"
        "/help — Show help\n"
        "/about — About Gold Academy\n"
        "/privacy — Privacy and data note\n\n"
        "The bot provides general educational information only."
    )


@router.message(Command("about"))
@router.message(F.text == "ℹ️ About")
async def about_handler(message: Message) -> None:
    await message.answer(
        "<b>About Gold Academy</b>\n\n"
        "Gold Academy is an educational reference bot covering gold, economics, and financial terminology.\n\n"
        "It provides short lessons and definitions for general learning.\n\n"
        "⚠️ It does not provide financial advice, trade signals, personalized recommendations, "
        "price forecasts, or guaranteed outcomes."
    )


@router.message(Command("privacy"))
async def privacy_handler(message: Message) -> None:
    await message.answer(
        "<b>Privacy</b>\n\n"
        "Gold Academy is designed to minimize data collection. It does not request passwords, "
        "payment details, broker credentials, or private financial account access.\n\n"
        "Telegram may provide basic account and message metadata required for bot operation."
    )


@router.message(F.text == "🟡 About Gold")
async def gold_handler(message: Message) -> None:
    await message.answer(
        "<b>🟡 About Gold</b>\n\n"
        "Learn general facts about gold, its history, economic context, and common terminology.",
        reply_markup=learn_keyboard(),
    )


@router.message(F.text == "📚 Learn")
async def learn_handler(message: Message) -> None:
    await message.answer(
        "<b>📚 Learn</b>\n\nChoose an educational topic:",
        reply_markup=learn_keyboard(),
    )


@router.message(F.text == "📖 Glossary")
async def glossary_handler(message: Message) -> None:
    await message.answer(
        "<b>📖 Glossary</b>\n\nChoose a term:",
        reply_markup=glossary_keyboard(),
    )


@router.callback_query(F.data == "home")
async def cb_home(callback: CallbackQuery) -> None:
    await callback.message.edit_text(HOME_TEXT)
    await callback.message.answer("Main menu", reply_markup=home_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("lesson:"))
async def cb_lesson(callback: CallbackQuery) -> None:
    key = callback.data.split(":", 1)[1]
    text = LESSONS.get(key)
    if not text:
        await callback.answer("Lesson unavailable", show_alert=True)
        return
    await callback.message.edit_text(text, reply_markup=back_home_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("glossary:"))
async def cb_glossary(callback: CallbackQuery) -> None:
    key = callback.data.split(":", 1)[1]
    explanation = GLOSSARY.get(key)
    if not explanation:
        await callback.answer("Term unavailable", show_alert=True)
        return
    title = key.replace("_", " ").title()
    await callback.message.edit_text(
        f"<b>{title}</b>\n\n{explanation}",
        reply_markup=back_home_keyboard(),
    )
    await callback.answer()


@router.message(F.text)
async def fallback_handler(message: Message) -> None:
    await message.answer(
        "Please use the menu below to explore the educational resources.",
        reply_markup=home_keyboard(),
    )


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
