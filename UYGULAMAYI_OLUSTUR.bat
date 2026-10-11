@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   Markdown Cevirici - uygulama olusturuluyor
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python bulunamadi. Once https://www.python.org/downloads/ adresinden
    echo Python kurun ve kurulumda "Add Python to PATH" kutusunu isaretleyin.
    pause
    exit /b 1
)

echo [1/2] Gerekli paketler kuruluyor (birkac dakika surebilir)...
python -m pip install --upgrade "markitdown[all]" pyinstaller
if errorlevel 1 goto hata

echo.
echo [2/2] Uygulama paketleniyor...
python -m PyInstaller --noconfirm --windowed --name "Markdown Cevirici" ^
    --collect-all markitdown --collect-all magika ^
    md_cevirici.py
if errorlevel 1 goto hata

echo.
echo Tamamlandi!
echo Uygulamaniz: dist\Markdown Cevirici\Markdown Cevirici.exe
echo Bu .exe icin masaustune kisayol olusturabilirsiniz.
explorer "dist\Markdown Cevirici"
pause
exit /b 0

:hata
echo.
echo Bir hata olustu. Yukaridaki mesajlari kontrol edin.
pause
exit /b 1
