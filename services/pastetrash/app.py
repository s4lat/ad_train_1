from flask import Flask, request, render_template_string, redirect, Response
from random import randint
from db import db, User, Paste
import os, hashlib, base64

app = Flask(__name__)

NONAUTH_INDEX_PAGE = """
<h2> NEW ANONYMOUS PASTE </h2>
<form action="/" method="POST">
<label for="name"> Content: <br></label>
<input type="text" id="content" name="content" placeholder="2 + 2 * 2 = 8"/>
<button type="sumbit"> Save paste anonymously </button>
</form>

<h2> Login or register </h2>
<form action="/auth" method="POST">
<label for="name"> Username: </label><br>
<input type="text" id="username" name="username" placeholder="Vasya2007"/><br>
<label for="name"> Password: </label><br>
<input type="password" id="pwd" name="pwd"/><br>
<button type="sumbit"> Confirm </button>
</form>
"""

AUTH_INDEX_PAGE = """
<h2> NEW PASTE </h2>
<form action="/" method="POST">
<label for="name"> Content: <br></label>
<input type="text" id="content" name="content" placeholder="2 + 2 * 2 = 8"/>
<button type="sumbit"> Save paste anonymously </button>
</form>

<h2> Your pastes </h2>
<ul>
	%s
</uL>
<hr>
Hello, you athorized as <strong>%s</strong>.
<a href="/logout"> Logout </a>
"""

@app.route("/", methods=["GET", "POST"])
def index():
	db.connect()
	is_auth = True
	try:
		cookies = request.cookies.get("auth")
		user = base64.b64decode(cookies.encode('utf-8'))
		user = user.decode('utf-8').split(':')
		user = {"id" : user[0], "username" : user[1], "pwd" : user[2]}
	except Exception as e:
		is_auth = False

	if request.method == "POST":
		content = request.values.get("content")
		if not len(content):
			db.close()
			return render_template_string("Paste should not be empty!")

		h = (str(randint(0, 13370)) + content + str(randint(0, 13370))).encode("utf-8")
		h = hashlib.sha1(h).hexdigest()
		with open("pastes/" + h + ".paste", "w") as f:
			f.write(content)

		if is_auth:
			try:
				user = User.get(username=user['username'], pwd=user['pwd'])
				if user:
					Paste.create(file_name=h, owner=user)
				db.close()
				return redirect("/")
			except User.DoesNotExist:
				pass

		db.close()
		return redirect("/paste/%s" % h)

	if is_auth:
		try:
			user_in_db = User.get(username=user['username'], pwd=user['pwd'])
		except User.DoesNotExist:
			db.close()
			return render_template_string(NONAUTH_INDEX_PAGE)

		pastes = [paste.file_name for paste in Paste.select().where(Paste.owner == user["id"])]
		pastes = [f'<li><a href="/paste/{paste}" target="_blank" rel="noopener noreferrer"> {paste} </a></li>' for paste in pastes]

		db.close()
		return render_template_string(AUTH_INDEX_PAGE % ('<br>'.join(pastes), 
			user["username"]))
	
	db.close()
	return render_template_string(NONAUTH_INDEX_PAGE)

@app.route("/paste/<string:h>")
def paste(h):
	if os.path.isfile("pastes/" + h + ".paste") :
		with open("pastes/" + h + ".paste") as f:
			return render_template_string(f.read())

	return render_template_string("There are no such paste(")

@app.route("/auth", methods=["POST"])
def register():
	db.connect()
	username = request.values.get("username")
	pwd = request.values.get("pwd")
	
	if not (username and pwd):
		return "bad request"

	user = User.get_or_create(username=username, pwd=pwd)[0]
	token = "%s:%s:%s" % (user.id, user.username, user.pwd)
	token = str(base64.b64encode(token.encode('utf-8')))[2:-1]

	resp = redirect("/")
	resp.set_cookie(key="auth", value=token, max_age=9999999)
	db.close()
	return resp

@app.route("/logout", methods=["GET"])
def logout():
	resp = redirect("/")
	resp.delete_cookie(key="auth")
	return resp

if __name__ == "__main__":
	app.run("0.0.0.0", 8080)