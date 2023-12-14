from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('routes/index.html', name=name)


@app.route('/testcomm')
def testcomm():
    return render_template('routes/testcomm.html')


@app.route('/webdynconfig')
def webdynconfig():
    return render_template('routes/webdynconfig.html')

@app.route('/suivilogs')
def suivilogs():
    return render_template('routes/suivilogs.html')

@app.route('/pontbascule')
def pontbascule():
    return render_template('routes/pontbascule.html')

@app.route('/webdynemul')
def webdynemul():
    return render_template('routes/webdynemul.html')

@app.route('/config')
def config():
    return render_template('routes/config.html')