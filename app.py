import datetime
from flask import Flask
from flaskext.auth import Auth
from flaskext.db import Database
from flaskext.admin import Admin, ModelAdmin
from flaskext.rest import RestAPI
from peewee import *

# configure our database
DATABASE = {
	'name': 'example.db',
	'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhh'

app = Flask(__name__)
app.config.from_object(__name__)

# instiantate the db wrapper
db = Database(app)

class Note(db.Model):
	message = TextField()
	created = DateTimeField(default=datetime.datetime.now)

class NoteAdmin(ModelAdmin):
	columns = ('message', 'created',)


class Person(db.Model):
	name = CharField(max_length=50)
	surname = CharField(max_length=50)
	created = DateTimeField(default=datetime.datetime.now)

class PersonAdmin(ModelAdmin):
	columns = ('name','surname','created',)


auth = Auth(app, db)

admin = Admin(app, auth)
admin.register(Note, NoteAdmin)
admin.register(Person, PersonAdmin)
admin.setup()

api = RestAPI(app)
api.register(Note)
api.setup()

if __name__ == '__main__':
	auth.User.create_table(fail_silently=True)
	Note.create_table(fail_silently=True)
	Person.create_table(fail_silently=True)

	app.run()


