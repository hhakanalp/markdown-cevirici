; Markdown Çevirici - Windows kurulum sihirbazı (Inno Setup 6)

#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppId={{6E2B1F7A-3C4D-4E8B-9A51-2F0D7C8E4B13}
AppName=Markdown Çevirici
AppVersion={#AppVersion}
AppPublisher=Hamit Hakan Alp
DefaultDirName={autopf}\Markdown Cevirici
DefaultGroupName=Markdown Çevirici
UninstallDisplayName=Markdown Çevirici
UninstallDisplayIcon={app}\Markdown Cevirici.exe
OutputDir=Output
OutputBaseFilename=Markdown-Cevirici-Kurulum
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "Masaüstüne kısayol oluştur"; GroupDescription: "Ek simgeler:"

[Files]
Source: "dist\Markdown Cevirici\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Markdown Çevirici"; Filename: "{app}\Markdown Cevirici.exe"
Name: "{group}\Markdown Çevirici'yi kaldır"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Markdown Çevirici"; Filename: "{app}\Markdown Cevirici.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Markdown Cevirici.exe"; Description: "Markdown Çevirici'yi şimdi başlat"; Flags: nowait postinstall skipifsilent
