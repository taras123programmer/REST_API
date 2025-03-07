from flask import current_app as app

@app.route('/')
def main():
    return "Hello!"