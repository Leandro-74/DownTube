# Maintainer: Leandro A. Rodrigues <SEU_EMAIL_AQUI>
pkgname=downtube
pkgver=1.1.0
pkgrel=1
pkgdesc="TUI para baixar vídeos, músicas e playlists do YouTube via yt-dlp"
arch=('x86_64')
url="https://github.com/Leandro-74/DownTube"
license=('MIT')
depends=('python' 'yt-dlp' 'ffmpeg' 'deno')
optdepends=('yt-dlp-ejs: evita a necessidade de baixar o solucionador de desafios JS em tempo de execucao')
makedepends=('git' 'unzip')
source=(
  "$pkgname-$pkgver.tar.gz::https://github.com/Leandro-74/DownTube/archive/refs/tags/v$pkgver.tar.gz"
  "bgutil-pot-linux-x86_64::https://github.com/jim60105/bgutil-ytdlp-pot-provider-rs/releases/download/v0.8.1/bgutil-pot-linux-x86_64"
  "bgutil-plugin.zip::https://github.com/jim60105/bgutil-ytdlp-pot-provider-rs/releases/latest/download/bgutil-ytdlp-pot-provider-rs.zip"
)
sha256sums=('SKIP' 'SKIP' 'SKIP')

package() {
  cd "$srcdir/DownTube-$pkgver"

  # Codigo-fonte principal (so os .py de verdade, nada de binarios/backup/__pycache__)
  install -d "$pkgdir/usr/lib/downtube"
  install -Dm644 src/downtube/main.py        "$pkgdir/usr/lib/downtube/main.py"
  install -Dm644 src/downtube/config.py      "$pkgdir/usr/lib/downtube/config.py"
  install -Dm644 src/downtube/downloaders.py "$pkgdir/usr/lib/downtube/downloaders.py"

  # Binario do PO Token provider - fica em /usr/bin, igual o config.py ja espera
  install -Dm755 "$srcdir/bgutil-pot-linux-x86_64" "$pkgdir/usr/bin/bgutil-pot"

  # Plugin do yt-dlp - fica em /usr/share/downtube, igual o config.py ja espera
  install -d "$pkgdir/usr/share/downtube/yt-dlp-plugins/bgutil-ytdlp-pot-provider"
  bsdtar -xf "$srcdir/bgutil-plugin.zip" -C "$pkgdir/usr/share/downtube/yt-dlp-plugins/bgutil-ytdlp-pot-provider"

  # Launcher - versionado na raiz do repositorio (arquivo "downtube")
  install -Dm755 downtube "$pkgdir/usr/bin/downtube"

  if [ -f LICENSE ]; then
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  fi
}
