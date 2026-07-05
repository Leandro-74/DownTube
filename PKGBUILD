# Maintainer: Leandro A. Rodrigues <leandro0rodriguea@gmail.com>
pkgname=downtube
pkgver=1.0.0
pkgrel=1
pkgdesc="Simple YouTube downloader using yt-dlp"
arch=('any')
url="https://github.com/Leandro-74/DownTube"
license=('GPL3')
depends=('python' 'python-pip' 'ffmpeg' 'yt-dlp')
makedepends=()
source=("$pkgname-$pkgver.tar.gz::https://github.com/Leandro-74/DownTube/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
  cd "$srcdir/$pkgname-$pkgver"

  # 1. Instala os scripts Python em /usr/share/downtube
  install -dm755 "$pkgdir/usr/share/downtube/src"
  cp -r src/downtube/*.py "$pkgdir/usr/share/downtube/src/"

  # 2. Instala o wrapper executável
  install -Dm755 downtube "$pkgdir/usr/bin/downtube"

  # 3. Instala os binários auxiliares
  install -Dm755 bin/bgutil-pot "$pkgdir/usr/bin/bgutil-pot"
  install -Dm755 bin/ffmpeg "$pkgdir/usr/bin/ffmpeg"
  install -Dm755 bin/ffprobe "$pkgdir/usr/bin/ffprobe"
  install -Dm755 bin/qjs "$pkgdir/usr/bin/qjs"

  # 4. Instala os plugins do yt-dlp
  install -dm755 "$pkgdir/usr/share/downtube/yt-dlp-plugins"
  cp -r yt-dlp-plugins/bgutil-ytdlp-pot-provider "$pkgdir/usr/share/downtube/yt-dlp-plugins/"
}