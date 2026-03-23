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
    print("{:=^100}".format(" Baixar Música "))
    print()
    music = input("Qual o link da música a ser baixada?: ")
    opcoes = opcoes_base_audio.copy()
    with YoutubeDL(opcoes) as ydl:
        ydl.download([music])
    limpar_tela()
    music_finish()

def music_finish():
    print("{:=^100}".format(" Baixar Música "))
    print()
    print("Música baixada com sucesso!")
    print()
    print("="*100)
    print("1 - Voltar")
    print("2 - Baixar outra música")
    print()
    finish_opt = input("Escolha uma opção: ")
    print()
    if finish_opt == "2":
        music()
    elif finish_opt == "1":
        limpar_tela()
    else:
        limpar_tela()
        print("opção inválida")
        print()
        music_finish()

def playlist():
    limpar_tela()
    print("{:=^100}".format(" Baixar Playlist "))
    print()
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
    print("{:=^100}".format(" Baixar Playlist "))
    print()
    print("Playlist baixada com sucesso!")
    print()
    print("="*100)
    print()
    print("1 - Voltar")
    print("2 - Baixar outra playlist")
    print()
    finish_opt = input("Escolha uma opção: ")
    print()
    if finish_opt == "2":
        playlist()
    elif finish_opt == "1":
        limpar_tela()
    else:
        limpar_tela()
        print("opção inválida")
        playlist_finish()

def video():
    limpar_tela()
    print("{:=^100}".format(" Baixar Vídeo "))
    print()
    url = input("Qual o link do vídeo a ser baixado?: ")

    with YoutubeDL({"quiet": True, "noplaylist": True}) as ydl:
        info = ydl.extract_info(url, download=False)

    formatos = info.get("formats", [])
    qualidades = {}

    # Filtra apenas formatos que possuem altura (vídeo)
    for f in formatos:
        altura = f.get("height")
        if altura:
            # Mantém a melhor variante para cada altura encontrada
            qualidades[altura] = f

    print("\nQualidades disponíveis:\n")
    opcoes_menu = []

    # Ordena as alturas numericamente
    alturas_ordenadas = sorted(qualidades.keys())

    for i, altura in enumerate(alturas_ordenadas, start=1):
        f = qualidades[altura]
        tamanho = f.get("filesize") or f.get("filesize_approx")
        tamanho_str = f"{tamanho / 1024 / 1024:.1f} MB" if tamanho else "tamanho desconhecido"

        print(f"{i} - {altura}p ({tamanho_str})")
        opcoes_menu.append(altura)  # Armazena a altura para o seletor

    escolha = int(input("\nEscolha a qualidade: "))
    altura_escolhida = opcoes_menu[escolha - 1]

    opcoes_download = {
        # Seleciona a altura específica e junta com o melhor áudio disponível
        "format": f"bestvideo[height={altura_escolhida}]+bestaudio/best[height={altura_escolhida}]",
        "outtmpl": os.path.join(pasta_download, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",  # Garante compatibilidade após o merge
    }

    with YoutubeDL(opcoes_download) as ydl:
        ydl.download([url])

    limpar_tela()
    video_finish()

def video_finish():
    print("{:=^100}".format(" Baixar Vídeo "))
    print()
    print("Vídeo baixado com sucesso!")
    print()
    print("=" * 100)
    print()
    print("1 - Voltar")
    print("2 - Baixar outro Vídeo")
    print()
    finish_opt = input("Escolha uma opção: ")
    print()
    if finish_opt == "2":
        video()
    elif finish_opt == "1":
        limpar_tela()
    else:
        limpar_tela()
        print("opção inválida")
        video_finish()

def init():
    print("{:=^100}".format(" DownTube "))
    print()
    print("1 - Baixar música")
    print("2 - Baixar playlist")
    print("3 - Baixar vídeo")
    print("0 - Sair")
    print()
    print("="*100)
    print()

while True:
    limpar_tela()
    
    init()
    
    opt = input("Digite a opção desejada: ")
    
    if opt == "1":
        music()
    elif opt == "2":
        playlist()
    elif opt == "3":
        video()
    elif opt == "0":
        break
    else:
        print("Opção inválida.")