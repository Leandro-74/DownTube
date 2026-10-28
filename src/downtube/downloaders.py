import json
import os
import subprocess

import config


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def _cabecalho(titulo):
    print("{:=^100}".format(f" {titulo} ") + "\n")


def _pedir_link(titulo, pergunta):
    limpar_tela()
    _cabecalho(titulo)
    return input(pergunta).strip()


def _executar(args):
    """Roda o yt-dlp herdando a saída. Retorna True em caso de sucesso."""
    try:
        codigo = subprocess.run([config.YTDLP, *args]).returncode
    except OSError as e:
        print(f"\nErro ao executar o yt-dlp: {e}")
        input("\nPressione ENTER para continuar...")
        return False

    if codigo != 0:
        print(f"\nO download falhou (yt-dlp retornou código {codigo}).")
        input("\nPressione ENTER para continuar...")
        return False
    return True


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


def _baixar_em_loop(titulo, pergunta, montar_args):
    while True:
        link = _pedir_link(titulo, pergunta)
        if not link:
            return

        if not _executar([*montar_args(), link]):
            continue
        if not _menu_final(titulo):
            return


def baixar_musica():
    _baixar_em_loop(
        "Baixar Música",
        "Qual o link da música a ser baixada?: ",
        config.args_musica,
    )


def baixar_playlist():
    _baixar_em_loop(
        "Baixar Playlist",
        "Qual o link da playlist a ser baixada?: ",
        config.args_playlist,
    )


def _listar_alturas(link):
    """Retorna as alturas disponíveis, ou None se não foi possível analisar."""
    resultado = subprocess.run(
        [config.YTDLP, *config.args_metadados(), link],
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if resultado.returncode != 0:
        return None

    try:
        info = json.loads(resultado.stdout)
    except json.JSONDecodeError:
        return None

    return sorted({
        f["height"]
        for f in info.get("formats", [])
        if f.get("vcodec") != "none" and f.get("height")
    })


def baixar_video():
    while True:
        link = _pedir_link("Baixar Vídeo", "Qual o link do vídeo a ser baixado?: ")
        if not link:
            return

        alturas = _listar_alturas(link)
        if alturas is None:
            print("\nNão foi possível obter as informações do vídeo.")
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
        limpar_tela()
        print(f"Baixando em {altura}p...\n")
        if not _executar([*config.args_video(altura), link]):
            continue
        if not _menu_final("Baixar Vídeo"):
            return
