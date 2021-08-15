import yaml
from time import sleep, time
from random import random, randint
import art
import signal

results = [{
    'text': '        POSSIBLE, BUT TIME CONSUMING. PLEASE BE PATIENT.',
    'art': art.umbrella
}, {
    'text': 'POSSIBLE, BUT DIFFERENT FROM WHAT YOU IMAGINE. PLEASE KEEP AN OPEN MIND.',
    'art': art.motorcycle
}, {
    'text': '                      A SLAM DUNK',
    'art': art.elephant
}, {
    'text': '                   A LONG SHOT',
    'art': art.duck
}]

#must try to quit twice in 1s to succeed
last_interrupt = None
def handleinterrupt(signum, frame):
    global last_interrupt
    if last_interrupt != None and time() - last_interrupt < 1:
        exit()
    else:
        last_interrupt = time()

signal.signal(signal.SIGINT, handleinterrupt)
signal.signal(signal.SIGHUP, handleinterrupt)

with open('questions.yaml','r') as f:
    questions = yaml.safe_load(f.read())

def draw_title():
    print("""


                               WELCOME TO THE

        =============================================================
        |   _       __ ____ _____  __  __      ______ ______ __ __  |
        |  | |     / //  _// ___/ / / / /     /_  __// ____// //_/  |
        |  | | /| / / / /  \__ \ / /_/ /______ / /  /   /  / ,<     |
        |  | |/ |/ /_/ /  ___/ // __  //_____// /  / /___ / /, |    |
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
    frames = [ "_","_","_","-","`","'","'","-","_","_","_"]
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

def show_response(question, user_input):
    response = question['responses'][user_input]
    if 'respond' in response:
        print('')
        print(response['respond'])
        show_loader(duration=1)

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
        print('')
        print('Your answer is not valid. Please try again.')
        show_loader(duration=1)
        get_input(question)
        return
    #some questions always do the same thing
    if 'respond' in question:
        print('')
        print(question['respond'])
    if 'goto' in question:
        get_input(questions[question['goto']])
    elif 'responses' in question:
        show_response(question, user_input)
        get_input(get_next(question, user_input))

def end_session():
    print('Your wish is:')
    show_loader(duration=3)
    show_wish_result()
    show_loader(duration=2)

    print('Your wish will now be routed to Station 3. Please check in with the attendant.')
    print('')
    print('Fulfilling your wish is our top priority.')
    show_loader(duration=2)
    print('')
    print('Thank you for using WISH-TEK2000')
    print('Sorting, processing, and distributing wishes since 1978')
    show_loader(duration=10)


def show_wish_result():
    item = results[randint(0, len(results) - 1)]
    item['art']()
    print('')
    print(item['text'])
    print('')
    print('')
    print("    Press RETURN to continue.")
    input('')


while(True):
    first = questions['init']
    draw_title()
    print('                           Press RETURN to begin')
    print('')
    print('')
    input('')
    print(first['respond'])

    get_input(questions[first['goto']])

    end_session()




