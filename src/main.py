from os import environ
import discord
from discord.ext import commands
from discord.ext.commands import Context
from spotipy import Spotify
from external_backend.spotify import SpotifyExternalBackend
from external_backend.youtube import YoutubeExternalBackend
from helpers.playlist import Playlist
from helpers.logger import logger

intents = discord.Intents.default()
intents.message_content = True  # Ensure message content intent is enabled

bot = commands.Bot(command_prefix="!", intents=intents)

# Your bot token here
TOKEN = environ.get("DISCORD_BOT_TOKEN")


playlists: dict[str, Playlist] = {}
spotify: Spotify | None = None


@bot.event
async def on_ready():
    logger.info(f"Bot is ready. Logged in as {bot.user.name}")


@bot.command(name="play", help="Play audio from a YouTube link in your voice channel")
async def play(ctx: Context, url: str):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    # Get or create playlist for this guild
    playlist = playlists.get(ctx.guild.id)
    if not playlist:
        playlists[ctx.guild.id] = Playlist(guild_id=ctx.guild.id)
        playlist = playlists[ctx.guild.id]

    # Check whether we are dealing with Spotify or YouTube
    if "spotify" in url:
        external_backend = SpotifyExternalBackend(ctx)
    elif (
        "youtu" in url
    ):  # Some YouTube URLs look like "youtu.be" so we need to check for "youtu" instead of "youtube"
        external_backend = YoutubeExternalBackend(ctx)
    else:
        await ctx.send("The link you provided is not a valid YouTube or Spotify URL.")
        return

    # Check if the URL is valid
    if not external_backend.is_valid_url(url):
        await ctx.send("The link you provided is not a valid YouTube or Spotify URL.")
        return

    # If it is part of a playlist, get the whole playlist.
    if external_backend.is_in_a_playlist(url):
        tracks_urls = await external_backend.get_playlist_youtube_urls(url)
        playlist.add_playlist(tracks_urls)
        await ctx.send(f"Added {len(tracks_urls)} to the playlist.")
    else:
        url = await external_backend.get_track_youtube_url(url)
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
async def skip(ctx: Context, amount: int = 1):
    playlist = playlists.get(ctx.guild.id)
    if playlist is None:
        await ctx.send("I'm not connected to a voice channel.")
        return

    await playlist.skip(amount)


@bot.command(name="clear", help="Clear the playlist")
async def clear(ctx: Context):
    playlist = playlists.get(ctx.guild.id)
    if playlist is None:
        await ctx.send("I'm not connected to a voice channel.")
        return

    await playlist.clear()


if __name__ == "__main__":
    bot.run(TOKEN)
