import logging
from os import environ
import discord
from discord.ext import commands
from discord.ext.commands import Context
from pytubefix import Playlist as YtPlaylist

from helpers.playlist import Playlist
from helpers.validators import is_in_a_playlist, is_valid_youtube_url
from helpers.logger import logger
intents = discord.Intents.default()
intents.message_content = True  # Ensure message content intent is enabled

bot = commands.Bot(command_prefix="!", intents=intents)

# Your bot token here
TOKEN = environ.get("DISCORD_BOT_TOKEN")


playlists :  dict[str, Playlist] = {}

@bot.event
async def on_ready():
    logger.info(f"Bot is ready. Logged in as {bot.user.name}")


@bot.command(name="play", help="Play audio from a YouTube link in your voice channel")
async def play(ctx: Context, url: str):
    # Validate the URL to ensure it is a valid YouTube URL
    if not is_valid_youtube_url(url):
        await ctx.send("The link you provided is not a valid YouTube URL.")
        return
    
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel.")
        return
    
    # Get or create playlist for this guild
    playlist = playlists.get(ctx.guild.id)
    if not playlist:
        playlists[ctx.guild.id] = Playlist(guild_id=ctx.guild.id)
        playlist = playlists[ctx.guild.id]
    
    # If it is part of a playlist, get the whole playlist.
    if is_in_a_playlist(url):
        yt_playlist = YtPlaylist(url)
        logger.info(yt_playlist)
        logger.info(yt_playlist.videos)
        playlist.add_playlist(yt_playlist.videos)

        await ctx.send(f"Added {len(yt_playlist.videos)} to the playlist.")
    else:
        playlist.add(url)
        await ctx.send(f"Added to playlist: {url}")

    # Get the voice channel of the user
    channel = ctx.author.voice.channel

    # Check if the user is in the same voice channel as the bot
    if ctx.voice_client is not None and ctx.voice_client.channel != channel:
        await ctx.send("I'm already in another voice channel.")
        return

    if not playlist.voice_client:
        connected = await playlist.connect(ctx)
        if connected:
            await playlist.play_next()
    elif not playlist.voice_client.is_playing():
        await playlist.play_next()


@bot.command(
    name="stop", help="Stop the currently playing audio and leave the voice channel"
)
async def stop(ctx: Context):
    playlist = playlists.get(ctx.guild.id)
    if playlist is None:
        await ctx.send("I'm not connected to a voice channel.")
        return
    
    await playlist.stop()


@bot.command(
    name="skip",
    help="Skip the currently playing audio and play the next song in the playlist",
)
async def skip(ctx: Context):
    playlist = playlists.get(ctx.guild.id)
    if playlist is None:
        await ctx.send("I'm not connected to a voice channel.")
        return
    
    await playlist.skip()

@bot.command(
    name="clear", help="Clear the playlist"
)
async def clear(ctx: Context):
    playlist = playlists.get(ctx.guild.id)
    if playlist is None:
        await ctx.send("I'm not connected to a voice channel.")
        return 
    
    await playlist.clear()

bot.run(token=TOKEN, log_level=logging.INFO)

