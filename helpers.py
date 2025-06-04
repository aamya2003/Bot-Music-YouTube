from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from datetime import datetime, timedelta
from pytgcalls import PyTgCalls, idle
from pyrogram import enums, filters, Client
from texts import *
import os, json, re, pyrogram, yt_dlp, random, time, sqlite3, requests





pathdb = "mediaBot/grmus.db"

# لتلعب بيها 
dataMusic= {}
# خليها كما هي



class yUtube_data:
    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id
        self.key = f"{chat_id}:{user_id}"
    def set_value(self, nkey, nvalue):
        if self.key not in dataMusic:
            dataMusic.update(
                {
                    self.key: {
                        nkey: nvalue
                    }
                }
            )
            return
        dataMusic[self.key][nkey] = nvalue 

    def set_valueList(self, nkey, nvalue):
        if self.key not in dataMusic:
            return
        for value in nvalue:
            dataMusic[self.key][nkey].append(value) 

    def del_value(self, nkey):
        if self.key in dataMusic:
            del dataMusic[self.key][nkey]

    def get_user(self):
        return dataMusic.get(self.key)

    def get_value(self, nkey):
        if self.key in dataMusic:
            return dataMusic[self.key].get(nkey)

    def del_user(self):
        if self.key in dataMusic:
            del dataMusic[self.key]


    def file_being_uploaded(self):
        if dataMusic.get(self.key) and dataMusic.get(self.key).get("null"):
            return True

    def delfile(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

    def minutes_passed(self, stime):
        try:
            return datetime.now() - stime >= timedelta(minutes=15)
        except:
            ...



    def word2links(self, msg, word:str, max_results=5):
        """    
        ### thumbnails
        ### id
        ### title
        ### duration
        ### channel
        ### views
        ### publish_time
        """
        data = YoutubeSearch(word, max_results=max_results).to_dict()
        return data

    def extract_ids(self, text):
        match = re.search(r'(\d+)_(\d+)', text)
        if match:
            user_id, chat_id = match.groups()
            return int(user_id), int(chat_id)
        return None, None
    

    def get_yt_link_by_id(self, type_yt, vid):
        url = f"https://youtu.be/{vid}"
        is_audio = type_yt != "video"
        print(f"{is_audio=}")
        print(f"{type_yt=}")

        options = {
            'quiet': True,
            'noplaylist': True,
            'skip_download': True,

        }


        format_selector = 'bestaudio/best' if is_audio else 'best'

        options['format'] = format_selector

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                return info['url'] 
        except Exception as e:
            return f"❌ خطأ: {str(e)}"


    @property
    def step_text(self):
        return '🎤🎤'


    def generate_markup(self, data, close_name, msg, username, bot):
        keyboard = []
        
        for d in data:
            button = InlineKeyboardButton(
                text=d['title'],
                callback_data=f'YT {d["id"]} {msg.chat.id} {msg.from_user.id}'
            )
            keyboard.append([button])  

        close_button = InlineKeyboardButton(text=". اغلاق .", callback_data=close_name)
        keyboard.append([close_button])
        if username:
            ch = bot.get_chat(username)
            username = username.replace("@", "")
            cch_button = InlineKeyboardButton(text=ch.title, url=f"https://t.me/{username}")
            keyboard.append([cch_button])

        return InlineKeyboardMarkup(keyboard)
    


    def is_admin(self, bot_token):
        checked = ['creator', 'administrator']
        url = f'https://api.telegram.org/bot{bot_token}/getChatMember?chat_id={self.chat_id}&user_id={self.user_id}'
        status = requests.get(url)
        data = status.json()
        status_user = data.get("result").get("status")
        if status_user in checked:
            return True


    def is_in_chat(self, bot_token, us):
        checked = ['creator', 'administrator', 'member']
        url = f'https://api.telegram.org/bot{bot_token}/getChatMember?chat_id={self.chat_id}&user_id={us}'
        status = requests.get(url)
        data = status.json()
        status_user = data.get("result").get("status")
        if status_user in checked:
            return True


    def select_type_mrkup_yt(self, call, username, bot):
        msg = call.message
        keyboard =[
                [
                    InlineKeyboardButton(text='. فيديو .', callback_data=f'vidyt {msg.chat.id} {call.from_user.id}'),
                    InlineKeyboardButton(text='. اوديو .', callback_data=f'audyt {msg.chat.id} {call.from_user.id}'),
                ],
                [
                    InlineKeyboardButton(text='. اغلاق .', callback_data=f'yt_close {msg.chat.id} {call.from_user.id}'),
                ],
            ]
        
        if username:
            ch = bot.get_chat(username)
            username = username.replace("@", "")
            cch_button = InlineKeyboardButton(text=ch.title, url=f"https://t.me/{username}")
            keyboard.append([cch_button])
        return InlineKeyboardMarkup(keyboard)
    


    def showTools(self, client:pyrogram.Client):
        btns = [
                [
                    InlineKeyboardButton(text='. ⏹️ .', callback_data=f'⏹️'),
                ],
                [
                    InlineKeyboardButton(text='. ⏸️ .', callback_data=f'⏸️'),
                    InlineKeyboardButton(text='. 🔁 .', callback_data=f'🔁'),
                    InlineKeyboardButton(text='. ⏮️ .', callback_data=f'⏮️'),
                    InlineKeyboardButton(text='. ▶ .', callback_data=f'▶'),
                ],
                [
                    InlineKeyboardButton(text='. 🔇 .', callback_data=f'🔇'),
                    InlineKeyboardButton(text='. 🔉 .', callback_data=f'🔉'),
                ]
            ]
        
        return btns

    def detxt(self, title, ti):
        v = f"""<b>⊱ {TitleMsg_msg}: {title}
⊱ {DurationMsg_msg}: <code>{ti}</code> </b>"""
        return v
    

    def btnsubC(self, ch, client, btns):
        if not ch: return btns
        name = client.get_chat(ch).title
        btns.append([
                InlineKeyboardButton(text=f'. {name} .', url=f'https://t.me/{ch}'),
            ],)
        return btns










def Connection():
    conn = sqlite3.connect(pathdb)
    conn.row_factory = sqlite3.Row
    return conn

def disConnection(conn:sqlite3.Connection):
    conn.commit()
    conn.close()



def createtable():
    conn = Connection()
    cursor = conn.cursor()
    query = """CREATE TABLE if not exists "grmus" (
	"id" INTEGER,
    chat_id INTEGER,
    user_id INTEGER,
	"path"	TEXT default null,
    "vid" TEXT default null,
    "thumbnails" TEXT default null,
    "title" TEXT default null,
    "duration" TEXT default null,
    "fname" TEXT default null,
    "type" TEXT default null,
    "msg_id" INTEGER default null,

    PRIMARY KEY (id)
    );"""
    cursor.execute(query)
    disConnection(conn)

createtable()

def addmusic(chat_id, vid= None, thumbnails=None, title=None, duration=None, path=None, user_id=None, fname = None, type = None, msg_id = None):
    conn = Connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT or REPLACE INTO grmus (chat_id, vid, thumbnails, title, duration, path, user_id, fname, type, msg_id)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (chat_id, vid, thumbnails, title, duration, path, user_id, fname, type, msg_id))
    disConnection(conn)


def get_music(chat_id):
    conn = Connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM grmus WHERE chat_id = ? ORDER BY id ASC LIMIT 1', (chat_id,))
    music = cursor.fetchone()
    disConnection(conn)
    if music:
        music_dict = dict(music)
        return {
            "path": music_dict['path'],
            "vid": music_dict['vid'],
            "thumbnails": music_dict['thumbnails'],
            "title": music_dict['title'],
            "duration": music_dict['duration'],
            "user_id": music_dict['user_id'],
            "fname": music_dict['fname'],
            "type": music_dict['type'],
            "msg_id": music_dict['msg_id'],
        }

def get_musics(chat_id):
    conn = Connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM grmus WHERE chat_id = ?', (chat_id,))
    musics = cursor.fetchall()
    disConnection(conn)
    music_list = []
    if not musics:return music_list
    for music in musics:
        music_dict = dict(music)
        music_list.append({
            "path": music_dict['path'],
            "vid": music_dict['vid'],
            "thumbnails": music_dict['thumbnails'],
            "title": music_dict['title'],
            "duration": music_dict['duration'],
            "user_id": music_dict['user_id'],
            "fname": music_dict['fname'],
            "type": music_dict['type'],
            "msg_id": music_dict['msg_id'],
        })
    
    return music_list



def addPathMusic(chat_id, path):
    conn = Connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE grmus SET path = ? WHERE chat_id = ?''', (path, chat_id,))
    disConnection(conn)


def remove_last_music(chat_id):
    conn = Connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM grmus WHERE chat_id = ? ORDER BY id ASC LIMIT 1', (chat_id,))
    row = cursor.fetchone()
    
    if row:
        cursor.execute('DELETE FROM grmus WHERE id = ?', (row[0],))
    
    disConnection(conn)


def remove_music(chat_id):
    conn = Connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM grmus WHERE chat_id = ?', (chat_id,))
    disConnection(conn)


def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds




User_Dict = {}
class User:
    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id
        self.key = f"{chat_id}:{user_id}"
    def insert(self):
        if self.key not in User_Dict:
            User_Dict[self.key] = {
                "user_id": self.user_id,
                "chat_id": self.chat_id,
                "status": "member"
            }
    def get_status(self):
        if self.key in User_Dict:
            return User_Dict[self.key]['status']
    def update(self, status):
        if not User_Dict.get(self.key): return
        User_Dict[self.key]["status"] = status
    def get(self):
        return User_Dict.get(self.key)
    def delete(self):
        if not User_Dict.get(self.key):return
        del User_Dict[self.key]
    def get_num_members(self):
        return len(User_Dict)
    def get_members(self):
        if not len(User_Dict):return
        return User_Dict.values()
    


