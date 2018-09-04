# Set up a local web interface to take data from using Flask
from flask import Flask, render_template, request, url_for
app = Flask(__name__)

# Index
@app.route('/')
def index():
    return render_template('mdrive.html')

# Incremental form submission
@app.route('/handleIncremental', methods=['POST'])
def handleIncremental():
    dir = request.form['dir']
    cts = request.form['cts']
    incAngle = request.form['incAngle']
    stopAngle = request.form['stopAngle']
    return render_template('mdrive.html')

# Specific form submission
@app.route('/handleSpecific', methods=['POST'])
def handleSpecific():
    angle = request.form['angle']
    return render_template('mdrive.html')

# Automatically run in debug mode
if __name__ == '__main__':
    app.run(debug = True)
