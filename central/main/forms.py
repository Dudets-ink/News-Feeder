from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length


class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[Length(min=4, max=1000)])
    submit = SubmitField('Submit')