from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, title="Stark Bank Challenge", description="Stark Bank Back End Developer Test")

if __name__ == '__main__':
    app.run(debug=True)