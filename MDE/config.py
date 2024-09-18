"""MDE development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\t\xa7\x16\xa3\x1ct\x8e\xdf\xcf.\x14\\\\m\xa5\x03\xa7d\xa2/\xa1\x11L\x90'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
MDE_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = MDE_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/database.sqlite3
DATABASE_FILENAME = MDE_ROOT/'var'/'database.sqlite3'
