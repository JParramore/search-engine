pip install -r requirements.txt
python crawler.py
npm install
npm run build
gunicorn --bind 0.0.0.0:8080 --workers 4 server:app
