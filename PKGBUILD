# Maintainer: Leandro A. Rodrigues <leandro0rodrigues@gmail.com>
pkgname=downtube
pkgver=1.0.0
pkgrel=1
pkgdesc="Simple YouTube downloader using yt-dlp"
arch=('any')
url="https://github.com/Leandro-74/DownTube"
license=('GPL3')
depends=('python' 'python-pip' 'ffmpeg' 'yt-dlp')
makedepends=('wget')
source=(
    "bgutil-pot::https://github.com/Leandro-74/DownTube/releases/download/v$pkgver/bgutil-pot"
    "ffmpeg::https://github.com/Leandro-74/DownTube/releases/download/v$pkgver/ffmpeg"
    "ffprobe::https://github.com/Leandro-74/DownTube/releases/download/v$pkgver/ffprobe"
    "qjs::https://github.com/Leandro-74/DownTube/releases/download/v$pkgver/qjs"
)
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
  cd "$startdir"

  # Instala os scripts Python
  install -dm755 "$pkgdir/usr/share/downtube/src"
  cp -r src/downtube/*.py "$pkgdir/usr/share/downtube/src/"

  # Instala o wrapper
  install -Dm755 downtube "$pkgdir/usr/bin/downtube"

  # Instala os binários (baixados do release)
  install -Dm755 "$srcdir/bgutil-pot" "$pkgdir/usr/bin/bgutil-pot"
  install -Dm755 "$srcdir/ffmpeg" "$pkgdir/usr/bin/ffmpeg"
  install -Dm755 "$srcdir/ffprobe" "$pkgdir/usr/bin/ffprobe"
  install -Dm755 "$srcdir/qjs" "$pkgdir/usr/bin/qjs"

  # Instala os plugins
  install -dm755 "$pkgdir/usr/share/downtube/yt-dlp-plugins"
  cp -r yt-dlp-plugins/bgutil-ytdlp-pot-provider "$pkgdir/usr/share/downtube/yt-dlp-plugins/"
}