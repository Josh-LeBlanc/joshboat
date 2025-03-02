import discord
from discord.ext import commands
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
    prefix = "."
    intents.message_content = True
    client = commands.Bot(command_prefix=prefix, intents=intents)

    queues = {}
    voice_clients = {}

    @client.event
    async def on_ready():
        print(f"{client.user} is ready")

    @client.command(name="play")
    async def play(ctx: commands.Context, link):
        try:
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client

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

            info = ytdlp.extract_info(link, download=True)
            filename = ytdlp.prepare_filename(info) + ".opus"
            ffmpeg_options = {"options": "-vn"}
            
            voice_client.play(discord.FFmpegOpusAudio(filename, **ffmpeg_options))

        except Exception as e:
            print(e)

    @client.command(name="pause")
    async def pause(ctx: commands.Context):
        try:
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client
            voice_client.pause()
        except Exception as e:
            print(e)

    @client.command(name="resume")
    async def resume(ctx: commands.Context):
        try:
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client

            voice_client.resume()
        except Exception as e:
            print(e)

    @client.command(name="stop")
    async def stop(ctx: commands.Context):
        try:
            if ctx.guild.id in voice_clients.keys():
                voice_client = voice_clients[ctx.guild.id]
            else:
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client

            voice_client.stop()
            await voice_client.disconnect()
            voice_clients.pop(ctx.guild.id)
        except Exception as e:
            print(e)


    client.run(bot_token)


    


