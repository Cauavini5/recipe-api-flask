from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import Receita, Users
import jwt
from datetime import datetime, timedelta, timezone
from flask_bcrypt import Bcrypt 
import os 


'''
   token = request.headers.get('Authorization')
   if not token:
        return jsonify({'message': 'Token não fornecido!'}), 401

   if token.startswith("Bearer "):
        token = token[7:]  

   try:
         decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
         receitas_to_view = Receita.select()
         listview = [{'name':receita.name, 'text':receita.text} for receita in receitas_to_view]
         return jsonify(listview), 200
   except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expirado!'}), 401
   except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido!'}), 401

'''

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/')
def hello_world():
   return 'Hello, From Receitas.net!'

@app.route('/receitas',methods=['GET',])
def receitas_list():

         receitas_to_view = Receita.select()
         listview = [{'name':receita.name, 'text':receita.text} for receita in receitas_to_view]
         return jsonify(listview), 200



@app.route('/criar', methods=['POST',])
def create_receitas():
   data = request.get_json()
   receita_to_create = Receita(name=data['name'], text=data['text'])
   receita_to_create.save()
   return jsonify([{'message':'Created'}])

@app.route('/receitas/delete/<int:id>', methods=['DELETE', ])
def DeleteReceita(id):
   receita_to_delete = Receita.get(Receita.id == id)
   receita_to_delete.delete_instance()
   return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/register', methods=['POST', ])
def register():
   data = request.get_json()
   username = data['username']; password = data['password'];
   hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
   user_to_save = Users(username=username, password=hash_password)
   user_to_save.save()
   return jsonify({'message':'User created successfull!'})

@app.route('/login', methods=['POST', ])
def login():
   data = request.get_json()
   username = data['username']; 
   password = data['password'];
   user = Users.get(Users.username==username)
   hash_pass = user.password
   if not bcrypt.check_password_hash(hash_pass, password):
      return jsonify({'message': 'Senha incorreta!'}), 401
   else:
      token = jwt.encode(
         {
            'username': username, 
            'exp': datetime.now(timezone.utc) + timedelta(minutes=10)
         },
         app.config['SECRET_KEY'],
         algorithm='HS256'
      )
      return jsonify({'token': token}), 200
      

if __name__== '__main__':
 app.run(debug=True)