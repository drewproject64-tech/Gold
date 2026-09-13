# Gold Pro Trader

Gold Pro Trader is a Telegram bot focused on gold and forex market education, terminology, basic calculators, and general market information.

## Features

- Simple `/start`, `/help`, `/about`, and `/privacy` commands
- Persistent reply-keyboard main menu
- Gold/XAUUSD educational overview
- Trading lessons: candlesticks, market structure, support/resistance, technical and fundamental analysis, psychology, and risk management
- Trading glossary
- Basic educational calculators
- Trading-session and economic-event explainers
- No broker credentials, passwords, or payment information requested
- Educational disclaimer throughout the experience

## Deploy

### Environment variable

Set:

```text
BOT_TOKEN=your_bot_token_from_botfather
```

### Docker

```bash
docker build -t gold-pro-trader .
docker run --rm -e BOT_TOKEN="$BOT_TOKEN" gold-pro-trader
```

### Render

Create a **Background Worker** or other continuously running service from this repository and set the environment variable `BOT_TOKEN` to the value supplied by BotFather. The included Dockerfile runs the bot with Python 3.12.

## Telegram Ads readiness

The bot is designed as a genuine informational destination rather than a thin redirect. It avoids guaranteed-profit claims, fake performance claims, forced redirects, and requests for sensitive financial credentials.

Before advertising, verify the live bot manually: every button should work, the username should be correct, the profile/about text should be complete, and any external market data should be accurate and up to date.

Approval is ultimately determined by Telegram and cannot be guaranteed by the code alone.
