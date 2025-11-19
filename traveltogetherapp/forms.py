from wtforms import Form, StringField, PasswordField, TextAreaField, validators


class RegisterForm(Form):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.Length(min=6, message="Password must be at least 6 characters long."),
        ],
    )


class LoginForm(Form):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])


class ProfileForm(Form):
    description = TextAreaField("Description", [validators.Optional(), validators.Length(max=500)])
