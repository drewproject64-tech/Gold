import asyncio
import logging
import os
from html import escape

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
logger = logging.getLogger(__name__)

BOT_COMMANDS = [
    ("start", "Open the Gold Academy"),
    ("help", "Show how to use the bot"),
]

HOME_TEXT = (
    "<b>🟡 Gold Academy</b>\n\n"
    "A Telegram-native learning guide to gold, markets, and common financial terms.\n\n"
    "Choose one of the three sections below. Each section contains short, "
    "self-contained lessons you can open and revisit.\n\n"
    "Educational information only. No trade signals, forecasts, personalized "
    "recommendations, or promises of financial returns."
)

GOLD_TOPICS = {
    "gold_basics": (
        "Gold Basics",
        "Gold is a precious metal used in jewelry, technology, industry, and "
        "official reserves. Its market is global and prices can change as "
        "economic and market conditions change.",
    ),
    "xauusd": (
        "XAUUSD",
        "XAU is the standard market symbol for one troy ounce of gold, while "
        "USD is the US dollar. XAUUSD is therefore commonly used to describe "
        "the gold price quoted in US dollars per troy ounce.",
    ),
    "gold_factors": (
        "What Can Affect Gold Prices",
        "Gold prices can be discussed in relation to interest rates, inflation "
        "expectations, currency conditions, investment demand, central-bank "
        "activity, supply, and broader market conditions. These factors do not "
        "guarantee a particular future price movement.",
    ),
    "gold_history": (
        "Gold Through History",
        "Gold has served cultural, monetary, and reserve roles across many "
        "civilizations. Modern gold markets developed alongside international "
        "trade, monetary systems, and financial institutions.",
    ),
}

MARKET_TOPICS = {
    "supply_demand": (
        "Supply and Demand",
        "Supply describes how much of a good producers are willing and able to "
        "provide. Demand describes how much buyers are willing and able to "
        "purchase. Market prices can change as these conditions change.",
    ),
    "inflation": (
        "Inflation",
        "Inflation is a sustained increase in the general level of prices over "
        "time. It is commonly measured using price indexes and can influence "
        "household spending, business costs, and economic policy.",
    ),
    "interest_rates": (
        "Interest Rates",
        "An interest rate is the cost of borrowing or the return associated "
        "with lending or saving. Central banks use policy rates and other tools "
        "to influence financial and economic conditions.",
    ),
    "market_structure": (
        "Market Structure",
        "Market structure describes how buyers, sellers, orders, and price "
        "formation interact. Price charts show historical market activity; "
        "they do not establish what will happen next.",
    ),
}

GLOSSARY = {
    "commodity": "A standardized basic good that can be bought and sold, such as certain metals or agricultural products.",
    "currency": "A medium of exchange issued or recognized as money within an economy.",
    "gdp": "Gross domestic product, a measure of the value of final goods and services produced within an economy over a period.",
    "central_bank": "An institution responsible for monetary policy and other functions within a country's financial system.",
    "inflation": "A sustained increase in the general level of prices over time.",
    "interest_rate": "The cost of borrowing or the return associated with lending or saving.",
    "supply": "The quantity of a good or service that producers are willing and able to provide.",
    "demand": "The quantity of a good or service that consumers are willing and able to purchase.",
    "xauusd": "A common market symbol for the price of one troy ounce of gold quoted in US dollars.",
}


def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🟡 Gold Guide", callback_data="menu:gold")
    kb.button(text="📚 Market Lessons", callback_data="menu:markets")
    kb.button(text="📖 Glossary", callback_data="menu:glossary")
    kb.adjust(1)
    return kb.as_markup()


def section_keyboard(items, prefix):
    kb = InlineKeyboardBuilder()
    for key, value in items.items():
        kb.button(text=value[0], callback_data=f"{prefix}:{key}")
    kb.button(text="↩️ Main Menu", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


def detail_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="↩️ Main Menu", callback_data="home")
    return kb.as_markup()


def glossary_items():
    return {
        key: (key.replace("_", " ").title(), value)
        for key, value in GLOSSARY.items()
    }


def help_text():
    return (
        "<b>How to use Gold Academy</b>\n\n"
        "🟡 <b>Gold Guide</b> — learn gold and XAUUSD basics.\n"
        "📚 <b>Market Lessons</b> — review core market and economic concepts.\n"
        "📖 <b>Glossary</b> — look up common financial terms.\n\n"
        "Tap any topic to read it, then use Main Menu to return.\n\n"
        "Commands:\n"
        "/start — open the main menu\n"
        "/help — show this help\n\n"
        "All content is general educational information."
    )


async def send_home(message: Message):
    await message.answer(HOME_TEXT, reply_markup=main_menu())


@router.message(CommandStart())
async def start_handler(message: Message):
    try:
        # CommandStart accepts Telegram deep-link payloads. The payload is
        # intentionally ignored so /start and /start <payload> reach the
        # same safe, complete destination experience.
        await send_home(message)
    except Exception:
        logger.exception("Failed to process /start")
        await message.answer(
            "The main menu could not be opened. Please try /start again."
        )


@router.message(Command("help"))
async def help_handler(message: Message):
    try:
        await message.answer(help_text(), reply_markup=main_menu())
    except Exception:
        logger.exception("Failed to process /help")


@router.callback_query(F.data == "home")
async def home_callback(callback: CallbackQuery):
    await callback.answer()
    try:
        if callback.message:
            await callback.message.edit_text(HOME_TEXT, reply_markup=main_menu())
    except Exception:
        logger.exception("Failed to return to main menu")
        if callback.message:
            await callback.message.answer(HOME_TEXT, reply_markup=main_menu())


@router.callback_query(F.data == "menu:gold")
async def gold_menu_callback(callback: CallbackQuery):
    await callback.answer()
    try:
        if callback.message:
            await callback.message.edit_text(
                "<b>🟡 Gold Guide</b>\n\nChoose a topic:",
                reply_markup=section_keyboard(GOLD_TOPICS, "gold"),
            )
    except Exception:
        logger.exception("Failed to open Gold Guide")


@router.callback_query(F.data == "menu:markets")
async def markets_menu_callback(callback: CallbackQuery):
    await callback.answer()
    try:
        if callback.message:
            await callback.message.edit_text(
                "<b>📚 Market Lessons</b>\n\nChoose a topic:",
                reply_markup=section_keyboard(MARKET_TOPICS, "market"),
            )
    except Exception:
        logger.exception("Failed to open Market Lessons")


@router.callback_query(F.data == "menu:glossary")
async def glossary_menu_callback(callback: CallbackQuery):
    await callback.answer()
    try:
        if callback.message:
            await callback.message.edit_text(
                "<b>📖 Glossary</b>\n\nChoose a term:",
                reply_markup=section_keyboard(glossary_items(), "glossary"),
            )
    except Exception:
        logger.exception("Failed to open Glossary")


@router.callback_query(F.data.startswith("gold:"))
async def gold_topic_callback(callback: CallbackQuery):
    await callback.answer()
    key = (callback.data or "").split(":", 1)[1]
    topic = GOLD_TOPICS.get(key)
    if not topic:
        if callback.message:
            await callback.message.answer(
                "That topic is unavailable. Please return to the main menu.",
                reply_markup=main_menu(),
            )
        return
    title, body = topic
    try:
        if callback.message:
            await callback.message.edit_text(
                f"<b>{escape(title)}</b>\n\n{escape(body)}",
                reply_markup=detail_keyboard(),
            )
    except Exception:
        logger.exception("Failed to open gold topic: %s", key)


@router.callback_query(F.data.startswith("market:"))
async def market_topic_callback(callback: CallbackQuery):
    await callback.answer()
    key = (callback.data or "").split(":", 1)[1]
    topic = MARKET_TOPICS.get(key)
    if not topic:
        if callback.message:
            await callback.message.answer(
                "That lesson is unavailable. Please return to the main menu.",
                reply_markup=main_menu(),
            )
        return
    title, body = topic
    try:
        if callback.message:
            await callback.message.edit_text(
                f"<b>{escape(title)}</b>\n\n{escape(body)}",
                reply_markup=detail_keyboard(),
            )
    except Exception:
        logger.exception("Failed to open market lesson: %s", key)


@router.callback_query(F.data.startswith("glossary:"))
async def glossary_term_callback(callback: CallbackQuery):
    await callback.answer()
    key = (callback.data or "").split(":", 1)[1]
    body = GLOSSARY.get(key)
    if not body:
        if callback.message:
            await callback.message.answer(
                "That term is unavailable. Please return to the main menu.",
                reply_markup=main_menu(),
            )
        return
    title = key.replace("_", " ").title()
    try:
        if callback.message:
            await callback.message.edit_text(
                f"<b>{escape(title)}</b>\n\n{escape(body)}",
                reply_markup=detail_keyboard(),
            )
    except Exception:
        logger.exception("Failed to open glossary term: %s", key)


@router.callback_query()
async def unknown_callback(callback: CallbackQuery):
    await callback.answer("That option is no longer available.", show_alert=True)
    logger.warning("Unknown callback received: %r", callback.data)


@router.message()
async def fallback_handler(message: Message):
    try:
        await message.answer(
            "Please use the three buttons below to explore Gold Academy.",
            reply_markup=main_menu(),
        )
    except Exception:
        logger.exception("Failed to process fallback message")


async def configure_bot(bot: Bot):
    await bot.set_my_commands(
        [BotCommand(command=command, description=description) for command, description in BOT_COMMANDS]
    )


async def main():
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
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
    await configure_bot(bot)
    logger.info("Gold Academy bot started")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Gold Academy bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
