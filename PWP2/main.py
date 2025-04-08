import time, pydirectinput, winsound
import tkinter as tk
from threading import Thread, Event
from tkinter import messagebox


DELAY_BETWEEN_ACTIONS = 1.5
stop_event = Event()
timer_after_id = None

# --- Funções auxiliares ---

def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

def wait_with_countdown(total_seconds):
    for remaining in range(total_seconds, 0, -1):
        if stop_event.is_set():
            break
        if remaining == 25:
            winsound.Beep(1000, 500)  # Frequência: 1000 Hz, Duração: 500 ms
        mins, secs = divmod(remaining, 60)
        timer_label.config(text=f"Reinício em {mins:02}:{secs:02}")
        time.sleep(1)
    timer_label.config(text="")

def action_with_delay(action, args=None, kwargs=None):
    args = args or []
    kwargs = kwargs or {}
    action(*args, **kwargs)
    time.sleep(DELAY_BETWEEN_ACTIONS)

def automation():
    try:
        while not stop_event.is_set():
            log('Iniciando...')

            if stop_event.is_set():
                break

            steps = [
                (pydirectinput.press, ["space"]),
                (pydirectinput.press, ["d"]),
                (pydirectinput.press, ["d"]),
                (pydirectinput.press, ["space"]),
                (pydirectinput.press, ["s"]),
                (pydirectinput.press, ["space"]),
                (time.sleep, [3]),
                (pydirectinput.press, ["s"]),
                (pydirectinput.press, ["space"]),
                (pydirectinput.click, [1161, 578]),
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

            for step in steps:
                if stop_event.is_set():
                    break
                action_with_delay(step[0], step[1] if len(step) > 1 else [], step[2] if len(step) > 2 else {})

            if stop_event.is_set():
                break

            log('Ações finalizadas, esperando o timer para reiniciar...')
            wait_with_countdown(1990)

    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        stop_event.clear()
        timer_label.config(text="")
        log("Automação finalizada!")

def start_automation():
    def countdown(seconds):
        global timer_after_id
        if seconds > 0 and not stop_event.is_set():
            timer_label.config(text=f"Iniciando em {seconds}...")
            timer_after_id = app_window.after(1000, countdown, seconds - 1)
        else:
            timer_label.config(text="")
            thread = Thread(target=automation, daemon=True)
            thread.start()

    stop_event.clear()
    countdown(3)

def stop_automation():
    global timer_after_id
    stop_event.set()
    if timer_after_id:
        app_window.after_cancel(timer_after_id)
        timer_after_id = None
    timer_label.config(text="")
    messagebox.showinfo("Status", "Automação cancelada!")

# --- Interface gráfica ---

app_window = tk.Tk()
app_window.title("EDPWPA")
app_window.geometry("550x420")
app_window.resizable(False, False)
app_window.configure(bg="#1e1e1e")

# Frame principal
app_frame = tk.Frame(app_window, padx=20, pady=20, bg="#1e1e1e")
app_frame.place(relx=0.5, rely=0.5, anchor="center")

# Título
title_main = tk.Label(app_frame, text="EDPWPA", font=("Arial Black", 22), fg="#00ffcc", bg="#1e1e1e")
title_main.pack()

title_sub = tk.Label(app_frame, text="Elite Dangerous Power Play Automation", font=("Arial", 10), fg="white", bg="#1e1e1e")
title_sub.pack(pady=(0, 15))

# Botões
btn_frame = tk.Frame(app_frame, bg="#1e1e1e")
btn_frame.pack(pady=10)

btn_style = {"font": ("Arial", 10, "bold"), "bg": "#333", "fg": "#00ffcc", "activebackground": "#555", "activeforeground": "white"}

btn_start = tk.Button(btn_frame, text="Iniciar automação", command=start_automation, **btn_style)
btn_start.pack(side="left", padx=10)

btn_stop = tk.Button(btn_frame, text="Cancelar automação", command=stop_automation, **btn_style)
btn_stop.pack(side="right", padx=10)

# Timer visível
timer_label = tk.Label(app_frame, text="", font=("Arial", 12), fg="#00ffcc", bg="#1e1e1e")
timer_label.pack(pady=10)

# Campo de log
log_box = tk.Text(app_frame, height=10, width=60, wrap="word", bg="#121212", fg="#00ffcc", insertbackground="white")
log_box.pack(pady=10)

app_window.mainloop()
