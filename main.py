import asyncio
import configparser

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, RPCError
from pyrogram.types import Message
from pyrogram.raw import functions, types

from core.data.db_connect import DBConnect

cfg = configparser.ConfigParser()
cfg.read('config.ini')
user = Client('account', api_id=cfg['USERBOT']['API_ID'], api_hash=cfg['USERBOT']['API_HASH'])
sched = AsyncIOScheduler(timezone='Europe/Moscow')
db = DBConnect()

def has_job(data):
    async def func(flt, client, msg):
        send = sched.get_job(flt.data)
        return send is not None

    return filters.create(func, data=data)

@user.on_message(filters.me & filters.command('start'))
async def start_spamer(client: Client, msg: Message):
    data = db.time_data(return_data=True)
    await msg.reply('Отправьте любое сообщение в этот чат, чтобы рассылка запустилась.')
    sched.add_job(spam_sender, 'interval', hours=data[0], kwargs={'client': client, 'msg': msg}, id='sender', replace_existing=True)
    sched.start()

@user.on_message(filters.me and filters.text and has_job('sender'))
async def spam_sender(client: Client, msg: Message):
    counts = 0
    time_data = db.time_data(return_data=True)
    spam_data = db.spam_data(return_data=True)
    interval = time_data[1]
    text = spam_data[0]
    photo = spam_data[1]
    group_chats = [dialog.chat.id async for dialog in user.get_dialogs() if dialog.chat.type == ChatType.GROUP or dialog.chat.type == ChatType.SUPERGROUP and dialog.chat.archive]
    await msg.reply(
        f"<b>БОТ</b>: <b>Рассылка запущена</b>, всего чатов: <b>{len(group_chats)}</b> шт.")
    try:
        for chat in group_chats:
            try:
                if photo and text:
                    await client.send_photo(chat, photo, text)
                if text is None:
                    await client.send_photo(chat, photo)
                if photo is None:
                    await client.send_message(chat, text)
                await asyncio.sleep(interval)
                counts += 1
            except FloodWait as fw:
                await msg.reply(f"<b>БОТ</b>: Слишком частое обращение к API Telegram!\nВремя окончания блокировки: {fw.value}")
                await asyncio.sleep(fw.value)
            except RPCError:
                pass
        await msg.reply(f'<b>БОТ</b>: <b>Рассылка завершена</b>., удалось отправить сообщения в <b>{counts}</b> чатов.')
    except Exception as e:
        await msg.reply(f"<b>БОТ</b>: Произошла ошибка: <b>{e}</b>")

@user.on_message(filters.me & filters.text & filters.command('info'))
async def get_photo(_, msg: Message):
    spam_data = db.spam_data(return_data=True)
    text = spam_data[0]
    photo_id = spam_data[1]
    time_data = db.time_data(return_data=True)
    timer = time_data[0]
    interval = time_data[1]
    await msg.delete()
    if text and photo_id:
        await msg.reply_photo(photo_id, caption=text)
    if text is None and photo_id is not None:
        await msg.reply_photo(photo_id)
    if photo_id is None and text is not None:
        await msg.reply(text)
    await msg.reply(f'🕖 Сколько будет идти рассылка: <b>{timer}ч.</b>\n〽️ Интервал отправки сообщений: <b>{interval}сек.</b>')

@user.on_message(filters.me & filters.all & filters.command('photo'))
async def get_photo(_, msg: Message):
    data = msg.command[1:]
    await msg.delete()
    if len(data) >= 1:
        db.spam_data(photo_id='del', delete=True)
        await msg.reply('Фотография была успешно удалена.')
        return
    db.spam_data(photo_id=str(msg.photo.file_id))
    await msg.reply('<b>🖼 Фотография установлена</b> и будет <b>добавлена к тексту</b>, если он <b>присутствует</b>, иначе рассылка будет без него.')

@user.on_message(filters.me & filters.all & filters.command('text'))
async def get_text(_, msg: Message):
    data = msg.command[1:]
    await msg.delete()
    if data[0] == '0':
        db.spam_data(text='del', delete=True)
        await msg.reply('Текст сообщения был успешно удален.')
        return
    db.spam_data(text=msg.text.replace('/text ', ''))
    await msg.reply('<b>✏️ Текст установлен</b> и будет <b>добавлен к фотографии</b>, если она <b>присутствует</b>, иначе рассылка начнётся без неё.')

@user.on_message(filters.me & filters.text & filters.command('timer'))
async def get_time_data(_, msg: Message):
    data = msg.command[1:]
    await msg.delete()
    if len(data) > 0:
        timer = int(data[0])
        interval = int(data[1])
        if interval == 0 and timer == 0:
            db.time_data(1, 10)
            data = db.time_data(return_data=True)
            await msg.reply(
                f'⚠️ Время таймера и интервала отправки сообщения установлено по умолчанию.\n\n🕖 Сколько будет идти рассылка: {data[0]}ч.\n〽️ Интервал отправки сообщений: {data[1]}сек.')
        elif timer == 0:
            db.time_data(1, interval)
            data = db.time_data(return_data=True)
            await msg.reply(
                f'🔘 Время таймера установлено по умолчанию.\n\n🕖 Сколько будет идти рассылка: {data[0]}ч.\n〽️ Интервал отправки сообщений: {data[1]}сек.')
        elif interval == 0:
            db.time_data(timer, 10)
            data = db.time_data(return_data=True)
            await msg.reply(
                f'🔘 Время интервала отправки сообщений установлено по умолчанию.\n\n🕖 Сколько будет идти рассылка: {data[0]}ч.\n〽️ Интервал отправки сообщений: {data[1]}сек.')
        else:
            db.time_data(timer, interval)
            data = db.time_data(return_data=True)
            await msg.reply(
                f'✅ Время таймера и интервала отправки сообщения успешно установлено.\n\n🕖 Сколько будет идти рассылка: {data[0]}ч.\n〽️ Интервал отправки сообщений: {data[1]}сек.')

if __name__ == '__main__':
    db.create_tables()
    user.run()
