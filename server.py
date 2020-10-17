from flask import Flask, request, jsonify, render_template
from query import query
app = Flask(__name__,
            static_url_path='',
            static_folder='build',
            template_folder='build')


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    q = request.args.get('q')
    if q:
        return jsonify(query(q))
    else:
        return jsonify([])


if __name__ == "__main__":
    '''
    In development, allow CORS requests so create-react-app
    can use hot reload and still hit us.
    '''
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
