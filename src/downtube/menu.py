# menu.py — apresentação do CLI: monta as linhas e desenha a caixa

import shutil

# Largura interna das caixas e prefixo dos escapes ANSI
LARGURA = 72
ESC = "\x1b"


def _pad_horizontal() -> int:
    try:
        cols = shutil.get_terminal_size().columns
    except Exception:
        cols = LARGURA + 2
    return max(0, (cols - (LARGURA + 2)) // 2)


def _pad_vertical(total_linhas: int) -> int:
    try:
        rows = shutil.get_terminal_size().lines
    except Exception:
        return 0
    return max(0, (rows - total_linhas) // 2)


# Linha de conteúdo com bordas e preenchimento à direita
def _linha(texto: str = "") -> str:
    return "║" + (" " + texto).ljust(LARGURA) + "║"


# Bordas horizontais da caixa (topo, separador e base)
def _topo() -> str:
    return "╔" + "═" * LARGURA + "╗"


def _sep() -> str:
    return "╠" + "═" * LARGURA + "╣"


def _fundo() -> str:
    return "╚" + "═" * LARGURA + "╝"


# Conteúdo do menu principal
def linhas_principal(aviso: str = "") -> list:
    linhas = [
        "DownTube",
        "Vídeos, músicas e playlists do YouTube",
        _sep(),
        "1. Baixar música",
        "2. Baixar playlist",
        "3. Baixar vídeo",
        "0. Sair",
    ]
    if aviso:
        linhas += [_sep(), aviso]
    return linhas


# Tela de entrada do link
def linhas_link(tipo: str) -> list:
    return [
        f"DownTube - Baixar {tipo}",
        _sep(),
        "Cole o link abaixo e pressione Enter.",
        "Deixe vazio para voltar.",
    ]


# Lista de resoluções disponíveis
def linhas_resolucao(alturas: list, aviso: str = "") -> list:
    linhas = ["DownTube - Escolher resolução", _sep()]
    linhas += [f"{i}. {altura}p" for i, altura in enumerate(alturas, start=1)]
    linhas += [_sep(), "0. Cancelar"]
    if aviso:
        linhas.append(aviso)
    return linhas


# Tela de encerramento de um download
def linhas_final(tipo: str, aviso: str = "") -> list:
    linhas = [
        f"DownTube - Baixar {tipo}",
        _sep(),
        "Download concluído!",
        _sep(),
        "1. Voltar ao menu",
        "2. Baixar outro",
    ]
    if aviso:
        linhas += [_sep(), aviso]
    return linhas


# Desenha a caixa completa e devolve o cursor para dentro dela, após o prompt
def abrir_caixa(linhas: list, prompt: str) -> None:
    pad = _pad_horizontal()
    total = len(linhas) + 4
    print("\n" * _pad_vertical(total), end="")

    def out(s: str) -> None:
        print(" " * pad + s)

    out(_topo())
    for linha in linhas:
        out(linha if linha.startswith("╠") else _linha(linha))
    out(_sep())
    texto = " " + prompt
    out("║" + texto + " " * max(1, LARGURA - len(texto)) + "║")
    out(_fundo())
    col = pad + 2 + len(texto)
    print(f"{ESC}[2A{ESC}[{col}G", end="", flush=True)


# Pula a base já desenhada para o próximo print não a sobrescrever
def fechar_caixa() -> None:
    print(f"{ESC}[1B", end="", flush=True)


# Desenha a caixa, colhe a resposta digitada dentro dela e devolve o valor
def perguntar(linhas: list, prompt: str) -> str:
    abrir_caixa(linhas, prompt)
    valor = input()
    fechar_caixa()
    return valor.strip()


# Espera o usuário ler uma mensagem antes de limpar a tela
def pausar() -> None:
    input("\nPressione ENTER para continuar...")
