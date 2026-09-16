# Gold Academy

Gold Academy is a Telegram-native educational bot about gold, XAUUSD, market concepts, and common financial terminology.

The bot deliberately focuses on **three complete user functions** rather than a large collection of partial tools:

1. **Gold Guide** — short lessons about gold and XAUUSD.
2. **Market Lessons** — core concepts such as supply and demand, inflation, interest rates, and market structure.
3. **Glossary** — concise definitions of common financial terms.

The bot does not provide trade signals, personalized financial recommendations, price forecasts, guaranteed returns, payments, broker access, or external redirects.

## Commands

- `/start` — open the main menu.
- `/help` — explain the three functions and navigation.

Telegram deep-link start payloads are accepted by the standard `/start` handler and do not change the destination experience.

## Environment

Required:

```text
BOT_TOKEN=your_bot_token_from_botfather
```

Optional:

```text
LOG_LEVEL=INFO
```

Never commit a real bot token or other credentials.

## Run locally

```bash
python -m pip install -r requirements.txt
BOT_TOKEN=your_token python bot.py
```

On Windows PowerShell:

```powershell
$env:BOT_TOKEN="your_token"
python bot.py
```

## Docker

```bash
docker build -t gold-academy .
docker run --rm -e BOT_TOKEN="$BOT_TOKEN" gold-academy
```

## Render

Deploy this repository as a **Background Worker**. The included `render.yaml` uses:

```text
python bot.py
```

Set `BOT_TOKEN` in the Render environment. Do not put the token in GitHub.

## QA

Run the standard-library checks with:

```bash
python -m unittest discover -s tests -v
```

The checks validate source compilation, the three-button main menu contract, supported commands, and callback coverage.

## Telegram Ads destination readiness

The implementation is designed as a genuine Telegram-native destination: the bot has original educational content, a clear main menu, working callbacks, back navigation, command responses, invalid-input handling, and no redirect-only flow.

Telegram's current guidelines state that promoted bots must be functional, technically complete, active, beneficial to users, and responsive to commands on mobile and desktop. Telegram also requires promoted bots to have a profile image and complete About/Description text. citeturn0search0

Code cannot guarantee approval. Before resubmitting an ad, manually verify the live bot account, profile image, About/Description, username, language, and every visible interaction. The advertisement should describe the same educational product users encounter after clicking.
