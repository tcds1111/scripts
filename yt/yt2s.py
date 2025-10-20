#!/usr/bin/env python3
# yt2script.py
# Script atualizado para gerar transcript de vídeos do YouTube usando transcript oficial ou Whisper

import os
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import whisper

def get_video_id(url: str) -> str:
    """Extrai o ID do vídeo do link do YouTube."""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("URL inválida do YouTube")

def get_transcript_from_youtube(url: str):
    """Tenta pegar o transcript oficial do YouTube."""
    video_id = get_video_id(url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t['text'] for t in transcript])
        return text
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        print("Transcript oficial não encontrado:", str(e))
        return None
    except Exception as e:
        print("Erro ao buscar transcript oficial:", str(e))
        return None

def download_audio(video_url: str, filename: str = "audio.m4a") -> str:
    """Baixa o áudio do vídeo usando yt-dlp."""
    print("Baixando áudio para gerar transcript com Whisper...")
    cmd = ["yt-dlp", "-f", "bestaudio", "-o", filename, video_url]
    try:
        subprocess.run(cmd, check=True)
        return filename
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro ao baixar áudio com yt-dlp: {e}")

def generate_transcript_with_whisper(video_url: str) -> str:
    """Gera transcript usando Whisper."""
    audio_file = download_audio(video_url)
    print("Gerando transcript com Whisper...")
    model = whisper.load_model("medium")  # Pode trocar para "small", "base" ou "large"
    result = model.transcribe(audio_file)
    return result["text"]

def main():
    url = input("Cole o link do vídeo do YouTube: ").strip()
    
    # Primeiro tenta o transcript oficial
    transcript = get_transcript_from_youtube(url)
    
    if transcript:
        print("\n=== Transcript oficial do YouTube ===\n")
        print(transcript)
    else:
        print("\n=== Gerando transcript com Whisper ===\n")
        try:
            transcript = generate_transcript_with_whisper(url)
            print(transcript)
        except Exception as e:
            print("Falha ao gerar transcript com Whisper:", e)

if __name__ == "__main__":
    main()
