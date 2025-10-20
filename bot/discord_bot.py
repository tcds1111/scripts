import discord
from discord.ext import commands
import yt_dlp as youtube_dl

TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extractaudio': True,
    'audioformat': "mp3",
    'default_search': 'auto',
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f'Bot online como {bot.user}!')

@bot.command()
async def tocar(ctx, url):
    if not ctx.author.voice:
        await ctx.send("Você precisa estar em um canal de voz!")
        return

    canal = ctx.author.voice.channel
    voz = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voz:
        voz = await canal.connect()

    info = ytdl.extract_info(url, download=False)
    url_audio = info['url']
    voz.play(discord.FFmpegPCMAudio(url_audio, **ffmpeg_options))

    await ctx.send(f"Tocando: {info['title']}")

bot.run(TOKEN)
