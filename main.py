from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/autopass')
def autopass():
    return render_template('autopass.html')

@app.route('/peoplepass')
def peoplepass():
    return render_template('peoplepass.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    input_values = []
    input_values.append(request.form['FCs'])
    input_values.append(request.form['dateS'])
    input_values.append(request.form['dateE'])
    input_values.append(request.form['passport'])
    input_values.append(request.form['address'])
    input_values.append(request.form['citizenship'])
    input_values.append(request.form['post'])
    input_values.append(request.form['purpose'])
    # Делайте что-то с input_value, например сохраните его в переменную
    print(input_values)
    return 'Значение поля ввода: {}'.format(input_values)

if __name__ == '__main__':
    app.run(port=2111, debug=True)