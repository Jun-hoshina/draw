from flask import Flask
app = Flask(__name__)

from templates.views import main
from draw.views import game

app.register_blueprint(main,template_folder='templates')
app.register_blueprint(game,template_folder='templates',static_folder="static", url_prefix="/draw")

if __name__=='__main__':
    app.run(debug=True)