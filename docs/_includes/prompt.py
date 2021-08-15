from time import sleep
from random import random, randint
import json
import js

results = [{
    'text': '        POSSIBLE, BUT TIME CONSUMING. PLEASE BE PATIENT.',
    'art': js.document.getElementById('ascii-umbrella').textContent
}, {
    'text': 'POSSIBLE, BUT DIFFERENT FROM WHAT YOU IMAGINE. PLEASE KEEP AN OPEN MIND.',
    'art': js.document.getElementById('ascii-motorcycle').textContent
}, {
    'text': '                      A SLAM DUNK',
    'art': js.document.getElementById('ascii-elephant').textContent
}, {
    'text': '                   A LONG SHOT',
    'art': js.document.getElementById('ascii-duck').textContent
}]

questions_json = """
{% include questions.json %}
"""

questions = json.loads(questions_json)

def draw_title():
    print("Welcome to the WISH-TEK 2000")

def show_prompt(options):
    if options:
        print('[%s] ' % options)

def get_type(question):
    if 'range' in question:
        return range
    elif 'responses' in question:
        t = type(question['responses'])
        if t is list or t is dict:
            return t
        else:
            raise TypeError('responses are not a valid type')
    elif 'respond' in question:
        return True
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
        return question['responses'][user_input]['goto']

def show_response(question, user_input):
    response = question['responses'][user_input]
    if 'respond' in response:
        print('')
        print(response['respond'])

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
    elif 'respond' in question:
        return True
    elif 'responses' in question:
        return user_input in question['responses'].keys()
    else:
        return True

def request_input(question_name):
    question = questions[question_name]
    print('')
    print(question['text'])
    if get_type(question) == None:
        end_session()
    show_options(question)
    show_prompt(get_options(question))

def handle_input(question_name, response):
    user_input = response.upper()
    question = questions[question_name]
    if not input_is_valid(question, user_input):
        print('')
        print('Your answer is not valid. Please try again.')
        return
    #some questions always do the same thing
    if 'respond' in question:
        print('')
        print(question['respond'])
    if 'goto' in question:
        request_input(question['goto'])
        return question['goto']
    elif 'responses' in question:
        show_response(question, user_input)
        next_question = get_next(question, user_input)
        request_input(next_question)
        return next_question

def end_session():
    print('')
    print('')
    print('Your wish is:')
    sleep(2)
    show_wish_result()
    print('')
    print('Press RETURN to continue.')


def show_wish_result():
    item = results[randint(0, len(results) - 1)]
    print('')
    print(item['text'])
    print(item['art'])
    print('')
    print('')


