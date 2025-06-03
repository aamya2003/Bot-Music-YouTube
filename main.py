from helpers import *





myus = "" # @يوزر نيم  => username
# اذا ماعندك قناة خليه فارغ




API_ID = 21678228
API_HASH = "fa295f4a9f5ca7fa4a361f075b8642cb"
bot_token = "7747517869:AAF3cJsk8AnYcqeEbj4cIf3uqQgC-4Ha5q8"

Your_Id = 123456789


userBot = Client(
    name="babybot",
    api_id=API_ID,
    api_hash=API_HASH,  
    )

bot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,  
    bot_token=bot_token,
    parse_mode=enums.ParseMode.HTML
    )

app = PyTgCalls(
    userBot
    )



userBot.start()
bot.start()
app.start()






@bot.on_message(filters.text)
def handle_text(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    ddtyt = yUtube_data(user_id, chat_id)
    USER = User(user_id, chat_id)
    fname = message.from_user.first_name
    usermention = f"""<a href="tg://user?id={user_id}">{fname}</a>"""
    text = message.text
    

    for key in syrian_responses.keys():
        if key == text:
            message.reply(syrian_responses[key])
            return

    if text in ['الصوتية', "الصوتيه"]:
        chat_id = message.chat.id
        user = message.from_user

        ddyt = yUtube_data(user.id, chat_id)

        client.send_animation(chat_id, "mediaBot/bg.mp4", Sout_msg.format(username =usermention)
                        ,reply_markup= InlineKeyboardMarkup(ddyt.btnsubC(myus, client, [])) if myus else None
            )


    elif text.startswith(("/start ", '/start')) or text == "/start":
        message.reply("أهلاً وسهلاً في بوت الميوزك والحماية!\n\nاكتب اسم أغنية بعد كلمة تحميل أو تنزيل، مثال: تحميل يا زين ياللي تعدينا.\n\nوأوامر الحماية: كتم، طرد، حظر.\n\nأي كلمة مثل 'اسكت' أو 'اخرس'، البوت بيرد عليك بردود سورية طريفة.")
        
    
    elif text.startswith(('رن ')):
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝘀𝗲𝗮𝗿𝗰𝗵", usermention= usermention),
            )
            return

    

        try:
            print(chat_id)
            print(Your_Id)
            c = ddtyt.is_in_chat(bot_token, Your_Id)
            print(c)
            if not c:
                raise Exception("error")
        except Exception as e:
            print(f"a {e = }")
            mm = client.send_message(
                chat_id=chat_id,
                text=Help_User_Invite_msg,
            )
            try:
                if not ("The user is already a participant of this chat" in str(e)):
                    invite_link = client.export_chat_invite_link(chat_id)
                    userBot.join_chat(invite_link)
                    
            except Exception as e:
                print(f"c {e = }")
                client.edit_message_text(
                    chat_id=chat_id,
                    text=No_Help_User_Invite_msg,
                    message_id=mm.id
                )
                return
            
        mems = app.get_participants(chat_id)
        print(mems)
        if not mems:
            client.send_message(chat_id, text=No_One_In_Call_msg)
            return
        
        if ddtyt.file_being_uploaded():
            client.send_message(
                        chat_id=chat_id,
                        text=Alert_Wait_For_Prev_msg.format(usermention=usermention),
                    )
            return 

        search_query = text.replace("call ", "", 1).strip()
        ddtyt = yUtube_data(user_id, chat_id)
        data = ddtyt.word2links(message, search_query)


        markup = ddtyt.generate_markup(data, f'yt_close {chat_id} {user_id}', message, myus, bot)

        emojis = ["😔", "💔", "✨", "⭐️"]        
        m = client.send_message(
            chat_id=chat_id,
            text=f"{Chose_Vid_msg} {random.choice(emojis)}:",
            reply_markup=markup
        )
        ddtyt.set_value("step", "search")
        ddtyt.set_value("data", data)
        ddtyt.set_value("user_id", user_id)
        ddtyt.set_value("chat_id", chat_id)
        ddtyt.set_value("search-time", datetime.now())
        ddtyt.set_value("msgs", [m.id])
        # ddtyt.set_value("msgs", [m.id, message.id])


    elif text.startswith(("/leave ", '/leave')) or text == "/leave":
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗰𝗹𝗼𝘀𝗲 𝗰𝗮𝗹𝗹", usermention= usermention),

            )
            return
        client.delete_messages(chat_id, message.id)
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝙚𝙣𝙙"),
            )
        try:
            app.leave_call(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝙚𝙣𝙙𝙚𝙙", emogi="😥"))
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))

        currentMusic = get_musics(chat_id)
        for m in currentMusic:
            if os.path.exists(m['path']):
                os.remove(m['path'])
        remove_music(chat_id)

    elif text.startswith(("/mute ", "/mute")) or text == "/mute":
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗺𝘂𝘁𝗲", usermention= usermention),
            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗺𝘂𝘁𝗲"),
            )
        try:
            app.mute(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝗺𝘂𝘁𝗲𝙙", emogi="🤐"))
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif text.startswith(("/repeat ", '/repeat')) or text == "/repeat":
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗿𝗲𝗽𝗲𝗮𝘁𝗲", usermention= usermention),
            )
            return
        client.delete_messages(chat_id, message.id)
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗿𝗲𝗽𝗲𝗮𝘁𝗲"),
            )
            return 'there is not any music to repeat'

        try:
            mm = client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝗿𝗲𝗽𝗲𝗮𝘁𝗲𝙙", emogi="😍"))

            app.play(
                chat_id,
                currentMusic['path']
            )
            btns = ddtyt.showTools(bot)
            btns = ddtyt.btnsubC(myus, client, btns)
            mrkup = InlineKeyboardMarkup(btns)

            usermention = f"""<a href="tg://user?id={currentMusic['user_id']}">{currentMusic['fname']}</a>"""
            caption = ddtyt.detxt(currentMusic['title'], currentMusic['duration']) + Song_Is_Requested_msg.format(usermention=usermention)

            m = client.send_photo(
            chat_id=chat_id,
            photo=currentMusic['thumbnails'],
            caption=caption,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=mrkup)
            client.delete_messages(chat_id, mm.id)
            

        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif text.startswith(("/skip ", '/skip')) or text == "/skip":
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝘀𝗸𝗶𝗽", usermention= usermention),
            )
            return

        removed_currentMusic = get_music(chat_id)
        print(f"{removed_currentMusic=}")
        client.delete_messages(chat_id, message.id)
        if not removed_currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝘀𝗸𝗶𝗽"),
            )
            return 'there is not any music to close'

        path_currentMusic_will_remove = removed_currentMusic['path']
        remove_last_music(chat_id)
        currentMusic = get_music(chat_id)
        print(f"{currentMusic=}")
        if not currentMusic:
            app.leave_call(chat_id)
            client.send_message(
                chat_id=chat_id,
                text=No_Next_Song_2_msg.format(usermention=usermention, action = "𝘀𝗸𝗶𝗽"),
            )
            return 'no new music to run'

        try:
            mm = client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝘀𝗸𝗶𝗽𝗲𝙙", emogi="😉"))
            app.leave_call(chat_id)
            app.play(
                chat_id,
                currentMusic['path']
            )



            btns = ddtyt.showTools(bot)
            btns = ddtyt.btnsubC(myus, client, btns)
            mrkup = InlineKeyboardMarkup(btns)

            usermention = f"""<a href="tg://user?id={currentMusic['user_id']}">{currentMusic['fname']}</a>"""
            caption = ddtyt.detxt(currentMusic['title'], currentMusic['duration']) + Song_Is_Requested_msg.format(usermention=usermention)

            m = client.send_photo(
            chat_id=chat_id,
            photo=currentMusic['thumbnails'],
            caption=caption,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=mrkup)
            client.delete_messages(chat_id, mm.id)
            

            if os.path.exists(path_currentMusic_will_remove):
                os.remove(path_currentMusic_will_remove)
        except Exception as e:
            print(f"{e=}")
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif text.startswith(("/pause ", '/pause')) or text == "/pause":
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗽𝗮𝘂𝘀𝗲", usermention= usermention),

            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗽𝗮𝘂𝘀𝗲𝗱"),
            )
        try:
            app.pause(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝗽𝗮𝘂𝘀𝗲𝗱", emogi="😶"))
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif text.startswith(("/resume ", '/resume')) or text == "/resume":
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗿𝗲𝘀𝘂𝗺𝗲", usermention= usermention),

            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗿𝗲𝘀𝘂𝗺𝗲𝗱")
            )
        try:
            app.resume(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝗿𝗲𝘀𝘂𝗺𝗲𝗱", emogi="😊"))

        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif text.startswith(("/unmute ", "/unmute")) or text == "/unmute":
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 
        
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝘂𝗻𝗺𝘂𝘁𝗲", usermention= usermention),

            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝘂𝗻𝗺𝘂𝘁𝗲")
            )
        try:
            app.unmute(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝘂𝗻𝗺𝘂𝘁𝗲𝗱", emogi="😻"))

        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))



    elif text.startswith(('/v ', "/volume ")) and len(text.split(" ")) == 2:
        sp = text.split(" ")
        level = None
        if sp[1].isnumeric():
            level = int(sp[1])
        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
            text=Alert_Admin_msg.format(action="𝗰𝗵𝗮𝗻𝗴𝗲 𝘁𝗵𝗲 𝘀𝗼𝗻𝗴 𝘃𝗼𝗹𝘂𝗺𝗲", usermention= usermention),

            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗰𝗵𝗮𝗻𝗴𝗲 𝘁𝗵𝗲 𝘀𝗼𝗻𝗴 𝘃𝗼𝗹𝘂𝗺𝗲")
            )
        try:
            app.change_volume_call(chat_id, level)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action=f"𝗰𝗵𝗮𝗻𝗴𝗲d 𝘁𝗵𝗲 𝘀𝗼𝗻𝗴 𝘃𝗼𝗹𝘂𝗺𝗲 𝗧𝗼 {level}", emogi="🙀"))
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))





@bot.on_callback_query()
def handle_callback(client: Client, call: CallbackQuery):

    data = call.data
    msg = call.message

    chat_id = msg.chat.id
    user_id = call.from_user.id

    msg_id = msg.id
    fname = call.from_user.first_name
    usermention = f"""<a href="tg://user?id={user_id}">{fname}</a>"""

    ddtyt = yUtube_data(user_id, chat_id)



    if "YT" in data:
        extracted_data  = data.split(" ")
        ID = extracted_data[1]
        chatID = int(extracted_data[2])
        userID = int(extracted_data[3])

        if userID == user_id and chatID == chat_id: 
            if not (ddtyt.get_value("step") == "search"):
                client.answer_callback_query(call.id, You_Are_Not_Auth_msg, show_alert=True)
                return

            ddtyt.set_value("step", "choose-link")

            ddtyt.set_value("choose-link-time", datetime.now())

            ddtyt.del_value("search-time")

            my_data = ddtyt.get_value('data')

            for i_d in my_data:
                if i_d['id'] == ID:
                    ddtyt.set_value("data", i_d)
                    # dataMusic[key]['data'] = i_d
                    mrkup = ddtyt.select_type_mrkup_yt(call, myus, client)

                    caption = ddtyt.detxt(i_d['title'], i_d['duration'])

                    client.delete_messages(chat_id, msg_id)

                    m = client.send_photo(
                        chat_id=chat_id,
                        photo=i_d['thumbnails'][-1],
                        caption=caption,
                        reply_markup=mrkup,
                        parse_mode=enums.ParseMode.HTML
                    )
                    ddtyt.set_valueList("msgs", [m.id, msg.id])


                    return
                
    elif "vidyt" in data or  "audyt" in data:
        extracted_data = data.split(' ')
        chatID = int(extracted_data[1])
        userID = int(extracted_data[2])
        if userID == user_id and chatID == chat_id:
            dtype = 'audio' if 'audyt' in data else 'video'
            print(f"{dtype=}")

            print(ddtyt.get_value("step"))
            key = f"{chat_id}:{user_id}"
            us = dataMusic.get(key)
            if not (ddtyt.get_value("step") == "choose-link"):
                client.answer_callback_query(call.id, You_Are_Not_Auth_msg, show_alert=True)
                return
            client.delete_messages(chat_id, msg.id)
            m = client.send_message(chat_id, downloadS1 + ddtyt.step_text * 2)
            us = ddtyt.get_user()
            i_d = us.get("data")
            ID = i_d['id']

            client.edit_message_text(chat_id, m.id, downloadS2 + ddtyt.step_text * 3)
            caption = ddtyt.detxt(i_d['title'], i_d['duration']) + Song_Is_Requested_msg.format(usermention= usermention)
            ifMusicExists = get_music(chat_id)

            ddtyt.set_value("null", True)    
            
            media = ddtyt.get_yt_link_by_id(dtype, ID)
            
            client.edit_message_text(chat_id, m.id, downloadS2 + ddtyt.step_text * 4)

            # s
            if ifMusicExists:
                print("Yes")
                client.delete_messages(chat_id, m.id)
                btns = ddtyt.showTools(bot)
                btns = ddtyt.btnsubC(myus, client, btns)
                mrkup = InlineKeyboardMarkup(btns)
                m = client.send_photo(
                chat_id=chat_id,
                photo=i_d['thumbnails'][-1],
                caption=Song_Added_2_List + caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=mrkup)
                addmusic(chat_id, i_d['id'], i_d['thumbnails'][-1], i_d['title'], i_d['duration'],media, user_id, fname,  dtype, m.id)
                client.delete_messages(chat_id, ddtyt.get_value("msgs"))
                ddtyt.del_user()
                return
            # s


            try:
                client.edit_message_text(chat_id, m.id, downloadS3)
                app.play(
                    chat_id,
                    media
                )


                client.delete_messages(chat_id, m.id)

                client.delete_messages(chat_id, ddtyt.get_value("msgs"))


                ddtyt.del_user()

                # start create mrkup
                btns = ddtyt.showTools(bot)
                btns = ddtyt.btnsubC(myus, client, btns)
                mrkup = InlineKeyboardMarkup(btns)
                # end create mrkup

                # start delete message option
                try:
                    client.delete_messages(chat_id, call.message.id)
                except:
                    ...
                # end delete message option
                

                m = client.send_photo(
                    chat_id=chat_id,
                    photo=i_d['thumbnails'][-1],
                    caption=caption,
                    reply_markup=mrkup,
                    parse_mode=enums.ParseMode.HTML
                    )
                addmusic(chat_id, i_d['id'], i_d['thumbnails'][-1], i_d['title'], i_d['duration'],media, user_id, fname,  dtype, m.id)


            except Exception as e:
                print(f"Error =>: {e}")
            return


    elif "yt_close" in data :
        key = f"{chat_id}:{user_id}"
        splted_data = data.split(" ") 
        ch = int(splted_data[1])
        us = int(splted_data[2])
        if not(ch == chat_id and us == user_id):  
            client.answer_callback_query(call.id, You_Are_Not_Auth_msg, show_alert=True)
            return
        if not dataMusic.get(key):
            return
        for ms in dataMusic[key]['msgs']:
            try:
                client.delete_messages(chat_id, ms)
            except:
                ...    
        del dataMusic[key]



    elif '⏹️' in data:
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 

        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝙚𝙣𝙙", usermention= usermention),
            )
            return
        try:
            client.delete_messages(chat_id, msg.id)
            app.leave_call(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝙚𝙣𝙙𝙚𝙙", emogi="😥"))
        except Exception as e:
            print(f"{e=}")
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))

        currentMusic = get_musics(chat_id)
        for m in currentMusic:
            if os.path.exists(m['path']):
                os.remove(m['path'])
        remove_music(chat_id)


    elif '⏮️' in data:
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 

        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝘀𝗸𝗶𝗽", usermention= usermention),
            )
            return
        client.delete_messages(chat_id, msg.id)
        removed_currentMusic = get_music(chat_id)
        if not removed_currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝘀𝗸𝗶𝗽")
            )
            return 'there is not any music to close'

        path_currentMusic_will_remove = removed_currentMusic['path']
        remove_last_music(chat_id)
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Next_Song_2_msg.format(usermention=usermention, action = "𝘀𝗸𝗶𝗽"),
            )
            return 'no new music to run'

        try:
            app.play(
                chat_id,
                currentMusic['path']
            )

            mm = client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝘀𝗸𝗶𝗽𝗲𝙙", emogi="😍"))



            btns = ddtyt.showTools(bot)
            btns = ddtyt.btnsubC(myus, client, btns)
            mrkup = InlineKeyboardMarkup(btns)
            usermention = f"""<a href="tg://user?id={currentMusic['user_id']}">{currentMusic['fname']}</a>"""
            caption = ddtyt.detxt(currentMusic['title'], currentMusic['duration']) +Song_Is_Requested_msg.format(usermention=usermention)

            m = client.send_photo(
                chat_id=chat_id,
                photo=currentMusic['thumbnails'],
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=mrkup
                )
            client.delete_messages(chat_id, mm.id)
            

            if os.path.exists(path_currentMusic_will_remove):
                os.remove(path_currentMusic_will_remove)
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif '🔁' in data:
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 

        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗿𝗲𝗽𝗲𝗮𝘁𝗲", usermention= usermention),
            )
            return
        client.delete_messages(chat_id, msg.id)
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗿𝗲𝗽𝗲𝗮𝘁𝗲")
            )
            return 'there is not any music to repeat'
        try:
            app.play(
                chat_id,
                currentMusic['path']
            )
            mm = client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝗿𝗲𝗽𝗲𝗮𝘁𝗲𝙙", emogi="😍"))


            btns = ddtyt.showTools(bot)
            btns = ddtyt.btnsubC(myus, client, btns)
            mrkup = InlineKeyboardMarkup(btns)
            usermention = f"""<a href="tg://user?id={currentMusic['user_id']}">{currentMusic['fname']}</a>"""
            caption = ddtyt.detxt(currentMusic['title'], currentMusic['duration']) + Song_Is_Requested_msg.format(usermention=usermention)

            m = client.send_photo(
                chat_id=chat_id,
                photo=currentMusic['thumbnails'],
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=mrkup
                )
            client.delete_messages(chat_id, mm.id)
        
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif '⏸️' in data:
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 

        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗽𝗮𝘂𝘀𝗲", usermention= usermention),
            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗽𝗮𝘂𝘀𝗲𝗱")
            )
            return 'there is not any music to 𝗽𝗮𝘂𝘀𝗲𝗱'

        try:
            app.pause(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝗽𝗮𝘂𝘀𝗲𝗱", emogi="😶"))
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))



    elif '▶' in data:
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 

        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗿𝗲𝘀𝘂𝗺𝗲", usermention= usermention)
            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗿𝗲𝘀𝘂𝗺𝗲")
                )
            return 'there is not any music to 𝗿𝗲𝘀𝘂𝗺𝗲𝗱'

        try:
            app.resume(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝗿𝗲𝘀𝘂𝗺𝗲𝗱", emogi="😊"))
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif '🔇' in data:
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 

        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝗺𝘂𝘁𝗲", usermention= usermention)
            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝗺𝘂𝘁𝗲")
                )
            return 'there is not any music to 𝗺𝘂𝘁𝗲𝗱'

        try:
            app.mute(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝗺𝘂𝘁𝗲𝙙", emogi="🤐"))
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))


    elif '🔉' in data:
        admin = client.get_chat_member(chat_id, user_id)
        ISADMIN = str(admin.status) in ['ChatMemberStatus.ADMINISTRATOR', "ChatMemberStatus.OWNER"] 

        if not ISADMIN:
            client.send_message(
                chat_id=chat_id,
                text=Alert_Admin_msg.format(action="𝘂𝗻𝗺𝘂𝘁𝗲", usermention= usermention)
            )
            return
        currentMusic = get_music(chat_id)
        if not currentMusic:
            client.send_message(
                chat_id=chat_id,
                text=No_Cureent_Song_msg.format(usermention=usermention, action="𝘂𝗻𝗺𝘂𝘁𝗲")
            )
            return 'there is not any music to 𝘂𝗻𝗺𝘂𝘁𝗲𝗱'

        try:
            app.unmute(chat_id)
            client.send_message(chat_id=chat_id, text=Song_Was_msg.format(usermention=usermention, action="𝘂𝗻𝗺𝘂𝘁𝗲𝗱", emogi="😻"))
        except:
            client.send_message(chat_id=chat_id, text=UserBot_Not_In_Call_msg.format(usermention=usermention))




@bot.on_message( filters=filters.new_chat_members)
def handle_text(client: Client, message: Message):
    chat_id = message.chat.id
    user = message.from_user
    ddyt = yUtube_data(user.id, chat_id)
    me = client.get_me()
    usermention = f"""<a href="tg://user?id={me.id}">{me.first_name}</a>"""
    if message.new_chat_members[0].id == me.id:
        client.send_photo(chat_id, "mediaBot/background.jpg", Bot_Join_msg.format(
            username =user.first_name,
            name =  usermention,
            grname = message.chat.title),reply_markup= InlineKeyboardMarkup(ddyt.btnsubC(myus, client, []) if myus else None)
            )

@bot.on_message( filters=filters.video_chat_started)
def handle_text(client: Client, message: Message):
    chat_id = message.chat.id
    client.send_message(chat_id, Call_Open_msg, reply_to_message_id=message.id)




@bot.on_message(filters.video_chat_ended)
def handle_text(client: Client, message: Message):
    chat_id = message.chat.id
    duration = message.video_chat_ended.duration 
    
    readable_time = str(timedelta(seconds=duration))

    client.send_message(
        chat_id, 
        Call_Close_msg.format(time=readable_time),
        reply_to_message_id=message.id
    )


from pytgcalls.types import StreamEnded
@app.on_update()
async def  stream_end_handler(_: PyTgCalls, update: StreamEnded):
    chat_id = update.chat_id
    if "Status.CLOSED_VOICE_CHAT" in str(update):
        currentMusic = get_musics(chat_id)
        for m in currentMusic:
            if os.path.exists(m['path']):
                os.remove(m['path'])
        remove_music(chat_id)

    
    elif "StreamEnded" in str(update):
        print("SE onUpdate")
        
        removed_currentMusic = get_music(chat_id)
        if not removed_currentMusic:
            await _.leave_call(chat_id)
            return 'there is not any music to play'

        path_currentMusic_will_remove = removed_currentMusic['path']

        remove_last_music(chat_id)

        currentMusic = get_music(chat_id)

        if not currentMusic:
            await bot.send_message(chat_id=chat_id, text=UserBot_Left_msg)
            return 'no new music to run'

        try:
            await bot.send_message(chat_id=chat_id, text=Song_Was_ended)

            await app.play(
                chat_id,
                currentMusic['path']
            )
            ddtyt = yUtube_data('me', chat_id)
            btns = ddtyt.showTools(bot)
            if myus:
                name = await bot.get_chat(myus)
                name = name.title
                btns.append([
                        InlineKeyboardButton(text=f'. {name} .', callback_data=f'https://t.me/{myus}'),
                    ],)


            mrkup = InlineKeyboardMarkup(btns)
            usermention = f"""<a href="tg://user?id={currentMusic['user_id']}">{currentMusic['fname']}</a>"""
            caption = ddtyt.detxt(currentMusic['title'], currentMusic['duration']) + Song_Is_Requested_msg.format(usermention=usermention)
            bot.delete_messages(chat_id, currentMusic['msg_id'])
            m = await bot.send_photo(
                chat_id=chat_id,
                photo=currentMusic['thumbnails'],
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=mrkup
                )
            
            if os.path.exists(path_currentMusic_will_remove):
                os.remove(path_currentMusic_will_remove)

        except Exception as e:
            print(f"Exception ===: {e=}")
            ...






idle()