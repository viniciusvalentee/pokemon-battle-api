from flask import Flask

# Flask instance creation
# __name__ argument helps Flask to know where to find resources like templates.
app = Flask(__name__)

# Basic route definition


@app.route('/')
def home():
    return "Hello, World!"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
