# Configurações: binários, PO Token, yt-dlp e pastas de destino

import atexit
import os
import platform
import subprocess
import sys
import time
import urllib.request


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

# PATH para o yt-dlp encontrar ffmpeg, deno e bgutil-pot
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")


def _pasta_cache():
    if os.name == "nt":
        # Fora do AppData: o Python da Microsoft Store redireciona escritas pra lá,
        # e o yt-dlp executado como subprocesso não enxerga o arquivo nesse caminho
        caminho = os.path.join(os.path.expanduser("~"), ".downtube")
    else:
        base = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
        caminho = os.path.join(base, "downtube")
    os.makedirs(caminho, exist_ok=True)
    return caminho


# --- yt-dlp: binário oficial, baixado e mantido atualizado em tempo de execução ---

def _nome_ytdlp():
    if os.name == "nt":
        return "yt-dlp.exe"
    if platform.machine().lower() in ("aarch64", "arm64"):
        return "yt-dlp_linux_aarch64"
    return "yt-dlp_linux"


YTDLP = os.path.join(_pasta_cache(), _nome_ytdlp())
_CARIMBO = os.path.join(_pasta_cache(), "ytdlp-atualizado")
_INTERVALO_ATUALIZACAO = 24 * 60 * 60  # 1 dia


def _baixar_ytdlp():
    url = f"https://github.com/yt-dlp/yt-dlp/releases/latest/download/{_nome_ytdlp()}"
    print("Baixando yt-dlp (primeira execução)...")
    temporario = YTDLP + ".part"
    urllib.request.urlretrieve(url, temporario)
    os.replace(temporario, YTDLP)
    if os.name != "nt":
        os.chmod(YTDLP, 0o755)


def garantir_ytdlp():
    """Garante o binário do yt-dlp e tenta atualizá-lo uma vez por dia."""
    if not os.path.isfile(YTDLP):
        try:
            _baixar_ytdlp()
        except Exception as e:
            print(f"[erro] Não foi possível baixar o yt-dlp: {e}")
            raise SystemExit(1)
    elif not os.path.exists(_CARIMBO) or time.time() - os.path.getmtime(_CARIMBO) > _INTERVALO_ATUALIZACAO:
        # `-U` é o updater oficial; se falhar (offline), segue com a versão atual
        try:
            resultado = subprocess.run([YTDLP, "-U"], capture_output=True, text=True, timeout=120)
            if "Updated" in resultado.stdout:
                print(resultado.stdout.strip())
        except (OSError, subprocess.TimeoutExpired):
            pass

    open(_CARIMBO, "w").close()


# --- PO Token provider (bgutil-pot) ---

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


_bgutil_processo = None


# Sobe o servidor do bgutil-pot em background
def iniciar_bgutil_server():
    global _bgutil_processo

    if _bgutil_processo is not None and _bgutil_processo.poll() is None:
        return  # já está rodando

    binario = get_bgutil_binary_path()
    if not os.path.isfile(binario):
        # Não impede o app de funcionar; só fica sem PO Token
        print(f"[aviso] bgutil-pot não encontrado em {binario}, seguindo sem PO Token provider.")
        return

    try:
        _bgutil_processo = subprocess.Popen(
            # --host explícito: por padrão ele escuta só em IPv6 e o plugin usa 127.0.0.1
            [binario, "server", "--host", "127.0.0.1", "--port", str(BGUTIL_PORT)],
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
garantir_ytdlp()


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


# --- Argumentos do yt-dlp ---

def _args_base():
    args = [
        "--ffmpeg-location", ffmpeg_dir,
        "--remote-components", "ejs:github",
    ]
    # --plugin-dirs itera os filhos do diretório; o filho deve conter yt_dlp_plugins
    plugin = os.path.dirname(get_plugin_path())
    if os.path.isdir(plugin):
        args += ["--plugin-dirs", plugin]
    return args


def args_musica():
    return [
        *_args_base(),
        "-x", "--audio-format", "mp3", "--audio-quality", "192",
        "-o", os.path.join(pastaMusica, "%(title)s.%(ext)s"),
    ]


def args_playlist():
    return [
        *_args_base(),
        "-x", "--audio-format", "mp3", "--audio-quality", "192",
        "--ignore-errors",  # um vídeo indisponível não derruba a playlist
        "-o", os.path.join(
            pastaMusica, "%(playlist_title)s", "%(playlist_index)02d - %(title)s.%(ext)s"
        ),
    ]


def args_metadados():
    return [*_args_base(), "-J", "--skip-download", "--no-playlist"]


def args_video(altura):
    # Prefere mp4+m4a (merge direto); o fallback pode sair em .mkv
    return [
        *_args_base(),
        "-f", (
            f"bestvideo[height={altura}][ext=mp4]+bestaudio[ext=m4a]"
            f"/bestvideo[height={altura}]+bestaudio/best[height={altura}]"
        ),
        "--merge-output-format", "mp4",
        "--no-playlist",
        "-o", os.path.join(pastaVideo, "%(title)s.%(ext)s"),
    ]
