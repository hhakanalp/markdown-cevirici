#!/bin/bash
# Markdown Çevirici - macOS uygulaması oluşturur
cd "$(dirname "$0")"
echo "============================================"
echo "  Markdown Çevirici - uygulama oluşturuluyor"
echo "============================================"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python bulunamadı. https://www.python.org/downloads/macos/ adresinden kurun."
  read -p "Kapatmak için Enter'a basın..." ; exit 1
fi
if ! python3 -c "import tkinter" 2>/dev/null; then
  echo "Python'unuzda tkinter yok."
  echo "python.org'dan Python kurun ya da Homebrew kullanıyorsanız: brew install python-tk"
  read -p "Kapatmak için Enter'a basın..." ; exit 1
fi

set -e
echo "[1/2] Gerekli paketler kuruluyor (birkaç dakika sürebilir)..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip >/dev/null
pip install "markitdown[all]" pyinstaller

echo "[2/2] Uygulama paketleniyor..."
python -m PyInstaller --noconfirm --windowed --name "Markdown Cevirici" \
  --collect-all markitdown --collect-all magika md_cevirici.py

echo
echo "Tamamlandı! Uygulamanız: dist/Markdown Cevirici.app"
echo "Bunu Uygulamalar (Applications) klasörüne sürükleyebilirsiniz."
open dist
read -p "Kapatmak için Enter'a basın..."
