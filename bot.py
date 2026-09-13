import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Optional

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


@dataclass(frozen=True)
class Config:
    token: str


def load_config() -> Config:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")
    return Config(token=token)


router = Router()

HOME_TEXT = (
    "<b>🟡 Gold Pro Trader</b>\n\n"
    "A practical learning and market-information toolkit for gold and forex.\n\n"
    "Explore trading concepts, calculators, terminology, and risk-management education from one place.\n\n"
    "⚠️ <b>Educational information only.</b> Nothing in this bot is a promise of profit or personalized investment advice."
)


# Educational content intentionally avoids return guarantees, trade instructions, or personalized recommendations.
LESSONS = {
    "xauusd": (
        "<b>What is XAUUSD?</b>\n\n"
        "XAUUSD is a commonly quoted market symbol for gold priced in U.S. dollars. "
        "Gold can be influenced by interest rates, inflation expectations, the U.S. dollar, "
        "central-bank activity, and changes in market risk sentiment.\n\n"
        "Use this section to understand terminology and market drivers—not to predict guaranteed outcomes."
    ),
    "candles": (
        "<b>Candlestick Basics</b>\n\n"
        "A candle summarizes open, high, low, and close prices for a selected period. "
        "Traders often study candle bodies, wicks, ranges, and sequences to describe price behavior.\n\n"
        "A pattern is information, not certainty."
    ),
    "levels": (
        "<b>Support & Resistance</b>\n\n"
        "Support and resistance are price areas where market participants may have reacted previously. "
        "They are best treated as zones rather than exact lines, and they can fail or change over time."
    ),
    "structure": (
        "<b>Market Structure</b>\n\n"
        "Market structure describes sequences such as higher highs, higher lows, lower highs, and lower lows. "
        "It is a framework for describing historical price behavior and should not be interpreted as a guarantee of future movement."
    ),
    "risk": (
        "<b>Risk Management</b>\n\n"
        "Risk management aims to limit the impact of adverse trades. Common concepts include position sizing, "
        "risk-per-trade limits, stop-loss planning, diversification, and understanding leverage.\n\n"
        "Consider your own circumstances and risk tolerance before making financial decisions."
    ),
    "psychology": (
        "<b>Trading Psychology</b>\n\n"
        "Common behavioral challenges include overtrading, revenge trading, fear of missing out, and abandoning a plan after a loss. "
        "Keeping records and using predefined rules can help make decisions more consistent."
    ),
    "technical": (
        "<b>Technical Analysis</b>\n\n"
        "Technical analysis uses historical price and volume information to describe market behavior. "
        "Common tools include moving averages, momentum indicators, trend lines, and volatility measures. "
        "No indicator can guarantee an outcome."
    ),
    "fundamental": (
        "<b>Fundamental Analysis</b>\n\n"
        "Fundamental analysis considers economic and financial factors such as interest rates, inflation, employment, "
        "currency conditions, and central-bank policy when evaluating markets."
    ),
}

GLOSSARY = {
    "xauusd": "Gold priced in U.S. dollars.",
    "pip": "A standardized unit commonly used to describe small changes in a forex quote. Exact conventions vary by instrument.",
    "lot": "A standardized trading size. The contract size depends on the instrument and broker.",
    "spread": "The difference between the bid and ask price.",
    "leverage": "A mechanism that allows a position larger than the cash posted as margin. It can increase both potential gains and losses.",
    "stop_loss": "An order or rule intended to close or reduce a position when a specified price condition is reached.",
    "take_profit": "An order or rule intended to close a position when a specified profit-price condition is reached.",
    "drawdown": "A decline from a previous peak in the value of an account or strategy.",
    "margin": "Funds required to support a leveraged position.",
}


def home_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="📊 Market Tools")
    kb.button(text="📚 Learn Trading")
    kb.button(text="🧮 Calculators")
    kb.button(text="📖 Glossary")
    kb.button(text="ℹ️ About")
    kb.adjust(2, 2, 1)
    return kb.as_markup(resize_keyboard=True, is_persistent=True)


def market_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🟡 XAUUSD Overview", callback_data="lesson:xauusd")
    kb.button(text="⏰ Trading Sessions", callback_data="sessions")
    kb.button(text="📅 Economic Events", callback_data="economic")
    kb.button(text="↩️ Home", callback_data="home")
    kb.adjust(1, 2, 1)
    return kb.as_markup()


def learn_keyboard():
    kb = InlineKeyboardBuilder()
    items = [
        ("🕯 Candlesticks", "lesson:candles"),
        ("📏 Support & Resistance", "lesson:levels"),
        ("📈 Market Structure", "lesson:structure"),
        ("🛡 Risk Management", "lesson:risk"),
        ("🧠 Trading Psychology", "lesson:psychology"),
        ("📐 Technical Analysis", "lesson:technical"),
        ("🌐 Fundamental Analysis", "lesson:fundamental"),
        ("🟡 XAUUSD", "lesson:xauusd"),
        ("↩️ Home", "home"),
    ]
    for label, data in items:
        kb.button(text=label, callback_data=data)
    kb.adjust(2, 2, 2, 2, 1)
    return kb.as_markup()


def calculator_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📏 Risk / Reward", callback_data="calc:rr")
    kb.button(text="💰 Position Size", callback_data="calc:position")
    kb.button(text="📐 Percentage", callback_data="calc:percent")
    kb.button(text="↩️ Home", callback_data="home")
    kb.adjust(1, 1, 1, 1)
    return kb.as_markup()


def glossary_keyboard():
    kb = InlineKeyboardBuilder()
    labels = [
        ("XAUUSD", "glossary:xauusd"),
        ("Pip", "glossary:pip"),
        ("Lot", "glossary:lot"),
        ("Spread", "glossary:spread"),
        ("Leverage", "glossary:leverage"),
        ("Stop Loss", "glossary:stop_loss"),
        ("Take Profit", "glossary:take_profit"),
        ("Drawdown", "glossary:drawdown"),
        ("Margin", "glossary:margin"),
        ("↩️ Home", "home"),
    ]
    for label, data in labels:
        kb.button(text=label, callback_data=data)
    kb.adjust(3, 3, 3, 1)
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
        "Use the menu buttons to explore the bot.\n\n"
        "Commands:\n"
        "/start — Open the main menu\n"
        "/help — Show help\n"
        "/about — About Gold Pro Trader\n"
        "/privacy — Privacy and data note\n\n"
        "The bot is designed for educational and informational use."
    )


@router.message(Command("about"))
@router.message(F.text == "ℹ️ About")
async def about_handler(message: Message) -> None:
    await message.answer(
        "<b>About Gold Pro Trader</b>\n\n"
        "Gold Pro Trader is an educational Telegram bot focused on gold and forex market concepts.\n\n"
        "It provides lessons, terminology, calculators, and general market information in a simple interface.\n\n"
        "⚠️ This service does not guarantee profits and does not provide individualized investment advice. "
        "Market information can be incomplete or delayed."
    )


@router.message(Command("privacy"))
async def privacy_handler(message: Message) -> None:
    await message.answer(
        "<b>Privacy</b>\n\n"
        "Gold Pro Trader is designed to minimize data collection. The bot does not ask for passwords, payment details, "
        "broker credentials, or private financial account access.\n\n"
        "Telegram may provide basic account and message metadata necessary for bot operation."
    )


@router.message(F.text == "📊 Market Tools")
async def market_tools_handler(message: Message) -> None:
    await message.answer(
        "<b>📊 Market Tools</b>\n\n"
        "Learn how gold and forex markets are described, review trading-session information, and understand economic events.\n\n"
        "This section is informational and does not provide guaranteed forecasts.",
        reply_markup=market_keyboard(),
    )


@router.message(F.text == "📚 Learn Trading")
async def learn_handler(message: Message) -> None:
    await message.answer(
        "<b>📚 Learn Trading</b>\n\nChoose a topic:",
        reply_markup=learn_keyboard(),
    )


@router.message(F.text == "🧮 Calculators")
async def calculator_handler(message: Message) -> None:
    await message.answer(
        "<b>🧮 Calculators</b>\n\nChoose a simple calculator. Enter only numbers; no financial account information is required.",
        reply_markup=calculator_keyboard(),
    )


@router.message(F.text == "📖 Glossary")
async def glossary_handler(message: Message) -> None:
    await message.answer(
        "<b>📖 Trading Glossary</b>\n\nChoose a term:",
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


@router.callback_query(F.data == "sessions")
async def cb_sessions(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "<b>⏰ Trading Sessions</b>\n\n"
        "Forex activity is commonly discussed using the Asian, London, and New York sessions. "
        "Overlap periods can have different liquidity and volatility characteristics.\n\n"
        "Exact market hours can vary with daylight-saving rules and broker schedules.",
        reply_markup=back_home_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "economic")
async def cb_economic(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "<b>📅 Economic Events</b>\n\n"
        "Economic calendars commonly track releases such as inflation data, employment reports, GDP, interest-rate decisions, "
        "and central-bank statements.\n\n"
        "Major releases can affect market volatility. Always verify the latest schedule using a reputable live calendar.",
        reply_markup=back_home_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("glossary:"))
async def cb_glossary(callback: CallbackQuery) -> None:
    key = callback.data.split(":", 1)[1]
    explanation = GLOSSARY.get(key)
    if not explanation:
        await callback.answer("Term unavailable", show_alert=True)
        return
    title = key.replace("_", " ").upper()
    await callback.message.edit_text(
        f"<b>{title}</b>\n\n{explanation}",
        reply_markup=back_home_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "calc:rr")
async def cb_rr(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "<b>📏 Risk / Reward Calculator</b>\n\n"
        "This calculator helps compare a planned loss amount with a planned gain amount.\n\n"
        "Send: <code>risk reward</code>\n"
        "Example: <code>50 100</code>\n\n"
        "Result: 100 ÷ 50 = 2.0R\n\n"
        "This is a mathematical ratio, not a recommendation to take a trade.",
        reply_markup=back_home_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "calc:position")
async def cb_position(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        "<b>💰 Position Size Calculator</b>\n\n"
        "Send three numbers separated by spaces:\n"
        "<code>account risk% stop_distance</code>\n\n"
        "Example: <code>1000 1 50</code>\n\n"
        "The bot will calculate the cash amount represented by the risk percentage and divide it by the stop distance. "
        "This is a simplified educational calculation; contract specifications differ by instrument and broker.",
        reply_markup=back_home_keyboard(),
    )
    await state.set_state("position")
    await callback.answer()


@router.callback_query(F.data == "calc:percent")
async def cb_percent(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "<b>📐 Percentage Calculator</b>\n\n"
        "Send two numbers:\n"
        "<code>value percentage</code>\n\n"
        "Example: <code>2500 1.5</code>\n\n"
        "Result: 37.50\n\n"
        "Use this for basic educational calculations.",
        reply_markup=back_home_keyboard(),
    )
    await callback.answer()


@router.message(F.text)
async def text_calculator_handler(message: Message, state: FSMContext) -> None:
    current = await state.get_state()
    text = (message.text or "").strip()

    if current == "position":
        parts = text.replace(",", ".").split()
        if len(parts) == 3:
            try:
                account, risk_percent, stop_distance = map(float, parts)
                if account <= 0 or risk_percent < 0 or stop_distance <= 0:
                    raise ValueError
                risk_cash = account * (risk_percent / 100)
                simplified_size = risk_cash / stop_distance
                await message.answer(
                    f"<b>Position Size Result</b>\n\n"
                    f"Risk amount: <code>{risk_cash:.2f}</code>\n"
                    f"Simplified size: <code>{simplified_size:.4f}</code>\n\n"
                    "This is an educational formula and is not a broker-specific lot-size calculation. "
                    "Contract size, tick value, leverage, and instrument specifications can change the real result.",
                    reply_markup=home_keyboard(),
                )
                await state.clear()
                return
            except ValueError:
                pass
        await message.answer("Please send three valid numbers, for example: <code>1000 1 50</code>.")
        return

    # Lightweight calculators from plain chat input.
    parts = text.replace(",", ".").split()
    if len(parts) == 2:
        try:
            a, b = map(float, parts)
            if b != 0:
                ratio = a / b
                percentage = a * (b / 100)
                await message.answer(
                    f"<b>Calculation</b>\n\n"
                    f"Ratio: <code>{ratio:.4f}</code>\n"
                    f"{b:g}% of {a:g}: <code>{percentage:.2f}</code>\n\n"
                    "Use these results as general mathematical information.",
                    reply_markup=home_keyboard(),
                )
                return
        except ValueError:
            pass

    await message.answer(
        "Please use the menu below to explore Gold Pro Trader.",
        reply_markup=home_keyboard(),
    )


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    config = load_config()
    bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    # Remove queued updates so a newly deployed instance starts cleanly.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
