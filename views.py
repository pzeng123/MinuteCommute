from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is your working location?', validators=[Required()])
    submit = SubmitField('Submit')


application = Flask(__name__, template_folder="templates")
bootstrap = Bootstrap(application)

input_path = 'position3.txt'

application.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


@application.route("/", methods=['GET', 'POST'])


def mapview():
    name = None
    form = NameForm()
    # creating a map in the view
    mymap = []
    mytime = []
    with open('position3.txt', "r") as inputfile:
        for current_appartment in inputfile:
            current_appartment = current_appartment.strip().split('|')
            location = [float(current_appartment[0].split(',')[0]), float(current_appartment[0].split(',')[1])]
            time = float(current_appartment[1])
            mymap.append(location)
            mytime.append(time)
			

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        return render_template('map.html', maymap=mymap, mytime=mytime)
    return render_template('index.html', form=form, name=name)
@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0',debug=True)

