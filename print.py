import yaml
from random import randint
from time import sleep

DEVICE='printout.txt'

WIDTH = 100
MARGIN = 7
COLUMN_OFFSETS = [20, 40, 60, 80]
PHRASE_DISTANCE = 30
LPM = 100


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
    else:
        start = MARGIN
        end = WIDTH - MARGIN
        phrase = None

    print(line)
    row += 1
    sleep(60 / LPM)
