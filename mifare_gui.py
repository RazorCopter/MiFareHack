import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess
import threading
import os
import shutil
import signal

running_process = None  # Traccia processo attivo

ICON_DIR = os.path.join(os.path.dirname(__file__), "icons")

def run_command(cmd):
    global running_process
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"🚀 Eseguo: {cmd}\n\n")
    output_box.see(tk.END)

    def worker():
        global running_process
        running_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        pid = running_process.pid
        try:
            for line in iter(running_process.stdout.readline, ''):
                if running_process.poll() is not None:
                    break
                output_box.insert(tk.END, line)
                output_box.see(tk.END)
        except Exception as e:
            output_box.insert(tk.END, f"\n⚠️ Errore lettura output: {e}\n")
        finally:
            if running_process:
                running_process.stdout.close()
                returncode = running_process.wait()
                if returncode == -9:
                    output_box.insert(tk.END, "\n☠️ Ucciso con SIGKILL.\n")
                else:
                    output_box.insert(tk.END, f"\n✅ Completato. Exit code: {returncode}\n")
                output_box.see(tk.END)
            running_process = None

    threading.Thread(target=worker, daemon=True).start()




def stop_process():
    global running_process
    if running_process and running_process.poll() is None:
        pid = running_process.pid
        output_box.insert(tk.END, f"\n🔴 Killo brutalmente il processo su PID {pid}...\n\n")
        output_box.see(tk.END)
        try:
            os.kill(pid, signal.SIGKILL)
            output_box.insert(tk.END, "☠️ ☠️   Processo terminato   ☠️ ☠️ \n\n")
        except Exception as e:
            output_box.insert(tk.END, f"⚠️ Errore durante kill: {e}\n")
        running_process = None
    else:
        messagebox.showinfo("Nessun processo", "Nessun processo in esecuzione.")

def run_mfoc_hardnested():
    dumpfile = simpledialog.askstring("Dump File (-O)", "Inserisci il nome del file dump (es. mycard.mfd):")
    probes = simpledialog.askstring("Probes (-P)", "Numero di probes per settore (default = 20):")
    tolerance = simpledialog.askstring("Nonce Tolerance (-T)", "Valore tolerance (default = 20):")
    key = simpledialog.askstring("Chiave esadecimale (-k)", "Chiave singola da testare (es. ffffffffffff):")
    keyfile = simpledialog.askstring("File chiavi (-f)", "Percorso file di chiavi (opzionale):")

    if not dumpfile and not probes and not tolerance and not key and not keyfile:
        cmd = "mfoc-hardnested -O test.mfd"
    else:
        cmd = "mfoc-hardnested"
        if probes:
            cmd += f" -P {probes}"
        if tolerance:
            cmd += f" -T {tolerance}"
        if key:
            cmd += f" -k {key}"
        if keyfile:
            cmd += f" -f {keyfile}"
        cmd += f" -O {dumpfile if dumpfile else 'test.mfd'}"

    run_command(cmd)

def run_mfoc():
    dumpfile = simpledialog.askstring("Dump File", "Inserisci nome del file dump:")
    probes = simpledialog.askinteger("Probes", "Numero di probes (0 = ignora):", initialvalue=0)
    cmd = f"mfoc {'-P ' + str(probes) if probes and probes > 0 else ''} -O {dumpfile}"
    run_command(cmd)

def run_mfcuk():
    dumpfile = simpledialog.askstring("Dump File", "Inserisci nome del file dump:")
    cmd = f"mfcuk -C -v 3 -R 0:A -s 250 -S 250 -O {dumpfile}"
    run_command(cmd)

def run_mikai():
    output_box.insert(tk.END, "🧠 Avvio Mikai GUI...\n")
    output_box.see(tk.END)

    terminal = shutil.which("gnome-terminal") or shutil.which("xfce4-terminal") or shutil.which("xterm")
    if not terminal:
        messagebox.showerror("Errore", "Nessun terminale compatibile trovato!")
        return

    process = subprocess.Popen([terminal, "--", "mikai"])

    def monitor():
        process.wait()
        output_box.insert(tk.END, "✅ Mikai è stato chiuso.\n")
        output_box.see(tk.END)

    threading.Thread(target=monitor, daemon=True).start()

# GUI setup
root = tk.Tk()
root.title("🎴 MIFARE Clone Tool - Gianvito Edition")
root.geometry("1500x1000")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("Bold.TButton", font=("Segoe UI", 10, "bold"))

def create_button(parent, icon_file, text, command):
    image = Image.open(os.path.join(ICON_DIR, icon_file)).resize((40, 40), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    btn = ttk.Button(parent, text=f"  {text}", image=photo, compound="left", command=command)
    btn.image = photo  # per non perdere il riferimento all'immagine
    btn.configure(style="Bold.TButton")  # stile personalizzato
    return btn


# Header
header = tk.Frame(root, bg="#e0e0e0", pady=10)
header.pack(fill=tk.X)

logo_path = os.path.join(ICON_DIR, "logo.png")
if os.path.exists(logo_path):
    logo_img = ImageTk.PhotoImage(Image.open(logo_path).resize((40, 40), Image.Resampling.LANCZOS))
    tk.Label(header, image=logo_img, bg="#e0e0e0").pack(side=tk.LEFT, padx=10)
tk.Label(header, text="MIFARE Hack Tool", bg="#e0e0e0", font=("Segoe UI", 20)).pack(side=tk.LEFT)

# Pulsanti
button_frame = tk.Frame(root, bg="#baff8d", pady=15)
button_frame.pack()

create_button(button_frame, "mfoc.png", "MFOC - Brute Force", run_mfoc).grid(row=0, column=0, padx=20, pady=10)
create_button(button_frame, "mfcuk.png", "MFCUK - Nested", run_mfcuk).grid(row=0, column=1, padx=20, pady=10)
create_button(button_frame, "mikai.png", "MIKAI - GUI", run_mikai).grid(row=0, column=2, padx=20, pady=10)
create_button(button_frame, "mfoc.png", "MFOC - Hardnested", run_mfoc_hardnested).grid(row=0, column=3, padx=20, pady=10)


# Pulsante Interrompi
tk.Button(root, text="🔴 Interrompi esecuzione", command=stop_process,
          bg="#e7c523", fg="white", font=("Segoe UI", 13, "bold")).pack(pady=5)

# Output
output_box = scrolledtext.ScrolledText(root, width=120, height=35, font=("Courier New", 10), bg="#ffffff")
output_box.pack(padx=15, pady=15)

root.mainloop()

