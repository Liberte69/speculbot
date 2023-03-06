#
# This project is meant to run on a Raspberry Pi 4
#

FROM python:3.9.2

WORKDIR /home/${USER}/speculbot

# Paths
ENV BOT_CONFIG_FILE=$PWD/bot_config.env
ENV BOT_TOKEN_FILE=$PWD/token.json
ENV DATA_PATH=$PWD/data

# Constants
ENV DEFAULT_BOTNAME=SpeculBot
ENV DEFAULT_DISCORD_PREFIX=$

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY LICENSE ./
COPY README.md ./

WORKDIR /home/${USER}/speculbot/src

COPY src ./

CMD [ "python", "./app.py" ]
