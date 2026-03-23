import os
from yt_dlp import YoutubeDL

pasta_download = os.path.join(os.path.expanduser("~"), "Music")
os.makedirs(pasta_download, exist_ok=True)
opcoes_base_audio = {
    "format": "bestaudio/best",
    "outtmpl": os.path.join(pasta_download, "%(title)s.%(ext)s"),
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def music():
    limpar_tela()
    print("{:=^100}".format(" Baixar Música ")+"\n")
    music = input("Qual o link da música a ser baixada?: ")
    opcoes = opcoes_base_audio.copy()
    with YoutubeDL(opcoes) as ydl:
        ydl.download([music])
    limpar_tela()
    music_finish()

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

def init():
    print("{:=^100}".format(" DownTube ")+"\n")
    print("1 - Baixar música")
    print("2 - Baixar playlist")
    print("0 - Sair\n")
    print("="*100+"\n")

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