from flask import Flask, render_template ,request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    des = db.Column(db.String(200), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Create the database tables within the Flask application context
with app.app_context():
    db.create_all()
    print('db created')

@app.route("/", methods=['GET', 'POST'])
def product():
    title = ''
    des = ''
    if request.method == 'POST':
        title = request.form['title']
        des = request.form['des']
        todo = Todo(title=title, des=des)
        db.session.add(todo)
        db.session.commit()
        alltodo = Todo.query.all()

        # Return JSON response with the updated data
        # return jsonify({"success": True, "message": "Task added successfully"})

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route("/update/<int:sno>")
def update(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todos=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
