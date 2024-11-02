from peewee import *

db = SqliteDatabase('receitas.db')
class Receita (Model):
   name=TextField(unique=True)
   text=TextField()
   class Meta:
      database=db
      db_table='Receita'
      
class Users(Model):
   username = CharField(unique=True, max_length=10)
   password = CharField(max_length=50)
   class Meta:
      database=db
      db_table='Users'

db.create_tables([Receita, Users])