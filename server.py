import time
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
        start = time.time()
        results = query(q.lower())
        t = (time.time() - start) / 1000
        t = f'{t/1000:.4}' if t > 0.0001 else '~0'
        return jsonify(
            {
                'results': results,
                'stats': f'{len(results)} results found in {t}ms'
            }
        )
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
