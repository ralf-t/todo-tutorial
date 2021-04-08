from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

# Application configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = "somesecuredstring"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Model for database
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), nullable=False)
	description = db.Column(db.String(50), nullable=False)
	done = db.Column(db.Boolean)

# Form for creating todo
class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=20)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=50)])
    done = BooleanField('Done')
    submit = SubmitField()

# read
@app.route('/',methods=['get'])
def home():

	# fetch all data
	todo = Todo.query.all()

	return render_template('home.html', todo=todo)

# create
@app.route('/create',methods=['post','get'])
def create_todo():

	# create form object
	form = TodoForm()

	# handling form submission
	if form.validate_on_submit():
		
		# create a record
		todo = Todo(
				title=form.title.data,
				description=form.description.data,
				done=form.done.data
			)

		# submit to db and save
		db.session.add(todo)
		db.session.commit()

		return redirect(url_for('home'))

	return render_template('create_todo.html', form=form)

# update
@app.route('/edit/<int:todo_id>',methods=['post','get'])
def edit_todo(todo_id):
	
	# make sure record exists
	todo = Todo.query.get_or_404(todo_id)

	form = TodoForm()
	
	if form.validate_on_submit():
		
		# update task
		todo.title = form.title.data
		todo.description = form.description.data
		todo.done = form.done.data

		# save
		db.session.commit()

		return redirect(url_for('home'))

	elif request.method == 'GET':
	
		# prepopulate values if not submitting form
		form.title.data = todo.title
		form.description.data = todo.description
		form.done.data = todo.done

	return render_template('create_todo.html', form=form)

# edit
@app.route('/delete/<int:todo_id>',methods=['post'])
def delete_todo(todo_id):

	todo = Todo.query.get_or_404(todo_id)
	
	# delete and save
	db.session.delete(todo)
	db.session.commit()

	return redirect(url_for('home'))

# run the application on loop
if __name__ == "__main__":
	app.run(debug=True)