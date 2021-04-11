# DishboardTracker
 Bot that tracks Dishboard votes

## Installation
- Clone this repo
- Install Python (3.6 - 3.8)
- Install dependencies from requirements.txt `py -m pip install -r requirements.txt`
- Rename .env_example to .env and replace "TOKEN HERE" with your bot token
- Navigate into the DishboardTracker directory
- Run the bot `py bot.py`

## Setup
- Create roles in your Discord server
- Go into "Settings -> Advanced" and enable Developer Mode
- In bot.py find variable named `roles` on line 28
- For each level add new "[]"
- The first number is the threshold (how much points you need to get the role), the second number is the role ID which you can get by right clicking "Copy ID" on the role in "Server settings -> Roles"
- Example would be [25, 020930103037704010] - User needs 25 bumps to recieve role with ID `020930103037704010`
- Each item has to be separated by `,`

## Commands
Default prefix is `t!` (You can change it on line 35)
- `t!check <member>` - Prints members points
- `t!reset <member>` - Resets members points