import os
import sys
from yt_dlp import YoutubeDL

# Define a pasta de Músicas do usuário como caminho padrão para salvar os downloads
pasta_download = os.path.join(os.path.expanduser("~"), "Music")
os.makedirs(pasta_download, exist_ok=True)

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

# Função padrão para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função que executa o download de músicas
def music():
    limpar_tela()
    print("{:=^100}".format(" Baixar Música ")+"\n")
    music = input("Qual o link da música a ser baixada?: ")
    opcoes = opcoes_base_audio.copy()
    with YoutubeDL(opcoes) as ydl:
        ydl.download([music])
    limpar_tela()
    music_finish()

# Função da tela de finalização em download de músicas
def music_finish():
    print("{:=^100}".format(" Baixar Música ")+"\n")
    print("Música baixada com sucesso!\n")
    print("="*100)
    print("1 - Voltar")
    print("2 - Baixar outra música\n")
    finish_opt = input("Escolha uma opção: \n")
    if finish_opt == "2":
        music()
    elif finish_opt == "1":
        limpar_tela()
    else:
        limpar_tela()
        print("opção inválida\n")
        music_finish()

# Função que executa o download de playlists
def playlist():
    limpar_tela()
    print("{:=^100}".format(" Baixar Playlist ")+"\n")
    playlist = input("Qual o link da playlist a ser baixada?: ")
    opcoes = opcoes_base_audio.copy()
    opcoes["outtmpl"] = os.path.join(
        pasta_download,
        "%(playlist_title)s",
        "%(playlist_index)02d - %(title)s.%(ext)s"
    )
    opcoes["ignoreerrors"] = True
    with YoutubeDL(opcoes) as ydl:
        ydl.download([playlist])
    limpar_tela()
    playlist_finish()

# Função da tela de finalização em download de playlists
def playlist_finish():
    print("{:=^100}".format(" Baixar Playlist ")+"\n")
    print("Playlist baixada com sucesso!\n")
    print("="*100+"\n")
    print("1 - Voltar")
    print("2 - Baixar outra playlist\n")
    finish_opt = input("Escolha uma opção: \n")
    if finish_opt == "2":
        playlist()
    elif finish_opt == "1":
        limpar_tela()
    else:
        limpar_tela()
        print("opção inválida")
        playlist_finish()

# Tela inicial
def init():
    print("{:=^100}".format(" DownTube ")+"\n")
    print("1 - Baixar música")
    print("2 - Baixar playlist")
    print("0 - Sair\n")
    print("="*100+"\n")

# Loop para fazer o encaminhamento das funções
while True:
    limpar_tela()
    
    init()
    
    opt = input("Digite a opção desejada: ")
    
    if opt == "1":
        music()
    elif opt == "2":
        playlist()
    elif opt == "0":
        break
    else:
        print("Opção inválida.")