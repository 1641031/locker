from app import app, db
from app.models import User,Locker


# flask shell 
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,'Locker':Locker}