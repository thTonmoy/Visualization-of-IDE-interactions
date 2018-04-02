from flask import Flask, render_template, Markup
from feature_by_hour import get_bar_chart_div
from refactoring_test_failure import get_div_for_plot
from WorldMap import get_map

app = Flask(__name__)


@app.route('/Bar')
def hello_world():
    chart = Markup(get_bar_chart_div(app.root_path))
    return render_template("index.html",title='Bar Chart', chart=chart)


@app.route('/')
def show_template():
    chart = Markup(get_bar_chart_div(app.root_path))
    return render_template("dashboard.html", title='Home',chart=chart)


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
    return render_template("Wmap.html", title='Map', chart= w_map)

@app.route('/spidy')
def Spider_Web():
    spider = Markup(get_map(app.root_path))
    return render_template("spidy.html", title='Spider', chart= spider)


if __name__ == '__main__':
    app.run()
