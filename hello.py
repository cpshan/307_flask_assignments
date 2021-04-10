from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

users = {'users_list' : [
	{'id' : 'xyz789', 'name' : 'Charlie', 'job' : 'Janitor'},
	{'id' : 'abc123', 'name' : 'Mac', 'job' : 'Bouncer'},
	{'id' : 'ppp222', 'name' : 'Mac', 'job' : 'Professor'},
	{'id' : 'yat999', 'name' : 'Dee', 'job' : 'Aspiriing Actress'},
	{'id' : 'zap555', 'name' : 'Denni', 'job' : 'Bartender'}]}

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
	if request.method == 'GET':
		search_username = request.args.get('name')	#accessing the value of parameter 'name'
		search_job = request.args.get('job')		#looks like .../users?name=Mac
		if search_username:							
			subdict = {'users_list' : []}
			for user in users['users_list']:
				if user['name'] == search_username:
					if (not search_job) or (search_job and user['job'] == search_job):
						subdict['users_list'].append(user)
			return subdict
		return users
	elif request.method == 'POST':
		userToAdd = request.get_json()
		users['users_list'].append(userToAdd)
		resp = jsonify(success=True)
		resp.status_code = 201
		return resp		#forgot this at first
	elif request.method == 'DELETE':
		userToDelete = request.get_json()
		users['users_list'].remove(userToDelete)
		resp = jsonify(success=True)
		return resp

@app.route('/users/<id>')
def get_user(id):
	if id:
		for user in users['users_list']:
			if user['id'] == id:
				return user
		return ({})
	return users