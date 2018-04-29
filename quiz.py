import copy
import random

from flask import render_template, request


def get_values(filename):
    original_questions = {}
    with open("data/quizQues.txt") as f:
        for line in f:
            (key, val) = line.strip().split(':')
            original_questions[key] = val.split(",")
    return original_questions


original_questions = get_values('data/quizQues.txt')
questions = copy.deepcopy(original_questions)


def shuffle(q):
    """
    This function is for shuffling
    the dictionary elements.
    """
    selected_keys = []
    i = 0
    while i < len(q):
        current_selection = random.choice(list(q.keys()))
        if current_selection not in selected_keys:
            selected_keys.append(current_selection)
            i = i + 1
    return selected_keys


def quiz():
    questions_shuffled = shuffle(questions)
    for i in questions.keys():
        random.shuffle(questions[i])
    return render_template('quizHTML.html', q=questions_shuffled, o=questions)


def quiz_answers():
    from quiz import questions, original_questions
    from flask import request
    correct = 0

    response = '\n'
    for i in list(questions.keys()):
        answered = request.form[i]
        response = response + '\nQuestion: ' + i + "\n" + 'Your answer ' + answered + '\n'
        if original_questions[i][0] == answered:
            correct = correct + 1
            response = response + "is correct" + '\n'
        else:
            response = response + "is incorrect" + '\n'
    return
    '<h1>' + str(correct) + '<pre>' + ' Correct answers:' + str(response) + '</pre' + '</h>'

    return render_template('quizAnswers.html')

