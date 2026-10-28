# Configurações: binários, PO Token e opções base do yt-dlp

import atexit
import importlib.util
import os
import subprocess
import sys
import time


# Localiza a pasta com os binários (ffmpeg, bgutil-pot)
def get_ffmpeg_path():
    # Executável do PyInstaller
    if getattr(sys, "frozen", False):
        return sys._MEIPASS

    # Instalado via makepkg, os binários ficam em /usr/bin
    if os.path.exists("/usr/bin/ffmpeg") and os.path.exists("/usr/bin/bgutil-pot"):
        return "/usr/bin"

    # Modo desenvolvimento: pasta do script
    return os.path.dirname(os.path.abspath(__file__))


ffmpeg_dir = get_ffmpeg_path()

# PATH para o plugin do PO Token encontrar o binário
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

BGUTIL_PORT = 4416


def get_bgutil_binary_path():
    nome_binario = "bgutil-pot.exe" if os.name == "nt" else "bgutil-pot"
    return os.path.join(ffmpeg_dir, nome_binario)


# Localiza o pacote do plugin (system-wide no Arch, local em dev/PyInstaller)
def get_plugin_path():
    system_plugin = "/usr/share/downtube/yt-dlp-plugins/bgutil-ytdlp-pot-provider"
    if os.path.isdir(system_plugin):
        return system_plugin
    return os.path.join(ffmpeg_dir, "yt-dlp-plugins", "bgutil-ytdlp-pot-provider")


try:
    _plugin_spec = importlib.util.find_spec("yt_dlp_plugins.extractor.getpot_bgutil_http")
except ModuleNotFoundError:
    _plugin_spec = None

if _plugin_spec is None:
    _plugin_path = get_plugin_path()
    if os.path.isdir(_plugin_path):
        sys.path.insert(0, _plugin_path)

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
        time.sleep(0.5)  # respiro pra ele subir antes do primeiro request
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


iniciar_bgutil_server()


# Pasta de destino: variável de ambiente > pasta localizada no sistema (PT, depois EN)
def _resolver_pasta(variavel, nomes):
    caminho = os.environ.get(variavel)
    if not caminho:
        home = os.path.expanduser("~")
        caminho = next(
            (os.path.join(home, n) for n in nomes if os.path.isdir(os.path.join(home, n))),
            os.path.join(home, nomes[-1]),
        )
    os.makedirs(caminho, exist_ok=True)
    return caminho


pastaMusica = _resolver_pasta("DOWNTUBE_MUSIC_DIR", ("Músicas", "Music"))
pastaVideo = _resolver_pasta("DOWNTUBE_VIDEO_DIR", ("Vídeos", "Videos"))


def opcoes_audio():
    return {
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


def opcoes_playlist():
    opcoes = opcoes_audio()
    opcoes["outtmpl"] = os.path.join(
        pastaMusica, "%(playlist_title)s", "%(playlist_index)02d - %(title)s.%(ext)s"
    )
    opcoes["ignoreerrors"] = True  # um vídeo indisponível não derruba a playlist
    return opcoes


def opcoes_video():
    return {
        "format": "bestvideo+bestaudio/best",
        "remote_components": ["ejs:github"],
        "ffmpeg_location": ffmpeg_dir,
        "outtmpl": os.path.join(pastaVideo, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
    }
