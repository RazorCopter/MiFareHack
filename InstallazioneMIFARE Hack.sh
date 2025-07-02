#!/bin/bash

set -e

# Funzione per stampare intestazioni carine
print_step() {
  echo -e "\n=============================="
  echo -e "🔧 $1"
  echo -e "=============================="
}

print_step "Aggiornamento del sistema"
sudo apt update && sudo apt full-upgrade -y

print_step "Installazione dipendenze di sistema (NFC, dev, Python, Git...)"
sudo apt install -y \
  pcscd pcsc-tools libpcsclite-dev \
  libnfc-bin libnfc-dev \
  mfoc mfcuk \
  git autoconf libtool \
  libusb-dev libreadline-dev \
  python3 python3-pip python3-tk \
  build-essential cmake unzip wget

print_step "Installazione librerie Python"
pip3 install --break-system-packages pillow

print_step "Abilitazione e avvio del servizio pcscd"
sudo systemctl enable pcscd
sudo systemctl start pcscd

print_step "Configurazione libnfc per ACR122U"
mkdir -p ~/.config/libnfc
cat <<EOF > ~/.config/libnfc/libnfc.conf
device.name = "ACR122U"
device.connstring = "pn532_usb:libusb"
EOF

print_step "Verifica presenza lettore NFC"
nfc-list || echo "⚠️ Lettore non rilevato. Assicurati che sia collegato."

print_step "Clonazione del tuo repository MIFARE GUI"
cd ~/Scrivania || cd ~/Desktop || mkdir -p ~/Scrivania && cd ~/Scrivania
git clone https://github.com/RazorCopter/MiFareHack.git mifare_gui

print_step "Installazione di Mikai"
cd ~/Scrivania/mifare_gui
if [ ! -f mikai.AppImage ]; then
  echo "⬇️ Scaricamento Mikai (AppImage)..."
  wget -O mikai.AppImage "https://github.com/Lilz073/mikai/releases/latest/download/Mikai_4.1.0-X86_64.AppImage" || echo "⚠️ Fallito, scaricalo manualmente."
  chmod +x mikai.AppImage
fi

print_step "Compilazione di mfoc-hardnested"
cd ~/Scrivania/mifare_gui
if [ ! -d mfoc-hardnested ]; then
  echo "📦 Clonazione di mfoc-hardnested..."
  git clone https://github.com/nfc-tools/mfoc-hardnested.git
fi
cd mfoc-hardnested
make clean && make
sudo make install

print_step "Creazione collegamento sul desktop"
cat <<EOF > ~/Scrivania/MIFARE-Tool.desktop
[Desktop Entry]
Name=MIFARE Hack Tool
Comment=Interfaccia grafica per clonazione MIFARE con mfoc, mfcuk e Mikai
Exec=python3 /home/$USER/Scrivania/mifare_gui/mifare_gui.py
Icon=/home/$USER/Scrivania/mifare_gui/icons/logo.png
Terminal=false
Type=Application
Categories=Utility;Security;
EOF
chmod +x ~/Scrivania/MIFARE-Tool.desktop

print_step "Fatto!"
echo "✅ Tutto pronto! Puoi lanciare l'app GUI dalla tua Scrivania!"
echo "   Oppure da terminale: python3 ~/Scrivania/mifare_gui/mifare_gui.p
