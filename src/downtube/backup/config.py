# Arquivo configurações, contém caminhos padrões e opção para configurações personalizadas

import os
import sys
import atexit
import subprocess
import time
from yt_dlp import YoutubeDL


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Localiza os arquivos do ffmpeg
def get_ffmpeg_path():
    # Se estiver rodando como executável do PyInstaller
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # Se estiver rodando como script .py normal
    return os.path.dirname(os.path.abspath(__file__))

# Define o caminho dos arquivos do ffmpeg
ffmpeg_dir = get_ffmpeg_path()

BGUTIL_PORT = 4416
 
def get_bgutil_binary_path():
    """Localiza o binário do bgutil-pot, tanto rodando como script quanto
    congelado pelo PyInstaller (nesse caso ele fica junto do ffmpeg)."""
    base_dir = ffmpeg_dir
    nome_binario = "bgutil-pot.exe" if os.name == "nt" else "bgutil-pot"
    return os.path.join(base_dir, nome_binario)
 
def get_plugin_path():
    """Caminho do plugin yt_dlp_plugins embutido junto do projeto/bundle."""
    return os.path.join(ffmpeg_dir, "yt-dlp-plugins", "bgutil-ytdlp-pot-provider")
 
# Garante que o plugin é encontrado independente de pip install/PYTHONPATH,
# tanto em dev quanto dentro do .exe/pacote Arch
plugin_path = get_plugin_path()
if plugin_path not in sys.path and os.path.isdir(plugin_path):
    sys.path.insert(0, plugin_path)
 
_bgutil_processo = None
 
def iniciar_bgutil_server():
    """Sobe o servidor bgutil-pot em background, se ainda não estiver rodando."""
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
 
def parar_bgutil_server():
    global _bgutil_processo
    if _bgutil_processo is not None and _bgutil_processo.poll() is None:
        _bgutil_processo.terminate()
        try:
            _bgutil_processo.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _bgutil_processo.kill()
 
# Importa o plugin explicitamente (em vez de depender só da autodiscovery do
# yt-dlp), pra funcionar de forma confiável mesmo dentro do bundle PyInstaller
try:
    import yt_dlp_plugins.extractor.getpot_bgutil_http  # noqa: F401
except ImportError:
    print("[aviso] Plugin bgutil-ytdlp-pot-provider não encontrado; resoluções altas podem ficar indisponíveis.")
 
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
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "ios", "web"],
        }
    },
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
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "ios", "web"],
        }
    },
    "outtmpl": os.path.join(pastaVideo, "%(title)s.%(ext)s"),
    "merge_output_format": "mp4",
}