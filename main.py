import yaml
from time import sleep
from random import random

with open('questions.yaml','r') as f:
    questions = yaml.safe_load(f.read())

def draw_title():
    print("""

                           WELCOME TO THE
    
    =============================================================
    |   _       __ ____ _____  __  __      ______ ______ __ __  |
    |  | |     / //  _// ___/ / / / /     /_  __// ____// //_/  |
    |  | | /| / / / /  \__ \ / /_/ /______ / /  / __/  / ,<     |
    |  | |/ |/ /_/ /  ___/ // __  //_____// /  / /___ / /| |    | 
    |  |__/|__//___/ /____//_/ /_/       /_/  /_____//_/ |_|    | 
    |             ___   ____   ____   ____                      | 
    |            |__ \ / __ \ / __ \ / __ \                     | 
    |            __/ // / / // / / // / / /                     | 
    |           / __// /_/ // /_/ // /_/ /                      | 
    |          /____/\____/ \____/ \____/                       | 
    |                                                           | 
    =============================================================

    """)

def show_prompt(options):
    user_input = input('[%s] ' % options)
    return user_input

def show_loader(duration=.5):
    fill = '█'
    frames = [ "_","_","_","-","`","'","´","-","_","_","_"]
    rate = .07
    time = 0
    frame = 0
    while time < duration:
        print('\r%s' % frames[frame], end = '\r')
        frame = frame + 1 if frame < len(frames) - 1 else 0
        sleep(rate)
        time += rate
    print('\r  ', end='\r')

def get_type(question):
    t = type(question['responses'])
    if t is list or t is dict:
        return t
    else:
        raise TypeError('responses are not a valid type')

def show_options(question):
    if get_type(question) is list:
        i = 1
        for item in question['responses']:
            print('%d: %s' % (i, item))
            i += 1

def get_options(question):
    r = question['responses']
    if get_type(question) is list:
        return '1 - %d' % len(r)
    else:
        return '/'.join(r.keys())


def get_next(question, user_input):
    if get_type(question) is list:
        raise NameError("List of responses was given without goto.")
    else:
        return questions[question['responses'][user_input]['goto']]

def input_is_valid(question, user_input):
    if get_type(question) is list:
        return int(user_input) in range(1, len(question['responses']))
    else:
        return user_input in question['responses'].keys()


def get_input(question):
    print('')
    print(question['text'])
    show_options(question)
    user_input = show_prompt(get_options(question)).upper()
    show_loader(duration = random())
    if not input_is_valid(question, user_input):
        print("Your answer is not valid. Please try again.")
        get_input(question)
        return
    #some questions always do the same thing
    if 'respond' in question:
        print(question['respond'])
    if 'goto' in question:
        get_input(questions[question['goto']])
    else:
        get_input(get_next(question, user_input))

while(True):
    first = questions['init']
    draw_title()
    print("Press ENTER to begin")
    input('')
    print(first['respond'])

    get_input(questions[first['goto']])

