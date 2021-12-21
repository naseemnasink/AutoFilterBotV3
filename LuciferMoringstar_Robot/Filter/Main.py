# (c) PR0FESS0R-99
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL, NOR_IMG, MAIN_GROUP, RESULT_MSG, NO_TXT
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from LuciferMoringstar_Robot import RATING, GENRES, HELP, ABOUT
import random
import asyncio
import time
BUTTONS = {}
BOT = {}

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍿 ᴊᴏɪɴ ᴏᴜʀ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ 🍿", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        mo_tech_yt = f"**🗂️ Title:** {search}\n**⭐ Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**📤 Uploaded by {message.chat.title}**"
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"🧧 {get_size(file.file_size)} ◼ {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"pr0fess0r_99#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAADBQADMwIAAtbcmFelnLaGAZhgBwI')
            return

        if not btn:
            return

        if len(btn) > 5: 
            btns = list(split_list(btn, 5)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="◉ ᴘᴀɢᴇ ɴᴜᴍʙᴇʀꜱ 1/1 ◉",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                 await message.reply_photo(photo=poster, caption=f"<b>⊰᯽⊱┈⟪ {search} ⟫┈⊰᯽⊱\n\n{RESULT_MSG} </b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                 await message.reply_photo(photo=NOR_IMG, caption=f"<b>❯────「 {search} 」────❮\n\n{RESULT_MSG} </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="◉ ɢᴏ ᴛᴏ ɴᴇxᴛ ᴘᴀɢᴇ ◉",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"◉ ᴘᴀɢᴇ ɴᴜᴍʙᴇʀꜱ 1/{data['total']} ◉",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
             await message.reply_photo(photo=poster, caption=f"<b>⊰᯽⊱┈⟪ {search} ⟫┈⊰᯽⊱\n\n{RESULT_MSG} </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
             await message.reply_photo(photo=NOR_IMG, caption=f"<b>❯────「 {search} 」────❮\n\n{RESULT_MSG} </b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        mo_tech_yt = f"**🗂️ Title:** {search}\n**⭐ Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**📤 Uploaded by {message.chat.title}**"
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"🧧 {get_size(file.file_size)}▫️{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=pr0fess0r_99_-_-_-_{file_id}")]
                )
        else:
            Send_message = await message.reply_text(
                     text=f"<b>Hello {message.from_user.first_name}, I could not find {search} the movie you asked for...\n\nGoogle,IMDB-Click on any button and find the CORRECT MOVIE NAME and enter it here but the movie will be available...If you do not receive the movie even after entering the correct name ...  @admin type movie name Inform the admin in this format...We will upload within 24 hours</b>",
                     reply_markup=InlineKeyboardMarkup(
                         [
                             [
                                 InlineKeyboardButton("⚡ ɪᴍᴅʙ ⚡", url="https://www.imdb.com/"),
                                 InlineKeyboardButton("🌟 ɢᴏᴏɢʟᴇ 🌟", url="https://www.google.com/")
                             ],
                             [
                                 InlineKeyboardButton("😪 ഒന്നും മനസ്സിലായില്ല 😪", callback_data="understand")
                             ]      
                         ]
                     )
                )
            await asyncio.sleep(10)
            await Send_message.delete()
            await message.delete()
            return
        if not btn:
            return

        if len(btn) > 5: 
            btns = list(split_list(btn, 5)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="◉ ɴᴏ ᴘᴀɢᴇ ◉",callback_data="pages"), InlineKeyboardButton(text="◉ ᴅᴇʟᴇᴛᴇ ◉", callback_data="deletemd")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                Send_messege = await message.reply_photo(photo=poster, caption=f"⌕ ǫᴜᴇʀʏ : {search}\n\n〓〓 ɪᴍᴅʙ ᴅᴇᴛᴀɪʟꜱ 〓〓\n\n⍞ ᴛɪᴛɪʟᴇ : {title}\n⌗ ɢᴇɴʀᴇ : {genres}\n★  ʀᴀᴛɪɴɢ : <a href={url}/ratings>{rating}</a> / 10\n⌥ ʀᴜɴᴛɪᴍᴇ : {runtime} Min\n⌬ ʟᴀɴɢᴜᴀɢᴇs : {languages}\n〄 ʀᴇʟᴇᴀꜱᴇ ᴅᴀᴛᴇ : {release_date}\n\n★ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴄɪɴᴇᴍᴀ ʟᴏᴋʜᴀᴍ", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                Send_messege = await message.reply_photo(photo=NOR_IMG, caption=f"⌕ ǫᴜᴇʀʏ : {search}\n\n〓〓 ɪᴍᴅʙ ᴅᴇᴛᴀɪʟꜱ 〓〓\n\n⍞ ᴛɪᴛɪʟᴇ : {title}\n⌗ ɢᴇɴʀᴇ : {genres}\n★  ʀᴀᴛɪɴɢ : <a href={url}/ratings>{rating}</a> / 10\n⌥ ʀᴜɴᴛɪᴍᴇ : {runtime} Min\n⌬ ʟᴀɴɢᴜᴀɢᴇs : {languages}\n〄 ʀᴇʟᴇᴀꜱᴇ ᴅᴀᴛᴇ : {release_date}\n\n★ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴄɪɴᴇᴍᴀ ʟᴏᴋʜᴀᴍ", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="◉ ɢᴏ ᴛᴏ ɴᴇxᴛ ᴘᴀɢᴇ ◉",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"◉ ᴘᴀɢᴇ ◉",callback_data="pages"),InlineKeyboardButton(text=f"1 - {data['total']}",callback_data="pages"),InlineKeyboardButton(text=f"◉ ᴅᴇʟᴇᴛᴇ ◉",callback_data="deletemd")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
             Send_messege = await message.reply_photo(photo=poster, caption=f"⌕ ǫᴜᴇʀʏ : {search}\n\n〓〓 ɪᴍᴅʙ ᴅᴇᴛᴀɪʟꜱ 〓〓\n\n⍞ ᴛɪᴛɪʟᴇ : {title}\n⌗ ɢᴇɴʀᴇ : {genres}\n★  ʀᴀᴛɪɴɢ : <a href={url}/ratings>{rating}</a> / 10\n⌥ ʀᴜɴᴛɪᴍᴇ : {runtime} Min\n⌬ ʟᴀɴɢᴜᴀɢᴇs : {languages}\n〄 ʀᴇʟᴇᴀꜱᴇ ᴅᴀᴛᴇ : {release_date}\n\n★ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴄɪɴᴇᴍᴀ ʟᴏᴋʜᴀᴍ", reply_markup=InlineKeyboardMarkup(buttons))
        else:
             Send_messege = await message.reply_photo(photo=NOR_IMG, caption=f"⌕ ǫᴜᴇʀʏ : {search}\n\n〓〓 ɪᴍᴅʙ ᴅᴇᴛᴀɪʟꜱ 〓〓\n\n⍞ ᴛɪᴛɪʟᴇ : {title}\n⌗ ɢᴇɴʀᴇ : {genres}\n★  ʀᴀᴛɪɴɢ : <a href={url}/ratings>{rating}</a> / 10\n⌥ ʀᴜɴᴛɪᴍᴇ : {runtime} Min\n⌬ ʟᴀɴɢᴜᴀɢᴇs : {languages}\n〄 ʀᴇʟᴇᴀꜱᴇ ᴅᴀᴛᴇ : {release_date}\n\n★ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴄɪɴᴇᴍᴀ ʟᴏᴋʜᴀᴍ", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "ᴋʙ", "ᴍʙ", "ɢʙ", "ᴛʙ", "ᴘʙ", "ᴇʙ"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("◉ ɢᴏ ᴛᴏ ʙᴀᴄᴋ ᴘᴀɢᴇ ◉", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"◉ ᴘᴀɢᴇ ◉", callback_data="pages"),InlineKeyboardButton(f"{int(index)+2} - {data['total']}", callback_data="pages"),InlineKeyboardButton(f"◉ ᴅᴇʟᴇᴛᴇ ◉", callback_data="deletemd")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("◉ ʙᴀᴄᴋ ᴘᴀɢᴇ ◉", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("◉ ɴᴇxᴛ ᴘᴀɢᴇ ◉", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"◉ ᴘᴀɢᴇ ◉", callback_data="pages"),InlineKeyboardButton(f"{int(index)+2} - {data['total']}", callback_data="pages"),InlineKeyboardButton(f"◉ ᴅᴇʟᴇᴛᴇ ◉", callback_data="deletemd")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("◉ ɢᴏ ᴛᴏ ɴᴇxᴛ ᴘᴀɢᴇ ◉", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"◉ ᴘᴀɢᴇ ◉", callback_data="pages"),InlineKeyboardButton(f"{int(index)} - {data['total']}", callback_data="pages"),InlineKeyboardButton(f"◉ ᴅᴇʟᴇᴛᴇ ◉", callback_data="deletemd")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("◉ ʙᴀᴄᴋ ᴘᴀɢᴇ ◉", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("◉ ɴᴇxᴛ ᴘᴀɢᴇ ◉", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"◉ ᴘᴀɢᴇ ◉", callback_data="pages"),InlineKeyboardButton(f"{int(index)} - {data['total']}", callback_data="pages"),InlineKeyboardButton(f"◉ ᴅᴇʟᴇᴛᴇ ◉", callback_data="deletemd")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "help":
            buttons = [
                [
                    InlineKeyboardButton("🍁 ʙᴏᴛ ɢʀᴏᴜᴘ 🍁", url=MAIN_GROUP)
                ]
                ]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton("🍁 ʙᴏᴛ ɢʀᴏᴜᴘ 🍁", url=MAIN_GROUP)
                ]
                ]
            await query.message.edit(text=f"{ABOUT}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
     
        elif query.data == "understand":
            buttons = [
                [
                    InlineKeyboardButton("channel", url=f"https://t.me/LatestmoviedriveCL")
                ]
                ]
            await query.answer("സിനിമ ലഭിക്കണം എങ്കിൽ താങ്കൾ ഗൂഗിൾ നോക്കി സിനിമയുടെ ᴄᴏʀʀᴇᴄᴛ ꜱᴘᴇʟʟɪɴɢ ഇവിടെ ꜱᴇɴᴅ ചെയ്യുക എങ്കിലേ താങ്കൾ ഉദ്ദശിക്കുന്ന സിനിമ എനിക്ക് അയച്ചു തരാൻ കഴിയുകയുളളു😄",show_alert=True)
     
        elif query.data == "deletemd":
            await query.message.delete()


        elif query.data.startswith("pr0fess0r_99"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton("🍁 ʙᴏᴛ ɢʀᴏᴜᴘ 🍁", url=MAIN_GROUP)
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton("🍁 ʙᴏᴛ ɢʀᴏᴜᴘ 🍁", url=MAIN_GROUP)
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer(NO_TXT.format(query.from_user.first_name), show_alert=True)
