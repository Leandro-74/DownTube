# Arquivo configurações, contém caminhos padrões e opção para configurações personalizadas

import atexit
import os
import subprocess
import sys
import time
import importlib.util
from yt_dlp import YoutubeDL


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Localiza os arquivos do ffmpeg
def get_ffmpeg_path():
    # Se estiver rodando como executável do PyInstaller
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    
    # Se estiver instalado no sistema (via makepkg), os binários estão em /usr/bin
    if os.path.exists('/usr/bin/ffmpeg') and os.path.exists('/usr/bin/bgutil-pot'):
        return '/usr/bin'
    
    # Caso contrário, usa o diretório do script (modo desenvolvimento)
    return os.path.dirname(os.path.abspath(__file__))

# Define o caminho dos arquivos do ffmpeg
ffmpeg_dir = get_ffmpeg_path()

# caminho PATH para uso do plugin do PO Token
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# Porta para rodar o servidor do BGUTIL
BGUTIL_PORT = 4416

# Localiza o binário do bgutil-pot
def get_bgutil_binary_path():
    base_dir = ffmpeg_dir
    nome_binario = "bgutil-pot.exe" if os.name == "nt" else "bgutil-pot"
    return os.path.join(base_dir, nome_binario)

# Localiza o caminho do yt-dlp-plugins
def get_plugin_path():
    # Primeiro tenta o caminho de instalação system-wide
    system_plugin = '/usr/share/downtube/yt-dlp-plugins/bgutil-ytdlp-pot-provider'
    if os.path.isdir(system_plugin):
        return system_plugin
    # Fallback para o diretório local (desenvolvimento)
    return os.path.join(ffmpeg_dir, "yt-dlp-plugins", "bgutil-ytdlp-pot-provider")


try:
    _plugin_spec = importlib.util.find_spec("yt_dlp_plugins.extractor.getpot_bgutil_http")
except ModuleNotFoundError:
    _plugin_spec = None

if _plugin_spec is None:
    plugin_path = get_plugin_path()
    if os.path.isdir(plugin_path):
        sys.path.insert(0, plugin_path)

_bgutil_processo = None

# Sobe o servidor do bgutil-pot em background
def iniciar_bgutil_server():
    global _bgutil_processo

    if _bgutil_processo is not None and _bgutil_processo.poll() is None:
        return  # já está rodando

    binario = get_bgutil_binary_path()
    if not os.path.isfile(binario):
        # Não impede o app de funcionar; só fica sem PO Token (volta pro 360p)
        print(f"[aviso] bgutil-pot não encontrado em {binario}, seguindo sem PO Token provider.")
        return

    try:
        _bgutil_processo = subprocess.Popen(
            [binario, "server", "--port", str(BGUTIL_PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        atexit.register(parar_bgutil_server)
        time.sleep(0.5)  # pequeno respiro pra ele subir antes do primeiro request
    except OSError as e:
        print(f"[aviso] Falha ao iniciar bgutil-pot: {e}")

# Encerra o servidor quando o processo do script for encerrado
def parar_bgutil_server():
    global _bgutil_processo
    if _bgutil_processo is not None and _bgutil_processo.poll() is None:
        _bgutil_processo.terminate()
        try:
            _bgutil_processo.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _bgutil_processo.kill()

# Inicia o servidor
iniciar_bgutil_server()

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
    "outtmpl": os.path.join(pastaVideo, "%(title)s.%(ext)s"),
    "merge_output_format": "mp4",
}