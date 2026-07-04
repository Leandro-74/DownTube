# Arquivo configurações, contém caminhos padrões e opção para configurações personalizadas

import os
import sys
from yt_dlp import YoutubeDL


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Localiza os arquivos do ffmpeg
def get_ffmpeg_path():
    # Se estiver rodando como executável do PyInstaller
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # Se estiver rodando como script .py normal
    return os.path.dirname(os.path.abspath(__file__))

# Define o caminho dos arquivos do ffmpeg
ffmpeg_dir = get_ffmpeg_path()

pastaMusica = ""
pastaVideo = ""

def caminhoPadrão():
    # Especifica o uso das variáveis globais
    global pastaMusica, pastaVideo

    # Define o caminho da pasta do usuário
    home = os.path.expanduser("~")

    # Define o caminho para as pastas em inglês
    pastaMusica_en = os.path.join(home, "Music")
    pastaVideo_en = os.path.join(home, "Videos")

    # Define o caminho para as pastas em português
    pastaMusica_pt = os.path.join(home, "Músicas")
    pastaVideo_pt = os.path.join(home, "Vídeos")

    # Define a pasta padrão para download das músicas e vídeos, dando prioridade para pt
    pastaMusica = pastaMusica_pt if os.path.exists(pastaMusica_pt) else pastaMusica_en
    pastaVideo = pastaVideo_pt if os.path.exists(pastaVideo_pt) else pastaVideo_en

    # Caso nenhuma das pastas exista, cria o diretório em inglês para padronização
    os.makedirs(pastaMusica, exist_ok=True)
    os.makedirs(pastaVideo, exist_ok=True)

caminhoPadrão()

def caminhoPersonalizado():
    # Pergunta o caminho a ser usado para músicas e playlists
    print("{:=^100}".format(" Alterar Caminhos ")+"\n")
    print("[1] Alterar caminho das músicas/playlists baixadas")
    print("[2] Alterar caminho dos vídeos baixados")
    print("[0] Cancelar"+"\n")
    opt = input("Que alteração deseja realizar?: ")

    # Checa a opção escolhida e da continuidade a personalização do caminho
    if opt == "1":
        limpar_tela()
        caminhoMusica = input("Qual caminho deseja especificar para download de músicas e playlists?: ")
        pastaMusica = caminhoMusica
    elif opt == "2":
        limpar_tela()
        caminhoVideo = input("Qual caminho deseja especificar para download de vídeos?: ")
        pastaVideo = caminhoVideo
    elif opt == "0":
        return
    else:
        limpar_tela()
        print("opção inválida, tente novamente...")
        caminhoPersonalizado()

# Define as opções globais para download de músicas e playlists
opcoes_base_audio = {
    "format": "bestaudio/best",
    "remote_components": ["ejs:github"],
    "ffmpeg_location": ffmpeg_dir,
    "outtmpl": os.path.join(pastaMusica, "%(title)s.%(ext)s"),
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "ios", "web"],
            "skip": ["hls", "dash"]
        }
    },
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}

# Define as opções globais para download de vídeos
opcoes_base_video = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "remote_components": ["ejs:github"],
    "ffmpeg_location": ffmpeg_dir,
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "ios", "web"],
            "skip": ["hls", "dash"]
        }
    },
    "outtmpl": os.path.join(pastaVideo, "%(title)s.%(ext)s"),
    "merge_output_format": "mp4",
}