# yt_playlist_downloader_ydlp.py
import os
import subprocess

# Arquivo com URLs de playlists
playlists_file = "playlists.txt"
# Pasta base para salvar músicas
base_dir = "musicas"
# Caminho para cookies do navegador exportados (veja abaixo)
cookies_file = "cookies.txt"

os.makedirs(base_dir, exist_ok=True)

# Lê links do arquivo
with open(playlists_file, "r") as f:
    playlist_urls = [line.strip() for line in f if line.strip()]

for pl_url in playlist_urls:
    try:
        # Descobre o nome da playlist usando yt-dlp
        result = subprocess.run(
            ["yt-dlp", "--get-title", "--flat-playlist", pl_url],
            capture_output=True, text=True
        )
        playlist_name = pl_url.split("list=")[-1]
        if result.stdout:
            playlist_name = result.stdout.splitlines()[0]

        playlist_dir = os.path.join(base_dir, playlist_name)
        os.makedirs(playlist_dir, exist_ok=True)
        print(f"\nBaixando playlist: {playlist_name}")

        # Comando yt-dlp para baixar áudio em MP3
        command = [
            "yt-dlp",
            "-ciw",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--yes-playlist",
            "--cookies-from-browser", "edge",  # <- aqui
            "-o", os.path.join(playlist_dir, "%(title)s.%(ext)s"),
            pl_url
        ]


        subprocess.run(command)

    except Exception as e:
        print(f"❌ Erro ao processar {pl_url}: {e}")

print("\nDownload concluído!")
