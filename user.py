from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, password, name, role):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.role = role
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        self.get_id = email

    def __str__(self):
        return "{},{},{},{},{}".format(self.id, self.email, self.password, self.name, self.role,
                                       self.is_authenticated, self.is_active, self.is_anonymous, self.get_id)

    # Necessary functions for Flask-Login session management
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        # Anonymous users aren't supported
        return False

    def get_id(self):
        return self.get_id
