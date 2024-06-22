# Telegram User Bot Mailer 
**Userbot for mailing in your chats** written in **Pyrogram** + library for middlewares **Pyrogram-patch**.
Database **SQLite** + **SQLAlchemy** (aiosqlite) for storing account data, chats and mailing history.

# ❗️ Important information ❗️
**The developer does not support intrusive spam in chats and does not recommend using it for bad purposes.
Use bot exclusively for good purposes, for example: sending messages to your chats, chats for services.
The bot must not violate the TOS**

## 🔎 Functionality
+ **Installing text in the mailing**, support for **HTML formatting**.
+ **Setting the interval** between sending a message in seconds.
+ **Parsing of all chats** (supergroup/group), does not affect the personal account and archive.
+ Get information about your current or any other account from anywhere in «**Saved Messages**».
+ Basic protection against invalid chats (deleted chat, kicked/banned). Automatically deletes it from the database.
+ Detailed statistics about the mailing: the time spent on the mailing, the number of successful chats, the number of unsuccessful chats.

## ⬇️ Installation (Ubuntu/Linux/Windows)
1. Install the virtual environment with **Python >= 3.11** with the command: `python -m venv .venv`
2. Activate virtual environment with the command: `source .venv/bin/activate` or `.venv/Scripts/activate`
3. Install the necessary libraries with the command: `pip install -r requirements.txt `
4. Go to **[Telegram's official website](https://my.telegram.org/apps )** to create application and get `API_ID` and `API_HASH` from there
5. Go to the `core` folder, find and change the file name `.env.dist` to `.env`
6. In this file, set the values of `API_ID` and `API_HASH` to your own, obtained from the site. The `session_name` variable is optional, this will be the name of your session with the account.
7. Run **migrations to create tables** in the database with the command: `alembic upgrade head`
8. Run the bot with the command: `python main.py ` and follow the **further instructions from Pyrogram** if you are creating a session for the first time.

## 📝 Spammer management (in «Saved Messages»)
+ `start` | `start Test Mailing` is the command to **start mailing**, after which you need to **set your text**.
+ `info` | `info 00000` — displays **information about the current account**, for information about another account after the command, specify its **User ID**
+ `interval` | `interval 5` — sets the interval between sending a message in seconds.
+ `parse` — parses all chats (supergroup/group), except those that are archived.
+ `help` — displays information **about the commands and functionality** of the bot.

## 📌 TODO
+ [ ] Integration of **APScheduler**, a full-fledged task scheduler. It will give you the opportunity to flexibly manage the launched newsletter.
+ [ ] **GUI interface**
  + [ ] **Selective** chat mailing list.
  + [ ] **Multi-accounts**.


**[Contact me on Telegram](https://t.me/kesevone )**