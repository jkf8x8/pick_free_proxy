from flask import Flask

import controller
app = Flask(__name__)

ctl = controller.Controller()

@app.route('/')
def hello_world():

    return 'Hello World22!'

@app.route('/random')
def t():
    ctl.random()
    return 'ok'


if __name__ == '__main__':
    ctl.run()
    app.run(debug=False)
