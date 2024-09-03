import re
emailRe = re.compile(r'[^@]+@[^@]+\.[^@]+')
passwordRe = re.compile(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,20})')


def validate_username(username: str) -> bool:
    return re.fullmatch(emailRe, username) is None


def validate_password(password: str) -> bool:
    return re.fullmatch(passwordRe, password) is None
