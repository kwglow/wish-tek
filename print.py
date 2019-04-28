import yaml
from random import randint
from time import sleep
import subprocess

DEVICE='printout.txt'

WIDTH = 80
MARGIN = 5
COLUMN_OFFSETS = [15, 30, 50, 70]
PHRASE_DISTANCE = 30
LPM = 10

DEVICE_NAME = 'okidata'

def printlines(lines):
    command = chr(27) + chr(107) + 'n' + line
    command += lines
    # ESC } NUL (I-Prime command)
    command += chr(27) + chr(125) + chr(0)
    
    print_cmd = ['lp', '-d', DEVICE_NAME, '-o', 'raw']
    #cmd = ['echo']
    proc = subprocess.Popen(print_cmd, stdin=subprocess.PIPE )
    proc.stdin.write(line.encode('ASCII'))
    proc.communicate()
    proc.wait()


with open('phrases.yaml', 'r') as f:
    phrases = yaml.safe_load(f.read())

def get_binary_char():
    digits = ['0', '1', ' ']
    return digits[randint(0, len(digits) - 1)]

row = 0
while True:
    line = ''
    for i in range(0, WIDTH):
        if i in COLUMN_OFFSETS:
            line += get_binary_char()
        else:
            line += ' '

    start = MARGIN
    end = WIDTH - MARGIN
    COLUMN_OFFSETS
    if row % PHRASE_DISTANCE == 0:
        phrase = phrases[randint(0, len(phrases) - 1)]
        left_align = row % (2 * PHRASE_DISTANCE) == 0
        if left_align:
            end = MARGIN + len(phrase)
        else:
            start = 80 - MARGIN - len(phrase)

        line = line[:start] + phrase + line[end:]

    printline(line)
    row += 1
    sleep(60 / LPM)
