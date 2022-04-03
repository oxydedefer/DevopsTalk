import os
from flask import Flask, render_template
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/')
def hello_world():
   return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, host='0.0.0.0', port=port)