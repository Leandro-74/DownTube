import os
import sys
from yt_dlp import YoutubeDL
import config


# Função padrão para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função que executa o download de vídeos
def baixar_video():
    while True:
        limpar_tela()

        print("{:=^100}".format(" Baixar Vídeo ")+"\n")
        link_video = input("Qual o link do vídeo a ser baixado?: ")

        opcoes = config.opcoes_base_video.copy()
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

        opcoes = config.opcoes_base_audio.copy()
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

        opcoes = config.opcoes_base_audio.copy()
        opcoes["outtmpl"] = os.path.join(
            config.pastaMusica,
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