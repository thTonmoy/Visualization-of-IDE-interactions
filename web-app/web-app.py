from flask import Flask, render_template, Markup
from feature_by_hour import get_bar_chart_div

app = Flask(__name__)


@app.route('/')
def hello_world():
    chart = Markup(get_bar_chart_div(app.root_path))
    return render_template("index.html",title='Home', chart=chart)


if __name__ == '__main__':
    app.run()
