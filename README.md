# DishboardTracker
 Bot that tracks Dishboard votes

## Create Discord bot account
- Log in on the [Discord website](https://discord.com/)
- Go to the [applications page](https://discord.com/developers/applications)
- Click "New Application"
- Give the application a name and click "Create"
- Go to the "Bot" tab and click "Add Bot"
- You can get the bot token later by going to "Bot" tab and clicking "Copy"

## Invite bot account to your server
- Go to the "OAuth2" tab
- In the "scopes" part select bot
- In the "permissions" part select whatever permissions select the ones you want
- In the "scopes" part click "Copy" and open the URL, select server and confirm

## Installation
- Install [Python (3.6 - 3.8)](https://www.python.org/downloads/)
- Open a command prompt
- Make new folder (`mkdir <foldername>`) and navigate into the folder (`cd <path>`)
- Clone this repo (`git clone https://github.com/CrumblyLiquid/DishboardTracker`)
- Navigate into the DishboardTracker directory (`cd <path>`)
- Install dependencies from requirements.txt (`py -m pip install -r requirements.txt`)
- Rename .env_example to .env and replace "TOKEN HERE" with your bot token

## Setup
- Create roles in your Discord server
- Go into "Settings -> Advanced" and enable Developer Mode
- In bot.py find variable named `roles` on line 28
- For each level add new "[]"
- The first number is the threshold (how much points you need to get the role), the second number is the role ID which you can get by right clicking "Copy ID" on the role in "Server settings -> Roles"
- Example would be [25, 020930103037704010] - User needs 25 bumps to recieve role with ID `020930103037704010`
- Each item has to be separated by `,`

## Run bot
- Make sure you've followed the installation instructions and setup
- Run the bot `py bot.py`

## Commands
Default prefix is `t!` (You can change it on line 35)
- `t!check <member>` - Prints members points
- `t!reset <member>` - Resets members points