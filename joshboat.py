import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
import collections
import requests

def run_joshboat():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    intents = discord.Intents.default()
    prefix = "?"
    intents.message_content = True
    client = commands.Bot(command_prefix=prefix, intents=intents)

    queues = {}
    voice_clients = {}

    @client.event
    async def on_ready():
        print(f"{client.user} is ready")

    async def play_next(ctx: commands.Context):
        try:
            if ctx.guild == None:
                raise Exception("please join a voice channel first")
            if ctx.guild.id in queues.keys() and len(queues[ctx.guild.id]) != 0:
                if not voice_clients[ctx.guild.id].is_playing() or ctx.guild.id not in voice_clients.keys():
                    await play_song(ctx, queues[ctx.guild.id].popleft())
                    print(f"\n\nplaying song from queue. new queue length is {len(queues[ctx.guild.id])}\n")
        except Exception as e:
            print(e)


    async def play_song(ctx: commands.Context, song: dict):
        try:
            if ctx.guild == None:
                raise Exception("please join a voice channel first")
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                if isinstance(ctx.author, discord.User):
                    raise Exception("please join a voice channel first")
                if ctx.author.voice == None:
                    raise Exception("please join a voice channel first")
                if ctx.author.voice.channel == None:
                    raise Exception("please join a voice channel first")
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client

            ffmpeg_options = {"options": "-vn"}
            voice_client.play(discord.FFmpegOpusAudio(song["filename"], **ffmpeg_options), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
            await ctx.send(f"Now playing: {song["title"]}")

        except Exception as e:
            print(e)

    @client.command(name="pause")
    async def pause(ctx: commands.Context):
        try:
            if ctx.guild == None:
                raise Exception("please join a voice channel first")
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                if isinstance(ctx.author, discord.User):
                    raise Exception("please join a voice channel first")
                if ctx.author.voice == None:
                    raise Exception("please join a voice channel first")
                if ctx.author.voice.channel == None:
                    raise Exception("please join a voice channel first")
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client
            voice_client.pause()
        except Exception as e:
            print(e)

    @client.command(name="resume")
    async def resume(ctx: commands.Context):
        try:
            if ctx.guild == None:
                raise Exception("please join a voice channel first")
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                if isinstance(ctx.author, discord.User):
                    raise Exception("please join a voice channel first")
                if ctx.author.voice == None:
                    raise Exception("please join a voice channel first")
                if ctx.author.voice.channel == None:
                    raise Exception("please join a voice channel first")
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client

            voice_client.resume()
        except Exception as e:
            print(e)

    @client.command(name="stop")
    async def stop(ctx: commands.Context):
        try:
            if ctx.guild == None:
                raise Exception("please join a voice channel first")
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                if isinstance(ctx.author, discord.User):
                    raise Exception("please join a voice channel first")
                if ctx.author.voice == None:
                    raise Exception("please join a voice channel first")
                if ctx.author.voice.channel == None:
                    raise Exception("please join a voice channel first")
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client

            for file in os.listdir("downloads"):
                os.remove("downloads/" + file)
            voice_client.stop()
            await voice_client.disconnect()
            voice_clients.pop(ctx.guild.id)
        except Exception as e:
            print(e)

    @client.command(name="play")
    async def play(ctx, *, link):
        try:
            if ctx.guild == None:
                raise Exception("please join a voice channel first")
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                if isinstance(ctx.author, discord.User):
                    raise Exception("please join a voice channel first")
                if ctx.author.voice == None:
                    raise Exception("please join a voice channel first")
                if ctx.author.voice.channel == None:
                    raise Exception("please join a voice channel first")
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client
            if ctx.guild == None:
                raise Exception("please join a voice channel first")
            if ctx.guild.id not in queues.keys():
                queues[ctx.guild.id] = collections.deque()

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

            if "https://" not in link:
                info = ytdlp.extract_info(f"ytsearch:{link}", download=True)
                if not info:
                    raise Exception("search failed")
                entry = info['entries'][0]
                title = entry['title']
                filename = "downloads/" + entry['id'] + ".opus"
            else:
                info = ytdlp.extract_info(link, download=True)
                if info == None:
                    raise Exception("ytdlp extract info failed")
                title = info['title']
                filename = "downloads/" + info['id'] + ".opus"

            song = {}
            song["filename"] = filename
            song["title"] = title

            queues[ctx.guild.id].append(song)

            await ctx.send(f"added {title} to queue")

            await play_next(ctx)
        except Exception as e:
            print(e)

    @client.command(name="skip")
    async def skip(ctx):
        try:
            if ctx.guild == None:
                raise Exception("please join a voice channel first")
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                if isinstance(ctx.author, discord.User):
                    raise Exception("please join a voice channel first")
                if ctx.author.voice == None:
                    raise Exception("please join a voice channel first")
                if ctx.author.voice.channel == None:
                    raise Exception("please join a voice channel first")
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client

            voice_client.stop()
            await play_next(ctx)
        except Exception as e:
            print(e)


    client.run(bot_token)


    


