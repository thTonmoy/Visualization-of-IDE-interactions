from flask import Flask, render_template, Markup
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
    return render_template("dashboard.html",title='Home',chart=chart)


@app.route('/tree')
def show_tree_chart():
    return render_template("tree.html",title='Tree graph')


@app.route('/rb')
def show_refactoring_build_vis():
    chart = Markup(get_div_for_plot(app.root_path))
    return render_template("index.html", title='Home', chart=chart)

if __name__ == '__main__':
    app.run()
