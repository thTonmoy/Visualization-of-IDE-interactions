from flask import Flask, render_template, Markup
from feature_by_hour import get_bar_chart_div
from refactoring_test_failure import get_div_for_plot
from WorldMap import get_map

app = Flask(__name__)


@app.route('/Bar')
def hello_world():
    chart = Markup(get_bar_chart_div(app.root_path))
    return render_template("index.html", title='Bar Chart', chart=chart)


@app.route('/')
def show_template():
    chart = Markup(get_bar_chart_div(app.root_path))
    return render_template("dashboard.html", title='Home', chart=chart)


@app.route('/tree')
def show_tree_chart():
    return render_template("tree.html", title='Commands and Triggers',
                           desc='Which IDE commands are used the most and how they are triggered')


@app.route('/rb')
def show_refactoring_build_vis():
    chart = Markup(get_div_for_plot(app.root_path))
    return render_template("index.html", title='Refactoring',
                           desc='Does Refactoring impact Test and Build Failures', chart=chart)


@app.route('/map')
def world_map():
    w_map = Markup(get_map(app.root_path))
    return render_template("Wmap.html", title='Map', chart=w_map)


@app.route('/spidy')
def Spider_Web():
    spider = Markup(get_map(app.root_path))
    return render_template("spidy.html", title='Spider', chart=spider)


@app.route('/network')
def network():
    network = Markup(get_map(app.root_path))
    return render_template("network.html", title='Network', chart=network)


@app.route('/quiz')
def show_quiz():
    from quiz import questions, shuffle
    import random
    questions_shuffled = shuffle(questions)
    for i in questions.keys():
        random.shuffle(questions[i])
    return render_template('quizHTML.html', q=questions_shuffled, o=questions)


@app.route('/quizAns', methods=['POST'])
def show_quiz_answers():
    from quiz import questions, original_questions
    from flask import request
    correct = 0
    corAns = ''
    next = ',  \n'

    for i in list(questions.keys()):
        answered = request.form[i]
        if original_questions[i][0] == answered:
            correct = correct + 1
            corAns = corAns + answered + next
    return '<h1><u>' + str(correct) + ' Correct answers: ' + str(corAns) + '</u></h1>'


if __name__ == '__main__':
    app.run(debug=True)
