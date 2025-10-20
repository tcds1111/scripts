import os
import subprocess
import re

def sanitize_filename(name, max_length=100):
    """Remove caracteres inválidos e limita o tamanho do nome da pasta"""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)  # remove chars proibidos
    return name[:max_length].strip() or "Playlist_Sem_Nome"

def get_playlist_title(url, browser="safari"):
    """Usa yt-dlp para pegar o título da playlist sem baixar nada"""
    result = subprocess.run(
        ["yt-dlp", "--cookies-from-browser", browser, "--flat-playlist", "--print", "%(playlist_title)s", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Pega só a primeira linha
    lines = result.stdout.strip().splitlines()
    title = lines[0] if lines else "videos_avulsos"
    return sanitize_filename(title)

def baixar_playlist(url, browser="safari"):
    # Descobre se é playlist ou vídeo único
    playlist_title = get_playlist_title(url, browser)

    if playlist_title == "videos_avulsos":  
        pasta_destino = os.path.join("musicas", "videos_avulsos")
    else:
        pasta_destino = os.path.join("musicas", playlist_title)

    os.makedirs(pasta_destino, exist_ok=True)

    # Monta comando yt-dlp
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3", "--audio-quality", "192K",
        "-o", os.path.join(pasta_destino, "%(title)s.%(ext)s"),
        "--cookies-from-browser", browser,
        url
    ]

    print(f"\n📂 Baixando em: {pasta_destino}\n")
    subprocess.run(cmd)

if __name__ == "__main__":
    url = input("🔗 Digite o link da playlist ou vídeo: ").strip()
    navegador = input("🌐 Qual navegador você usa (safari/chrome/firefox/edge)? ").strip().lower() or "edge"

    if url:
        baixar_playlist(url, navegador)
    else:
        print("⚠ Nenhum link informado.")
