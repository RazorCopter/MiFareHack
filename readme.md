# 🎴 MIFARE Hack Tool - GUI Edition

**Interfaccia grafica avanzata per la clonazione e l'analisi di carte MIFARE Classic 1K**, realizzata con Python + Tkinter e supporto ai tool più noti: `mfoc`, `mfcuk`, `mfoc-hardnested`, `mikai`.

---

## ✨ Funzionalità principali

- ✅ Avvio di attacchi MFOC (brute-force)
- ✅ Avvio di attacchi MFCUK (nested)
- ✅ Integrazione con `mfoc-hardnested`
- ✅ Avvio della GUI Mikai direttamente da interfaccia
- ✅ Output terminale in tempo reale
- ✅ Pulsante per terminare il processo NFC in esecuzione
- ✅ Grafica migliorata: icone, font Windows-style, bottoni eleganti

---

## 📸 Screenshot

> *(Da aggiungere! Inserisci qui eventuali immagini della GUI in uso)*

---

## ⚙️ Requisiti

- Linux (Ubuntu/Debian-based consigliato)
- Lettore NFC compatibile, es. **ACR122U**
- Python 3.x
- Tool NFC:
  - `mfoc`, `mfcuk`, `mfoc-hardnested`, `libnfc`, `pcscd`
- GUI: `python3-tk`, `pillow`

---

## 🧪 Modalità di installazione

### 🔧 Metodo 1 — Script automatico `.sh`

1. Scarica lo script di installazione:
   ```bash
   wget https://raw.githubusercontent.com/RazorCopter/MiFareHack/main/InstallazioneMIFARE%20Hack.sh
   chmod +x InstallazioneMIFARE\ Hack.sh
   ./InstallazioneMIFARE\ Hack.sh

