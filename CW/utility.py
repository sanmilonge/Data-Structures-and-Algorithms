import time

def typewriter(text, delay=0.005, end=''):
    for char in text:
        print(char, end=end, flush=True)
        time.sleep(delay)

def wait(seconds = 1):
    time.sleep(seconds)