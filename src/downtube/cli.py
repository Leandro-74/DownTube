# cli.py — ações de download e loop principal

import json
import os
import subprocess
import sys

import config
import menu


# Limpa o terminal (cls no Windows, clear nos demais)
def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


# Roda o yt-dlp herdando a saída. Retorna True em caso de sucesso
def _executar(args: list) -> bool:
    try:
        codigo = subprocess.run([config.YTDLP, *args]).returncode
    except OSError as e:
        print(f"\nErro ao executar o yt-dlp: {e}")
        menu.pausar()
        return False

    if codigo != 0:
        print(f"\nO download falhou (yt-dlp retornou código {codigo}).")
        menu.pausar()
        return False
    return True


# Depois de um download: True = baixar outro, False = voltar ao menu
def _menu_final(tipo: str) -> bool:
    aviso = ""
    while True:
        limpar_tela()
        escolha = menu.perguntar(menu.linhas_final(tipo, aviso), "Escolha uma opção: ")
        if escolha == "2":
            return True
        if escolha in ("1", "0", ""):
            return False
        aviso = "Opção inválida."


# Pede o link e baixa em loop, até o usuário voltar ao menu
def _baixar_em_loop(tipo: str, montar_args) -> None:
    while True:
        limpar_tela()
        link = menu.perguntar(menu.linhas_link(tipo), "Link: ")
        if not link:
            return

        if not _executar([*montar_args(), link]):
            continue
        if not _menu_final(tipo):
            return


def _acao_musica() -> None:
    _baixar_em_loop("Música", config.args_musica)


def _acao_playlist() -> None:
    _baixar_em_loop("Playlist", config.args_playlist)


# Retorna as alturas disponíveis, ou None se não foi possível analisar
def _listar_alturas(link: str):
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


def _acao_video() -> None:
    while True:
        limpar_tela()
        link = menu.perguntar(menu.linhas_link("Vídeo"), "Link: ")
        if not link:
            return

        alturas = _listar_alturas(link)
        if alturas is None:
            print("\nNão foi possível obter as informações do vídeo.")
            menu.pausar()
            continue
        if not alturas:
            print("Nenhuma resolução de vídeo encontrada!")
            menu.pausar()
            continue

        aviso = ""
        while True:
            limpar_tela()
            escolha = menu.perguntar(
                menu.linhas_resolucao(alturas, aviso), "Escolha uma opção: "
            )
            if escolha in ("0", ""):
                return
            if escolha.isdigit() and 1 <= int(escolha) <= len(alturas):
                break
            aviso = "Opção inválida."

        altura = alturas[int(escolha) - 1]
        limpar_tela()
        print(f"Baixando em {altura}p...\n")
        if not _executar([*config.args_video(altura), link]):
            continue
        if not _menu_final("Vídeo"):
            return


# Loop principal: redesenha o menu e despacha a opção escolhida
def run() -> None:
    acoes = {
        "1": _acao_musica,
        "2": _acao_playlist,
        "3": _acao_video,
    }
    aviso = ""
    while True:
        limpar_tela()
        escolha = menu.perguntar(menu.linhas_principal(aviso), "Escolha uma opção: ")
        aviso = ""
        if escolha == "0":
            return

        acao = acoes.get(escolha)
        if acao is None:
            aviso = "Opção inválida."
            continue
        acao()


# Entry point chamado pelo main.py
def main() -> None:
    # Saída redirecionada (pipe/arquivo) usa a codificação do sistema, que não
    # cobre os caracteres da caixa: força UTF-8 nesse caso
    if not sys.stdout.isatty():
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nSaindo...")
