from generator import Poet
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


CHOICES = open('poets.txt', 'r', encoding='utf-8').readlines()


class Form(FlaskForm):
    seed = StringField('Podaj zdanie, od którego rozpoczynać się będzie wygenerowany wiersz:', validators=[DataRequired()])
    poet = SelectField('Wybierz poetę:', choices=[poet.strip() for poet in CHOICES])
    submit = SubmitField('Wygeneruj')

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'secret key :)'


@app.route('/', methods=['GET', 'POST'])
def index():
    seed, poem = None, None
    form = Form()
    if form.validate_on_submit():
        seed = form.seed.data
        poet_name = form.poet.data
        poet = Poet(poet_name, seed)
        poem = poet.generate()
        form.seed.data = ''
    return render_template('index.html', form=form, seed=seed, poem=poem)



# if __name__ == '__main__':
#     app.run()
