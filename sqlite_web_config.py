from passlib.hash import pbkdf2_sha256

CONFIG = {
    'db_filename': '/home/unialco/portaria/portaria.db',
    'password_hash': pbkdf2_sha256.hash('u200809gx5'),
    'password_salt': '12',
}
