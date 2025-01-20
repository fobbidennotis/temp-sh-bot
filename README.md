
# Temp.sh Telegram bot wrapper

Just a super-simple wrapper that allows simple and fast upload of files to [temp.sh](https://temp.sh)

## Current functionality

### Commands:

/wrap - must be sent as a reply to message that contains the file you want to upload. Returns a link. Only supports files up to 20MB because of the [Telegram API limit](https://core.telegram.org/bots/api#getfile).

## Running

### Make a .env file that contains:

```bash
export TELEGRAM_BOT_TOKEN="token"
```
replace "token" with token your retrieved from BotFather

### Then use poetry PM to run:


Install dependencies:
```bash
poetry install
```
Set enviroment variables:
```bash
source .env
```
Run with poetry:
```bash
poetry run python3 main.py
```
