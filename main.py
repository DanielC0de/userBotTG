from asyncio import sleep
from operator import iadd
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from config import api_hash, api_id
from time import sleep

AUTO_ANSWER_WORKS = False
HW = False
AUTO_ANSWER_TEXT = " "

dp = Client("my_account", api_id=api_id, api_hash=api_hash)


# functions which only i can use
# spam
@dp.on_message(filters.command("spam") & filters.me)
async def enable_spam(_, message):
    cmd = message.text.split(" ")[1:]
    if cmd[0] == "True":
        await message.delete()
        cmd = cmd[1:]
    text = " ".join(cmd[1:])
    for i in range(int(cmd[0])):
        await message.reply_text(text, quote=False)
        sleep(0.25)

# message for all users in group
@dp.on_message(filters.command("for_all") & filters.me)
async def for_all(_, message):
    await message.delete()
    chat = message.text.replace("/for_all ", "")
    async for member in dp.get_chat_members(message.chat.id):
        if str(member.user.username) != "None":
            chat += " @" + str(member.user.username)
        else:
            chat += " " + member.user.mention
    await message.reply_text(chat, quote=False)

# flip text
@dp.on_message(filters.command("flip") & filters.me)
async def flip(_, message):
    text = message.text.replace("/flip ", "")
    await message.edit_text(text[::-1])

# type my text using typing_symbol
@dp.on_message(filters.command("type") & filters.me) 
async def type(_, message):
    txt = message.text.split("/type ")[1]
    typing_symbol = txt[0]
    txt = txt[2:]
    check_txt = txt
    tbp = ""
    while(tbp != txt):
        try: 
            await message.edit_text(tbp + typing_symbol)
            sleep(0.05)

            tbp = tbp + check_txt[0]
            check_txt = check_txt[1:]

            await message.edit_text(tbp)
            sleep(0.05)
        except FloodWait as e:
            await sleep(e.x)

# give me home work
@dp.on_message(filters.command("дз") & filters.me)
async def auto_answer(_, message):
    global HW 
    HW = True
    await message.delete()
    await message.reply_text("Дайте, пожалуйста, дз на завтра.", quote=False)

# auto answering for all messages with my own text
@dp.on_message(filters.command("auto_answer") & filters.me)
async def auto_answer(_, message):
    global AUTO_ANSWER_TEXT, AUTO_ANSWER_WORKS
    txt = message.text.replace("/auto_answer ", "")
    AUTO_ANSWER_TEXT = txt
    AUTO_ANSWER_WORKS = True

# auto answering, but message /auto_answer deletes 
@dp.on_message(filters.command("auto_answer_del") & filters.me)
async def auto_answer(_, message):
    global AUTO_ANSWER_TEXT, AUTO_ANSWER_WORKS
    txt = message.text.replace("/auto_answer_del ", "")
    AUTO_ANSWER_TEXT = txt
    await message.delete()
    AUTO_ANSWER_WORKS = True

# off auto answering
@dp.on_message(filters.command("off_auto_answer") & filters.me)
async def off_auto_answer(_, message):
    global AUTO_ANSWER_TEXT, AUTO_ANSWER_WORKS
    check = message.text.replace("/off_auto_answer ", "")
    if check == "True":
        await message.delete()
    AUTO_ANSWER_WORKS = False 
    AUTO_ANSWER_TEXT = " "

@dp.on_message()
async def answering(_, message):
    global AUTO_ANSWER_TEXT, AUTO_ANSWER_WORKS, HW
    # answering for home work
    if HW:
        await message.reply_text("Большое спасибо!", quote=False)
        HW = False
    # auto answering in work mode 
    elif AUTO_ANSWER_WORKS:
        # if I say "рот закрой" it will stop
        if message.text.lower() == "рот закрой" or message.text.lower() == "заткнись" and message.from_user.id == 888353462:
            await message.reply_text("Понял, Сэр, извините!")
            AUTO_ANSWER_WORKS = False
        # don't auto answer me
        elif message.from_user.id == 888353462:
            pass
        # for everybody except me => auto answer
        else:
            await message.reply_text(AUTO_ANSWER_TEXT, quote=False)
    
dp.run()
