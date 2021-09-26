class User():
    def __init__(self, id, email, password, name, role):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    def __str__(self):
        return "{},{},{},{},{}".format(self.id, self.email, self.password, self.name, self.role,
                                       self.is_authenticated, self.is_active, self.is_anonymous, self.get_id)

    # Necessary functions for Flask-Login session management
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        # Anonymous users aren't supported
        return False

    def get_id(self):
        return str(self.email)
