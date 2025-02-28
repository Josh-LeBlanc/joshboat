import discord
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv


def run_joshboat():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    prefix = "hey bitch "
    vcs = {}

    @client.event
    async def on_ready():
        print(f"{client.user} is now playing music")

    @client.event
    async def on_message(message):
        if message.content.startswith(prefix + "play"):
            try:
                if vcs == {}:
                    voice_client = await message.author.voice.channel.connect()
                    vcs[voice_client.guild.id] = voice_client
                else:
                    voice_client = list(vcs.items())[0][1]

                url = message.content.split()[-1]

                yt_dl_options = {
                    "format": "bestaudio/best",
                    'outtmpl': 'downloads/%(id)s.opus',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'opus',  # or 'mp3'
                        'preferredquality': '192',
                    }],
                }
                ytdlp = yt_dlp.YoutubeDL(yt_dl_options)
                # loop = asyncio.get_event_loop()
                # data = await loop.run_in_executor(None, lambda: ytdlp.extract_info(url, download=False))
                #
                # song = data['url']

                info = ytdlp.extract_info(url, download=True)
                filename = ytdlp.prepare_filename(info)
                print(filename)
                ffmpeg_options = {"options": "-vn"}
                player = discord.FFmpegPCMAudio(filename, **ffmpeg_options)

                if vcs != {}:
                    vcs[voice_client.guild.id].play(player)
            except Exception as e:
                print(e)


    client.run(bot_token)


    


