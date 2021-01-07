# forms.py users
from cuneiform.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms import ValidationError


def appropriate_credentials(form, field):
    """Checks username/password """

    password = field.data
    email = form.email.data

    user = User.query.filter_by(email=self.email.data).first()
    # Check username is valid

    if user is None:
        raise ValidationError("Username or password is incorrect")

    # Check password is valid
    if not user.check_password(password):
        raise ValidationError("Username or password is incorrect")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[InputRequired(message="Email required"), Email()]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(message="Password required")]
    )
    submit = SubmitField("Log in")

    # check if password is valid
    def validate_password(self, field):
        password = field.data
        user = User.query.filter_by(email=self.email.data).first()
        # if user doesnt exist password is incorrect, display message
        if not user or not user.check_password(password):
            raise ValidationError("Email or password is incorrect")


class RegistrationForm(FlaskForm):
    len_err_msg = lambda x, min, max: f"{x} must be between {min} and {max} characters"
    min, max = User.email_min_len, User.email_max_len
    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(message="Invalid email"),
            Length(min=min, max=max, message=len_err_msg("Email", min, max)),
        ],
    )

    min, max = User.username_min_len, User.username_max_len
    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(min=min, max=max, message=len_err_msg("Username", min, max)),
        ],
    )

    min, max = User.pass_min_len, User.pass_max_len
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            EqualTo("pass_confirm", message="Passwords must match!"),
            Length(min=min, max=max, message=len_err_msg("Password", min, max)),
        ],
    )

    pass_confirm = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            Length(min=min, max=max, message=len_err_msg("Password", min, max)),
        ],
    )

    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been already registered!")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username is taken!")
