from flask import Flask, render_template, Markup, request
from feature_by_hour import get_bar_chart_div
from refactoring_test_failure import get_div_for_plot

app = Flask(__name__)


@app.route('/Bar')
def hello_world():
    chart = Markup(get_bar_chart_div(app.root_path))
    return render_template("index.html",title='Bar Chart', chart=chart)


@app.route('/')
def show_template():
    chart = Markup(get_bar_chart_div(app.root_path))
    return render_template("dashboard.html", title='Home', chart=chart)


@app.route('/tree')
def show_tree_chart():
    return render_template("tree.html", title='Commands and Triggers',
                           desc='Which IDE commands are used the most and how they are triggered')


@app.route('/rb', methods=['GET', 'POST'])
def show_refactoring_build_vis():
    dev_id = 2
    if request.method == 'POST':
        dev_id = request.form['dev']
    chart = Markup(get_div_for_plot(app.root_path, int(dev_id)))
    return render_template("index.html", title='Refactoring',
                           desc='How Refactoring impacts Test and Build Failures', chart=chart)


@app.route('/map')
def world_map():
    from WorldMap import get_map
    w_map = Markup(get_map(app.root_path))
    return render_template("Wmap.html", title='Map', chart=w_map)


@app.route('/spidy')
def Spider_Web():
    return render_template("spidy.html", title='Spider')

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
    correct_amount = 0
    response = ''

    for i in list(questions.keys()):
        answered = request.form[i]
        response = response + '\nQuestion: ' + i + "\n" + 'Your answer ' + answered + '\n'
        if original_questions[i][0] == answered:
            correct_amount = correct_amount + 1
            response = response + "Correct" + '\n'
        else:
            response = response + "Incorrect, correct answer: " + original_questions[i][0]+ '\n'

    return render_template('quizAnswers.html', cor_amount=correct_amount, cor_answers=response.split('\n'))


@app.route('/cluster')
def show_cluster():
    from cluster_debug_build import get_cluster_viz_dv
    viz = Markup(get_cluster_viz_dv(app.root_path))
    return render_template('cluster.html', chart=viz)

@app.route('/network')
def show_net():
    return render_template('NetworkGraph.html')


if __name__ == '__main__':
    app.run(debug=True)
    #app.run()
