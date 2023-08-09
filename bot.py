from os import getenv, path, rename, remove
from dotenv import load_dotenv
from pytube.__main__ import pytube
from telegram import Update, Video
from telegram.ext import (ApplicationBuilder,
                         ContextTypes, 
                         CommandHandler,
                         MessageHandler, filters)
from pytube import YouTube, exceptions

load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if effective_chat:
        await context.bot.send_message(chat_id=effective_chat.id, text="I'm a bot, please talk to me!")


async def on_attach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    message = update.message
    if effective_chat and message and message.text:
        try:
            yt_video = YouTube(message.text)
            video_streams = yt_video.streams.get_audio_only()
            if video_streams:
                videos_dir = "videos"
                out_file = video_streams.download(output_path=videos_dir)
                base, _ = path.splitext(out_file) # split the file on base and extention
                new_file = base + ".mp3"
                rename(out_file, new_file)
                await context.bot.send_audio(chat_id=effective_chat.id, audio=new_file)
                remove(new_file)
        except exceptions.RegexMatchError:
            await context.bot.send_message(chat_id=effective_chat.id, text="Ссылка не ведёт на youtube")


def main():
    TOKEN = getenv("TOKEN")
    if TOKEN is None:
        print("No token")
        exit(1)
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(MessageHandler(filters.ALL, on_attach))
    
    application.run_polling()


if __name__ == '__main__':
    main()

