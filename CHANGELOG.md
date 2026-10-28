# Changelog

Todas as mudanças relevantes do DownTube. O projeto usa versionamento semântico.

## [1.1.1] - 2026-10-28

### Adicionado

- Interface em caixas Unicode centralizadas, com o prompt dentro da caixa e avisos de opção inválida que não somem mais ao redesenhar a tela
- Janela do terminal redimensionada para 78×20 e centralizada na tela (Windows)

### Alterado

- CLI reorganizado em `menu.py` (apresentação), `cli.py` (ações e loop principal), `console.py` (janela) e `main.py` (entry point)
- Saída redirecionada (pipe/arquivo) passa a usar UTF-8, evitando erro com os caracteres da caixa

### Removido

- `downloaders.py`, substituído por `cli.py`

## [1.1.0] - 2026-10-28

### Adicionado

- yt-dlp é baixado na primeira execução e atualizado sozinho uma vez por dia (`-U`), sem depender de uma nova versão do DownTube
- PKGBUILD para instalar no Arch Linux via `makepkg`, com launcher `downtube` em `/usr/bin`
- Workflow que compila o `.exe` no Windows e o anexa automaticamente na release
- README completo, licença MIT e ícone do executável

### Alterado

- O yt-dlp deixa de ser biblioteca embutida e passa a ser o binário oficial (executável de 150,7 MB para 139,5 MB)
- Projeto sem dependências Python (`requirements.txt` removido)
- PKGBUILD não depende mais do pacote `yt-dlp`

### Corrigido

- Erro HTTP 403 em downloads (`--plugin-dirs` apontava para o diretório errado e o PO Token não era carregado)
- Build do CI quebrando com o gyan.dev fora do ar (mirror alternativo do ffmpeg)
- Release não publicada por falta de permissão de escrita no token do Actions

## [1.0.0] - 2026-07-05

### Adicionado

- Download de músicas em MP3 e de vídeos com escolha de resolução
- Download de playlists inteiras, organizadas em pastas numeradas
- PO Token próprio via bgutil-pot, liberando resoluções acima de 360p
