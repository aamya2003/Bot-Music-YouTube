
# 🎵 Telegram Group Music Bot with Voice Call Support

A powerful and unique music bot for Telegram that streams songs directly into **group voice chats**, with advanced features not found in other bots. This bot searches for songs on **YouTube** and plays them seamlessly in the group call.

---

## 🚀 Features

- ✅ **Stream Music** in Telegram group voice calls.
- 🔍 **Search YouTube** for songs and play them instantly.
- 🧠 **Smart Features** not available in other music bots.
- 👥 **Works in Groups** – not private chats.
- 🔐 Requires admin permissions:
  - `Delete messages`
  - `Add users`

---

## 🛠️ Setup Instructions

### 1. Requirements

Before running the bot, make sure you have:

- `API_ID` – from [my.telegram.org](https://my.telegram.org/)
- `API_HASH` – from [my.telegram.org](https://my.telegram.org/)
- `BOT_TOKEN` – from [BotFather](https://t.me/BotFather)
- `Your_Id` – from [@myidbot](https://t.me/myidbot)
- (Optional) `mych` – your channel username if you want to broadcast updates

---

### 2. Install Required Libraries

Install the required Python libraries using:

```bash
pip install -r requirements.txt
```

---

### 3. Configuration

Open the `main.py` file and fill in your details:

```python
API_ID = "your_api_id"
API_HASH = "your_api_hash"
bot_token = "your_bot_token"
Your_Id = "your_id"
mych = "your_channel_username"  # optional
```

---

### 4. Run the Bot

Once configured, simply run:

```bash
python main.py
```

The bot will join the voice chat in the group and wait for your commands.

---

## 📌 Notes

- Make sure the bot is an **admin** in the group with **delete** and **invite** permissions.
- This bot uses a **user account (session)** to join the call – don’t use it in more than one group simultaneously unless handled properly.
- Compatible with Pyrogram and pytgcalls.

---

## 🤖 Commands

> You can document available commands here, like:
- `رن [song name]` – Search and play a song
- `/leave` – Stop music
- `/skip` – Skip current song

> To learn more, use:
- `الصوتيه` – Show more available commands

---

## 🧑‍💻 Developer

Created with ❤️ by [Ahmed Asaad](https://t.me/procreem)  
From Iraq 🇮🇶

---

## ⚠️ Common Issues

### ❌ Error: Authentication Required

If you encounter this error while trying to play a YouTube video:

```
ERROR: [youtube] VIDEO_ID: Sign in to confirm you’re not a bot. Use --cookies-from-browser or --cookies for the authentication.
```

This usually happens because **YouTube restricts some formats**, especially for non-logged-in users or on certain platforms (e.g., Ubuntu server).

### ✅ Solution: Use YouTube Cookies

You need to provide a `cookies.txt` file to yt-dlp so it can access the video formats available to your logged-in session.

Update your `yt_dlp.YoutubeDL` options like this:

```python
options = {
    'quiet': True,
    'noplaylist': True,
    'skip_download': True,
    'cookiefile': 'cookies.txt',  # 👈 Required to access restricted formats
    'format': 'bestaudio[ext=m4a]/bestaudio/best',
}
```

---

## 🔐 How to Get `cookies.txt`

Follow these steps to export your YouTube cookies from your browser:

### 1. Use an Extension (easiest)

Install this extension in Chrome or Firefox:

🔗 [Get cookies.txt Extension](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

1. Open YouTube in your browser (you must be logged in).
2. Click the extension icon.
3. Click `Export` to download your cookies.
4. Save the file as `cookies.txt` in your bot directory.

---

### ❌ Error: Requested Format is Not Available

If you encounter this error:

```
Requested format is not available. Use --list-formats for a list of available formats
```

This usually means that your version of `yt-dlp` is outdated, or YouTube has changed their format structure.

### ✅ Solution: Update yt-dlp

Update `yt-dlp` to the latest version with the following command:

```bash
pip install -U yt-dlp
```

---

## 📜 License

This project is open-source and free to use under the [MIT License](LICENSE).
