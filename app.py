from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'DDDDD3WEddjkfn1323454'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


# 表单
class HelloForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 20)])
    remember = BooleanField('Remenber me')
    submit = SubmitField()


# 模型
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')


@app.route('/form/', methods=['GET', 'POST'])
def test_form():
    form = HelloForm()
    return render_template('form.html', form=form)


@app.route('/pagination/', methods=['GET', 'POST'])
def test_pagination():
    db.drop_all()
    db.create_all()
    for i in range(100):
        m = Message()
        db.session.add(m)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page, per_page=10)
    messages = pagination.items
    return render_template('pagination.html', pagination=pagination, messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
