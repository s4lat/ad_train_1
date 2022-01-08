from flask import Flask, request, render_template_string, redirect
from random import randint
import os, hashlib

app = Flask(__name__)

INDEX_PAGE = """
<form action="/" method="POST">
<label for="name"> Content: <br></label>
<input type="text" id="content" name="content" placeholder="2 + 2 * 2 = 8"/>
<button type="sumbit"> Save paste </button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		content = request.values.get("content")
		if not len(content):
			return render_template_string("Paste should not be empty!")

		h = (str(randint(0, 13370)) + content + str(randint(0, 13370))).encode("utf-8")
		h = hashlib.sha1(h).hexdigest()
		with open("pastes/" + h + ".paste", "w") as f:
			f.write(content)

		return redirect("/paste/%s" % h)

	return render_template_string(INDEX_PAGE)

@app.route("/paste/<string:h>")
def paste(h):
	if os.path.isfile("pastes/" + h + ".paste") :
		with open("pastes/" + h + ".paste") as f:
			return render_template_string(f.read())

	return render_template_string("There are no such paste(")

if __name__ == "__main__":
	app.run("0.0.0.0", 8080)