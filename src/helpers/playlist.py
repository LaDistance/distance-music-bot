import discord
from pytubefix import YouTube
import os
import asyncio


class Playlist:
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.voice_client = None
        self.current_ctx = None
        self.max_queue_size = 10

    def add(self, url):
        if len(self.queue) >= self.max_queue_size:
            raise ValueError("The playlist is full.")
        self.queue.append(url)

    def next(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0

    async def connect(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            return False

        channel = ctx.author.voice.channel
        if self.voice_client is None:
            self.voice_client = await channel.connect()
        elif self.voice_client.channel != channel:
            await self.voice_client.move_to(channel)

        self.current_ctx = ctx
        return True

    async def play_next(self):
        if self.is_empty():
            await self.current_ctx.send("The playlist is empty.")
            return

        url = self.next()
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file = stream.download(filename="audio.mp4")

        source = discord.FFmpegPCMAudio(
            audio_file,
        )
        self.voice_client.play(source)

        await self.current_ctx.send(f"Now playing: {yt.title}")

        while self.voice_client.is_playing():
            await asyncio.sleep(1)

        os.remove(audio_file)

    async def handle_next(self):
        await self.play_next()

    async def stop(self):
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None
            await self.current_ctx.send("Disconnected from the voice channel.")

    async def skip(self):
        if self.voice_client is not None:
            self.voice_client.stop()
            await self.play_next()
        else:
            await self.current_ctx.send("Not currently playing anything.")
