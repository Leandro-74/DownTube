<div align="center">

# 📥 DownTube

**Um CLI simples e rápido pra baixar vídeos, músicas e playlists do YouTube**

Construído em cima do [yt-dlp](https://github.com/yt-dlp/yt-dlp), com suporte automático a PO Token pra garantir resoluções em alta qualidade (720p, 1080p+).

[![Arch Linux](https://img.shields.io/badge/Arch%20Linux-1793D1?style=flat&logo=arch-linux&logoColor=white)](#-instalação-arch-linux)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)](#-instalação-windows)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](#)

</div>

---

## ✨ Funcionalidades

- 🎵 **Baixar música** — extrai o áudio direto em MP3 (192kbps)
- 🎬 **Baixar vídeo** — escolha a resolução, de 144p até 1080p+
- 📃 **Baixar playlist inteira** — organiza automaticamente em pastas numeradas
- 🔓 **PO Token integrado** — resolve o bloqueio do YouTube que limita downloads a 360p sem token, usando o [bgutil-pot](https://github.com/jim60105/bgutil-ytdlp-pot-provider-rs) rodando localmente em background
- 🗂️ Detecta automaticamente as pastas de Música/Vídeos do seu usuário (PT-BR ou EN-US)

---

## 🐧 Instalação (Arch Linux)

Via `makepkg`, clonando o `PKGBUILD` deste repositório:

```bash
git clone https://github.com/Leandro-74/DownTube.git
cd DownTube
makepkg -si
```

Isso instala automaticamente as dependências necessárias (`python`, `yt-dlp`, `ffmpeg`, `deno`) e o binário do PO Token provider. Depois disso, rode de qualquer lugar do sistema:

```bash
downtube
```

### Dependências instaladas automaticamente

| Pacote | Pra quê serve |
|---|---|
| `yt-dlp` | Motor de download/extração |
| `ffmpeg` | Conversão de áudio/mux de vídeo |
| `deno` | Resolve os desafios de JavaScript do YouTube |
| `bgutil-pot` *(embutido)* | Gera o PO Token pra liberar resoluções altas |

> **Dica:** instale também o pacote opcional `yt-dlp-ejs` para evitar que o `deno` precise baixar o solucionador de desafios JS na primeira execução.

---

## 🪟 Instalação (Windows)

1. Vá até a aba [**Releases**](../../releases) deste repositório
2. Baixe o `downtube.exe` mais recente
3. Execute — na primeira vez, o Windows Defender/SmartScreen pode avisar que é "aplicativo desconhecido". Clique em **Mais informações → Executar assim mesmo** (é normal para executáveis sem certificado de assinatura pago)

O `.exe` já vem com tudo embutido (`ffmpeg`, `bgutil-pot`, plugin de PO Token) — não precisa instalar nada além dele.

---

## 🛠️ Rodando a partir do código-fonte (desenvolvimento)

```bash
git clone https://github.com/Leandro-74/DownTube.git
cd DownTube/src/downtube
pip install -r ../../requirements.txt
python3 main.py
```

Pra ter resoluções acima de 360p em modo dev, você também precisa do binário `bgutil-pot` e da pasta `yt-dlp-plugins/` na mesma pasta do `config.py` — veja a seção de PO Token abaixo.

### Sobre o PO Token

Desde 2024/2025 o YouTube passou a exigir um **PO Token** pra liberar formatos de vídeo acima de 360p. O DownTube resolve isso automaticamente subindo um servidor local ([bgutil-pot](https://github.com/jim60105/bgutil-ytdlp-pot-provider-rs)) em background — você não precisa fazer nada manualmente, contanto que o binário e o plugin estejam nos lugares certos (o instalador via `makepkg`/`.exe` já cuida disso sozinho).

---

## 📦 Compilando você mesmo

- **Arch/AUR:** o `PKGBUILD` na raiz do repositório já faz tudo — veja a seção [Instalação (Arch Linux)](#-instalação-arch-linux).
- **Windows:** o build é automatizado via GitHub Actions (`.github/workflows/build-windows.yml`) — toda tag `v*` gera um `.exe` novo automaticamente, anexado à Release correspondente.

---

## 🤝 Contribuindo

Issues e PRs são bem-vindos! Se encontrar algum bug (especialmente relacionado a resoluções/PO Token, que é a parte mais sensível do projeto), abra uma issue com o output do comando em modo verbose:

```bash
yt-dlp -v "URL_DO_VIDEO" 2>&1 | grep -i "pot"
```

---

## 📄 Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

Feito por [Leandro A. Rodrigues](https://github.com/Leandro-74)

</div>
