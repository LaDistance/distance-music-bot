import asyncio
from os import environ, remove
import discord
from discord.ext import commands
from pytubefix import YouTube

from helpers.playlist import Playlist
from helpers.validators import is_valid_youtube_url

intents = discord.Intents.default()
intents.message_content = True  # Ensure message content intent is enabled

bot = commands.Bot(command_prefix="!", intents=intents)

# Your bot token here
TOKEN = environ.get("DISCORD_BOT_TOKEN")

playlist = Playlist(bot)


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user.name}")


@bot.command(name="play", help="Play audio from a YouTube link in your voice channel")
async def play(ctx, url: str):
    # Validate the URL to ensure it is a valid YouTube URL
    if not is_valid_youtube_url(url):
        await ctx.send("The link you provided is not a valid YouTube URL.")
        return

    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    # Get the voice channel of the user
    channel = ctx.author.voice.channel

    # Check if the user is in the same voice channel as the bot
    if ctx.voice_client is not None and ctx.voice_client.channel != channel:
        await ctx.send("I'm already in another voice channel.")
        return

    playlist.add(url)
    await ctx.send(f"Added to playlist: {url}")

    if not playlist.voice_client:
        connected = await playlist.connect(ctx)
        if connected:
            await playlist.play_next()
    elif not playlist.voice_client.is_playing():
        await playlist.play_next()


@bot.command(
    name="stop", help="Stop the currently playing audio and leave the voice channel"
)
async def stop(ctx):
    await playlist.stop()


@bot.command(
    name="skip",
    help="Skip the currently playing audio and play the next song in the playlist",
)
async def skip(ctx):
    await playlist.skip()


bot.run(TOKEN)
