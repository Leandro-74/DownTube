import os

from yt_dlp import YoutubeDL

import config


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def _cabecalho(titulo):
    print("{:=^100}".format(f" {titulo} ") + "\n")


def _pedir_link(titulo, pergunta):
    limpar_tela()
    _cabecalho(titulo)
    return input(pergunta).strip()


def _baixar(titulo, link, opcoes):
    try:
        with YoutubeDL(opcoes) as ydl:
            ydl.download([link])
        return True
    except Exception as e:
        print(f"\nOcorreu um erro ao baixar: {e}")
        input("\nPressione ENTER para continuar...")
        return False


def _menu_final(titulo):
    """Depois de um download: True = baixar outro, False = voltar ao menu."""
    while True:
        limpar_tela()
        _cabecalho(titulo)
        print("Download concluído!\n")
        print("=" * 100 + "\n")
        print("1 - Voltar")
        print("2 - Baixar outro\n")
        opt = input("Escolha uma opção: ").strip()

        if opt == "2":
            return True
        if opt == "1":
            return False
        else:
            limpar_tela()
            print("Opção inválida.\n")


def _baixar_em_loop(titulo, pergunta, montar_opcoes):
    while True:
        link = _pedir_link(titulo, pergunta)
        if not link:
            return

        if not _baixar(titulo, link, montar_opcoes()):
            continue
        if not _menu_final(titulo):
            return


def baixar_musica():
    _baixar_em_loop(
        "Baixar Música",
        "Qual o link da música a ser baixada?: ",
        config.opcoes_audio,
    )


def baixar_playlist():
    _baixar_em_loop(
        "Baixar Playlist",
        "Qual o link da playlist a ser baixada?: ",
        config.opcoes_playlist,
    )


def baixar_video():
    while True:
        link = _pedir_link("Baixar Vídeo", "Qual o link do vídeo a ser baixado?: ")
        if not link:
            return

        # Lista as resoluções disponíveis sem baixar nada
        try:
            with YoutubeDL(config.opcoes_video()) as ydl:
                infos = ydl.extract_info(link, download=False)
            alturas = sorted({
                f["height"]
                for f in infos.get("formats", [])
                if f.get("vcodec") != "none" and f.get("height")
            })
        except Exception as e:
            print(f"\nOcorreu um erro ao analisar o vídeo: {e}")
            input("\nPressione ENTER para continuar...")
            continue

        if not alturas:
            print("Nenhuma resolução de vídeo encontrada!")
            input("\nPressione ENTER para tentar novamente...")
            continue

        limpar_tela()
        _cabecalho("Resolução")
        for i, altura in enumerate(alturas, start=1):
            print(f"[{i}] {altura}p")
        print("[0] Cancelar\n")

        escolha = input("Qual a resolução desejada?: ").strip()
        if escolha == "0":
            return
        if not escolha.isdigit() or not 1 <= int(escolha) <= len(alturas):
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")
            continue

        altura = alturas[int(escolha) - 1]
        opcoes = config.opcoes_video()
        # Prefere mp4+m4a (merge direto); o fallback pode sair em .mkv
        opcoes["format"] = (
            f"bestvideo[height={altura}][ext=mp4]+bestaudio[ext=m4a]"
            f"/bestvideo[height={altura}]+bestaudio/best[height={altura}]"
        )

        limpar_tela()
        print(f"Baixando em {altura}p...\n")
        if not _baixar("Baixar Vídeo", link, opcoes):
            continue
        if not _menu_final("Baixar Vídeo"):
            return
