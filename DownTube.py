import os
import sys
from yt_dlp import YoutubeDL

# Define a pasta de Músicas do usuário como caminho padrão para salvar as músicas e playlists
pasta_download = os.path.join(os.path.expanduser("~"), "Music")
os.makedirs(pasta_download, exist_ok=True)

# Define a pasta de Vídeos do usuário como caminho padrão para salvar os vídeos
pasta_video = os.path.join(os.path.expanduser("~"), "Videos")
os.makedirs(pasta_video, exist_ok=True)

# Localiza os arquivos do ffmpeg
def get_ffmpeg_path():
    # Se estiver rodando como executável do PyInstaller
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # Se estiver rodando como script .py normal
    return os.path.dirname(os.path.abspath(__file__))

ffmpeg_dir = get_ffmpeg_path()

# Define as opções globais para download de músicas e playlists
opcoes_base_audio = {
    "format": "bestaudio/best",
    "ffmpeg_location": ffmpeg_dir,
    "outtmpl": os.path.join(pasta_download, "%(title)s.%(ext)s"),
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
    "ffmpeg_location": ffmpeg_dir,
    "outtmpl": os.path.join(pasta_video, "%(title)s.%(ext)s"),
    "merge_output_format": "mp4",
}


# Função padrão para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função que executa o download de vídeos
def baixar_video():
    while True:
        limpar_tela()

        print("{:=^100}".format(" Baixar Vídeo ")+"\n")
        link_video = input("Qual o link do vídeo a ser baixado?: ")

        opcoes = opcoes_base_video.copy()
        with YoutubeDL(opcoes) as ydl:
            ydl.download([link_video])
        limpar_tela()

        while True:
            print("{:=^100}".format(" Baixar Vídeo ")+"\n")
            print("Vídeo baixado com sucesso!\n")
            print("="*100)
            print("1 - Voltar")
            print("2 - Baixar outro vídeo\n")
            finish_opt = input("Escolha uma opção: \n")
            if finish_opt == "2":
                break
            elif finish_opt == "1":
                return
            else:
                limpar_tela()
                print("opção inválida\n")

# Função que executa o download de músicas
def baixar_musica():
    while True:
        limpar_tela()

        print("{:=^100}".format(" Baixar Música ")+"\n")
        link_musica = input("Qual o link da música a ser baixada?: ")

        opcoes = opcoes_base_audio.copy()
        with YoutubeDL(opcoes) as ydl:
            ydl.download([link_musica])
        limpar_tela()

        while True:
            print("{:=^100}".format(" Baixar Música ")+"\n")
            print("Música baixada com sucesso!\n")
            print("="*100)
            print("1 - Voltar")
            print("2 - Baixar outra música\n")
            finish_opt = input("Escolha uma opção: \n")
            if finish_opt == "2":
                break
            elif finish_opt == "1":
                return
            else:
                limpar_tela()
                print("opção inválida\n")

# Função que executa o download de playlists
def baixar_playlist():
    while True:
        limpar_tela()

        print("{:=^100}".format(" Baixar Playlist ")+"\n")
        link_playlist = input("Qual o link da playlist a ser baixada?: ")

        opcoes = opcoes_base_audio.copy()
        opcoes["outtmpl"] = os.path.join(
            pasta_download,
            "%(playlist_title)s",
            "%(playlist_index)02d - %(title)s.%(ext)s"
        )

        opcoes["ignoreerrors"] = True
        with YoutubeDL(opcoes) as ydl:
            ydl.download([link_playlist])
        limpar_tela()

        while True:
            print("{:=^100}".format(" Baixar Playlist ")+"\n")
            print("Playlist baixada com sucesso!\n")
            print("="*100+"\n")
            print("1 - Voltar")
            print("2 - Baixar outra playlist\n")
            finish_opt = input("Escolha uma opção: \n")

            if finish_opt == "2":
                break
            elif finish_opt == "1":
                return
            else:
                limpar_tela()
                print("opção inválida\n")

# Tela inicial
def init():
    print("{:=^100}".format(" DownTube ")+"\n")
    print("1 - Baixar música")
    print("2 - Baixar playlist")
    print("3 - Baixar Vídeo")
    print("0 - Sair\n")
    print("="*100+"\n")

# Loop para fazer o encaminhamento das funções
while True:
    limpar_tela()
    
    init()
    
    opt = input("Digite a opção desejada: ")
    
    if opt == "1":
        baixar_musica()
    elif opt == "2":
        baixar_playlist()
    elif opt == "3":
        baixar_video()
    elif opt == "0":
        break
    else:
        print("Opção inválida.")