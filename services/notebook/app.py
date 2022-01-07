from flask import Flask, render_template, request
import os, utility, db

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create_note():
    data = request.form
    name = data['note-name']
    text = data['text']
    key = data['key']

    if os.path.isfile('notes/%s' % name):
        return "Note with this name already exists."

    with open('notes/%s' % name, 'w') as f:
        f.write(utility.encrypt(text, key))

    db.add_note(name, key)
    return "Note successfully created!"


@app.route('/note', methods=['POST'])
def render_note():
    data = request.form
    name = data['note-name']
    key = data['key']
    text = os.popen('cat "notes/%s"' % name).read()
    print('cat "notes/%s"' % name)
    print(text)

    if db.get_key(name) == key:
        text = utility.decrypt(text, key)
    return text


if __name__ == "__main__":
    app.run("0.0.0.0", 8616)

#" || python3 -c "import db; print(list(db.Note.select().dicts()));