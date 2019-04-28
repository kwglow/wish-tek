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
    if options:
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
    if 'range' in question:
        return range
    elif 'responses' in question:
        t = type(question['responses'])
        if t is list or t is dict:
            return t
        else:
            raise TypeError('responses are not a valid type')
    else:
        return None

def show_options(question):
    if get_type(question) is list:
        i = 1
        for item in question['responses']:
            print('%d: %s' % (i, item))
            i += 1

def get_options(question):
    if get_type(question) is list:
        return '1 - %d' % len(question['responses'])
    elif get_type(question) is range:
        r = question['range']
        return '%d - %d' % (r['min'], r['max'])
    elif get_type(question) is dict:
        return '/'.join(question['responses'].keys())


def get_next(question, user_input):
    if get_type(question) is list:
        raise NameError("List of responses was given without goto.")
    else:
        return questions[question['responses'][user_input]['goto']]

def safe_int(user_input):
    try:
        return int(user_input)
    except ValueError:
        return None

def input_is_valid(question, user_input):
    if get_type(question) is list:
        return safe_int(user_input) in range(1, len(question['responses']) + 1)
    elif get_type(question) is range:
        r = question['range']
        return safe_int(user_input) in range(r['min'], r['max'])
    else:
        return user_input in question['responses'].keys()


def get_input(question):
    print('')
    print(question['text'])
    if get_type(question) == None:
        return
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
    elif 'responses' in question:
        get_input(get_next(question, user_input))

def end_session():
    print("Your wish is:")
    show_loader(duration=2)
    show_wish_result()

    print("Your wish will now be routed to Station X. Please check in with the attendant.")
    print("")
    print("Fulfilling your wish is our top priority.")
    print("")
    print("Thank you for using WISH-TEK2000")
    print("Sorting, processing, and distributing wishes since 1978")
    show_loader(duration=10)


def show_wish_result():
    print("TBD")

while(True):
    first = questions['init']
    draw_title()
    print("Press ENTER to begin")
    input('')
    print(first['respond'])

    get_input(questions[first['goto']])

    end_session()

