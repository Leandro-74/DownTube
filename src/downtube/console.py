# console.py — redimensiona e centraliza a janela do terminal (Windows)

import os
import time

if os.name == "nt":
    import ctypes
    import ctypes.wintypes

TITULO = "DownTube"


# Descobre a janela VISÍVEL do terminal (WT ou conhost) pelo título do console
def _hwnd_da_janela() -> int:
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    kernel32.SetConsoleTitleW(TITULO)
    time.sleep(0.25)  # o WT atualiza o título em async
    hwnd = user32.FindWindowW(None, TITULO)
    return hwnd or kernel32.GetConsoleWindow()  # fallback: conhost clássico


# Redimensiona em pixels (pela grade atual) e centraliza a janela do console
def ajustar_janela(cols: int = 78, lines: int = 20) -> None:
    if os.name != "nt":
        return
    try:
        grid = os.get_terminal_size()
    except OSError:
        return  # saída redirecionada (pipe/arquivo): não há janela pra ajustar

    try:
        user32 = ctypes.windll.user32
        hwnd = _hwnd_da_janela()
        if not hwnd:
            return
        if user32.IsZoomed(hwnd):
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            time.sleep(0.15)

        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        largura = rect.right - rect.left
        altura = rect.bottom - rect.top
        celula_w = largura / max(1, grid.columns)  # px por caractere, na janela real
        celula_h = altura / max(1, grid.lines)
        nova_largura = int(cols * celula_w)
        nova_altura = int(lines * celula_h)

        x = (user32.GetSystemMetrics(0) - nova_largura) // 2
        y = (user32.GetSystemMetrics(1) - nova_altura) // 2
        user32.MoveWindow(hwnd, x, y, nova_largura, nova_altura, True)
    except Exception:
        pass
