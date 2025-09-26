class Config:
    SECRET_KEY = '891752ade6b71f6a47407f4e42b5a81f37df3c7b52582e26f56b55a7987bf46e'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactiva las notificaciones de modificaciones
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:@localhost/hiraoka_sistema_gestion'
    )