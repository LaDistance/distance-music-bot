from typing import List
from discord import VoiceClient, FFmpegPCMAudio
from discord.ext.commands import Context
from pytubefix import YouTube
import os
import asyncio


class Playlist:
    def __init__(self, guild_id: str):
        self.guild_id: str = None
        self.queue: List[str] = []
        self.voice_client : VoiceClient = None
        self.current_ctx : Context = None
        self.max_queue_size = 200

    def add(self, url: str) -> None:
        if len(self.queue) >= self.max_queue_size:
            raise ValueError("The playlist is full.")
        self.queue.append(url)

    def add_playlist(self, videos: List[YouTube]) -> None:
        if len(self.queue) + len(videos) > self.max_queue_size:
            raise ValueError("The playlist is full.")
        
        for video in videos:
            self.queue.append(video.watch_url)

    def next(self) -> str | None:
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    async def connect(self, ctx: Context) -> bool:
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

    async def disconnect(self) -> None:
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None
            await self.current_ctx.send("Disconnected from the voice channel.")

    async def play_next(self) -> None:
        if self.is_empty():
            await self.current_ctx.send("The playlist is empty.")
            await self.disconnect()
            return

        url = self.next()
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file = stream.download(filename="audio.mp4")

        source = FFmpegPCMAudio(
            audio_file,
        )
        self.voice_client.play(source)

        await self.current_ctx.send(f"Now playing: {yt.title}")

        while self.voice_client.is_playing():
            await asyncio.sleep(1)

        os.remove(audio_file)
        await self.play_next()

    async def handle_next(self) -> None:
        await self.play_next()

    async def stop(self) -> None:
        if self.voice_client is not None:
            await self.disconnect()
            await self.queue.clear()

    async def skip(self) -> None:
        if self.voice_client is not None:
            self.voice_client.stop()
            await self.play_next()
        else:
            await self.current_ctx.send("Not currently playing anything.")

    async def clear(self) -> None:
        self.queue.clear()
        self.voice_client.stop()
        await self.current_ctx.send("Playlist cleared.")
