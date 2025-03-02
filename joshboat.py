import discord
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
import collections
import time


def run_joshboat():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    prefix = "?"
    queue = collections.deque()
    voice_clients = []

    def play_queue(voice_client, ffmpeg_options):
        while len(queue) != 0:
            time.sleep(2)
            if not voice_client.is_playing():
                voice_client.play(discord.FFmpegPCMAudio(queue.pop(), **ffmpeg_options))
                time.sleep(3)

    @client.event
    async def on_ready():
        print(f"{client.user} is ready")

    @client.event
    async def on_message(message: discord.message.Message):

        if message.content.startswith(prefix + "play"):
            try:
                if len(voice_clients) == 0:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients.append(voice_client)
                else:
                    voice_client = voice_clients[0]

                url = message.content.split()[-1]

                yt_dl_options = {
                    "format": "bestaudio/best",
                    'outtmpl': 'downloads/%(id)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'opus',  # or 'mp3'
                        'preferredquality': '192',
                    }],
                }
                ytdlp = yt_dlp.YoutubeDL(yt_dl_options)

                info = ytdlp.extract_info(url, download=True)
                filename = ytdlp.prepare_filename(info) + ".opus"
                queue.append(filename)
                ffmpeg_options = {"options": "-vn"}
                
                asyncio.get_event_loop().run_in_executor(None, lambda: play_queue(voice_client, ffmpeg_options))

            except Exception as e:
                print(e)

        elif message.content.startswith(prefix + "pause"):
            try:
                if len(voice_clients) == 0:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients.append(voice_client)
                else:
                    voice_client = voice_clients[0]

                voice_client.pause()
            except Exception as e:
                print(e)

        elif message.content.startswith(prefix + "resume"):
            try:
                if len(voice_clients) == 0:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients.append(voice_client)
                else:
                    voice_client = voice_clients[0]

                voice_client.resume()
            except Exception as e:
                print(e)

        elif message.content.startswith(prefix + "stop"):
            try:
                if len(voice_clients) == 0:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients.append(voice_client)
                else:
                    voice_client = voice_clients[0]

                voice_client.stop()
                await voice_client.disconnect()
                voice_clients.remove(voice_client)
            except Exception as e:
                print(e)


    client.run(bot_token)


    


