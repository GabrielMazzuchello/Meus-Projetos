import time
import winsound
import pyautogui
import pydirectinput
import tkinter as tk
from tkinter import messagebox
from threading import Thread, Event

# pyinstaller --onefile --noconsole --icon=eclipse.ico main.py

DELAY_BETWEEN_ACTIONS = 1.6
stop_event = Event()
timer_after_id = None

# --- Funções principais ---
def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    app_window.update_idletasks()

def wait_with_countdown(total_seconds, is_image_check=False):
    for remaining in range(total_seconds, 0, -1):
        if stop_event.is_set():
            break
        if not is_image_check and remaining == 25:
            winsound.Beep(1000, 500)
        mins, secs = divmod(remaining, 60)
        timer_text = f"Verificação: {mins:02}:{secs:02}" if is_image_check else f"Reinício em {mins:02}:{secs:02}"
        timer_label.config(text=timer_text)
        time.sleep(1)
    timer_label.config(text="")

def check_image_and_wait():
    """Verifica continuamente a imagem até que não seja mais encontrada."""
    while not stop_event.is_set():
        try:
            pos = pyautogui.locateOnScreen('unavailable.png', confidence=0.8)
            if pos:
                log("Material indisponível. Aguardando...")
                action_wrapper(pydirectinput.press, ["backspace"])
                wait_with_countdown(60, is_image_check=True)
                action_wrapper(pydirectinput.press, ["space"])
                action_wrapper(pydirectinput.press, ["s"])
                action_wrapper(pydirectinput.press, ["space"])
            else:
                log("Material disponível - prosseguindo.")
                return True
        except pyautogui.ImageNotFoundException:
            log("Imagem não encontrada - continuando.")
            return True
        except Exception as e:
            log(f"Erro na verificação: {str(e)}")
            return False
        time.sleep(5)

def action_wrapper(action, args=None):
    args = args or []
    action(*args)
    time.sleep(DELAY_BETWEEN_ACTIONS)

def automation_cycle():
    """Loop principal de automação usando apenas teclado"""
    while not stop_event.is_set():
        try:
            log('Iniciando novo ciclo...')
            
            # Lista de ações atualizada sem clique do mouse
            steps = [
                (pydirectinput.press, ["space"]),
                (pydirectinput.press, ["d"]),
                (pydirectinput.press, ["d"]),
                (pydirectinput.press, ["space"]),
                (pydirectinput.press, ["s"]),
                (pydirectinput.press, ["space"]),
                (time.sleep, [1]),
                (pydirectinput.press, ["s"]),
                (pydirectinput.press, ["space"]),
                (check_image_and_wait, []),
                # Substituição do clique por comandos de teclado
                (pydirectinput.press, ["d"]),
                (pydirectinput.press, ["s"]),
                (pydirectinput.press, ["s"]),
                (pydirectinput.press, ["space"]),
                (pydirectinput.press, ["s"]),
                (pydirectinput.keyDown, ["d"]),
                (time.sleep, [1]),
                (pydirectinput.keyUp, ["d"]),
                (pydirectinput.press, ["s"]),
                (pydirectinput.press, ["space"]),
                (pydirectinput.press, ["backspace"]),
                (pydirectinput.press, ["backspace"]),
                (pydirectinput.press, ["backspace"]),
            ]

            for action, args in steps:
                if stop_event.is_set():
                    return
                if callable(action):
                    if args:
                        action(*args)
                    else:
                        action()
                    time.sleep(DELAY_BETWEEN_ACTIONS)

            log('Ciclo completo. Aguardando 30 minutos...')
            wait_with_countdown(1800)

        except Exception as e:
            log(f"Erro crítico: {str(e)}")
            messagebox.showerror("Erro", str(e))
            stop_automation()

# --- Controle da automação ---
def start_automation():
    def countdown(seconds):
        global timer_after_id
        if seconds > 0 and not stop_event.is_set():
            timer_label.config(text=f"Iniciando em {seconds}...")
            timer_after_id = app_window.after(1000, countdown, seconds - 1)
        else:
            timer_label.config(text="")
            automation_thread = Thread(target=automation_cycle, daemon=True)
            automation_thread.start()

    stop_event.clear()
    countdown(3)

def stop_automation():
    global timer_after_id
    stop_event.set()
    if timer_after_id:
        app_window.after_cancel(timer_after_id)
        timer_after_id = None
    timer_label.config(text="")
    log("Automação interrompida pelo usuário")

# --- Interface gráfica ---
app_window = tk.Tk()
app_window.title("EDPWPA")
app_window.geometry("550x420")
app_window.resizable(False, False)
app_window.configure(bg="#1e1e1e")

# Componentes da interface
main_frame = tk.Frame(app_window, padx=20, pady=20, bg="#1e1e1e")
main_frame.pack(expand=True, fill='both')

title_label = tk.Label(main_frame, 
                       text="EDPWPA\nElite Dangerous Power Play Automation",
                       font=("Arial", 12, "bold"),
                       fg="#00ffcc",
                       bg="#1e1e1e")
title_label.pack(pady=10)

control_frame = tk.Frame(main_frame, bg="#1e1e1e")
control_frame.pack(pady=10)

btn_style = {
    'font': ('Arial', 10, 'bold'),
    'bg': '#333',
    'fg': '#00ffcc',
    'activebackground': '#555',
    'padx': 15,
    'pady': 5
}

start_btn = tk.Button(control_frame, 
                      text="Iniciar", 
                      command=start_automation,
                      **btn_style)
start_btn.pack(side='left', padx=10)

stop_btn = tk.Button(control_frame, 
                     text="Parar", 
                     command=stop_automation,
                     **btn_style)
stop_btn.pack(side='right', padx=10)

timer_label = tk.Label(main_frame, 
                       text="",
                       font=('Arial', 10),
                       fg='#00ffcc',
                       bg='#1e1e1e')
timer_label.pack(pady=5)

log_box = tk.Text(main_frame,
                  height=10,
                  width=60,
                  wrap='word',
                  bg='#121212',
                  fg='#00ffcc',
                  insertbackground='white')
log_box.pack(pady=10, fill='both')

app_window.mainloop()