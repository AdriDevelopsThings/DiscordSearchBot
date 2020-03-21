# DiscordSearchBot
OpenSource DiscordBot

Get the bot on your server: https://discordapp.com/api/oauth2/authorize?client_id=677860409146867733&permissions=88128&scope=bot

**Please fork for contribution**

## Install

#### Raw
1. ``git clone https://github.com/YourUserName/DiscordSearchBot``
2. ``cd DiscordSearchBot``
3. ``pipenv install`` (install pipenv with ``pip install pipenv``)
4. run the programm with ``pipenv run python run.py`` (Configure the settings with environment variables (infos in the ressources/config.py oder docker-compose.yml))

#### Or use Docker
**Set the DISCORD_BOT_TOKEN and GOOGLE_API_TOKEN in the docker-compose.yml**

**Do not upload your customized docker-compose file to github**
1. ``docker-compose pull``
2. ``docker-compose build``
3. ``docker-compose up -d``

## Tokens and configuration

### MySQL or MariaDB

Please set following mysql environment variables:
1. DB_HOST
2. DB_PORT
3. DB_USER
4. DB_PASSWORD
5. DB_NAME

### Api and bot tokens

1. GOOGLE_API_TOKEN (get your api key here: https://developers.google.com/custom-search/v1/overview)
2. BOT_TOKEN (get your bot token here: https://discordapp.com/developers)

##### And your Google CX keys

Google CX is a customized search. You can create this keys here: https://cse.google.com/cse/all (sometimes you can get an error 500).
In this console you can configure the search_query (say google on what websites google search. for example: *.stackoverflow.com).

### Other environment variables
LOG_GUILD = The guild id of your log server

LOG_CHANNEL = The id of the log channel (The channel must be on the LOG_GUILD)

You can set the LOG_GUILD and LOG_CHANNEL to null or dont set this environments to disable the log feature

## Contribution

If you would like to contribute to our open source project, use this checklist step by step:

1. fork our project
2. Develop your changes
3. test it
4. if you are ready, push it to development on your fork
5. create pull request from your fork (development branch) to our project (development branch).
Please describe your changes in the merge request to make it easier for us to check your code.
When your code is okay, we merge your pull request.

Please come to our discord server so we can ask you questions, if we have questions.

## Social Media

We have a own discord server: https://discord.gg/2p8uvTD (please join us and help us :D)
