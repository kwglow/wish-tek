import yaml
from random import randint
from time import sleep
import subprocess

DEVICE='printout.txt'

WIDTH = 80
MARGIN = 5
COLUMN_OFFSETS = [15, 30, 50, 70]
PHRASE_DISTANCE = 30
LPM = 60

DEVICE_NAME = 'okidata'

def printlines(lines):
    #Half speed
    command = chr(27) + chr(115) + chr(49)
    #NLQ
    command = chr(27) + chr(120) + chr(49)

    command += lines
    
    # ESC } NUL (I-Prime command)
    command += chr(27) + chr(125) + chr(0)
    
    print_cmd = ['lp', '-d', DEVICE_NAME, '-o', 'raw']
    #cmd = ['echo']
    proc = subprocess.Popen(print_cmd, stdin=subprocess.PIPE )
    proc.stdin.write(lines.encode('ASCII'))
    proc.communicate()
    proc.wait()


with open('phrases.yaml', 'r') as f:
    phrases = yaml.safe_load(f.read())

def get_binary_char():
    digits = ['0', '1', ' ']
    return digits[randint(0, len(digits) - 1)]

row = 0
phrase = None
left_align = True
start = 0
end = 0
lines = ''
while True:
    line = ''
    for i in range(0, WIDTH):
        if i in COLUMN_OFFSETS:
            line += get_binary_char()
        else:
            line += ' '

    if row % PHRASE_DISTANCE == PHRASE_DISTANCE - 1:
        phrase = phrases[randint(0, len(phrases) - 1)]
        left_align = (row + 1) % (2 * PHRASE_DISTANCE) == 0
        start = MARGIN if left_align else WIDTH - MARGIN - len(phrase)
        end = MARGIN + len(phrase) if left_align else WIDTH - MARGIN
        line = line[:start] + (' ' * len(phrase)) + line[end:]
    elif phrase != None and row % PHRASE_DISTANCE == 0:
        line = line[:start] + phrase + line[end:]
    elif phrase != None and row % PHRASE_DISTANCE == 1:
        line = line[:start] + (' ' * len(phrase)) + line[end:]
    elif phrase != None and row % PHRASE_DISTANCE == 2:
        printlines(lines + line)
        lines = ''
    else:
        start = MARGIN
        end = WIDTH - MARGIN
        phrase = None

    lines += line + '\n'
    row += 1
    sleep(60 / LPM)
