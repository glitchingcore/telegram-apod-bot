# Telegram APOD Bot

This is a simple Telegram Bot that sends the Astronomy Picture Of the Day to a Telegram channel every day.

See it in action on a Telegram channel: [@apod_nasapy](https://t.me/apod_nasapy)

# Used technology

- Python 3.10;
- requests
- Docker

# Installation

Clone the git repository into a directory of your choice.

Grab `env_dist` file, rename it into `.env` and put it next to `Dockerfile` (project root directory), open and input the necessary data. Make sure to input the right Telegram channel username and add your bot to the channel with permission to send posts.

Open a terminal in the project root directory and run:

```
docker build -t telegram-apod-bot .
```

After building the docker image run it:

```
docker run telegram-apod-bot
```
