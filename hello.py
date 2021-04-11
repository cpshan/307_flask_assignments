from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string
app = Flask(__name__)
CORS(app)

users = {'users_list' : [
	{'id' : 'xyz789', 'name' : 'Charlie', 'job' : 'Janitor'},
	{'id' : 'abc123', 'name' : 'Mac', 'job' : 'Bouncer'},
	{'id' : 'ppp222', 'name' : 'Mac', 'job' : 'Professor'},
	{'id' : 'yat999', 'name' : 'Dee', 'job' : 'Aspiriing Actress'},
	{'id' : 'zap555', 'name' : 'Dennis', 'job' : 'Bartender'}]}

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
		userToAdd['id'] = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)\
							+ str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9))
		users['users_list'].append(userToAdd)
		resp = jsonify(success=True)
		resp.status_code = 201
		return userToAdd
	elif request.method == 'DELETE':
		userToDelete = request.get_json()
		resp = jsonify(success=False)
		try:
			users['users_list'].remove(userToDelete)
			resp = jsonify(success=True)
			resp.status_code = 204
		except ValueError:
			resp.status_code = 404
		return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
	if request.method == 'GET':
		if id:
			for user in users['users_list']:
				if user['id'] == id:
					return user
			return ({})
		return users	
	elif request.method == 'DELETE':
		resp = jsonify(success=False)
		userToDelete = None
		if id:
			for user in users['users_list']:
				if user['id'] == id:
					userToDelete = user
		try:
			users['users_list'].remove(userToDelete)
			resp = jsonify(success=True)
			resp.status_code = 204
		except ValueError:
			resp.status_code = 404
		return resp