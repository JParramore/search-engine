pip3 install -r requirements.txt
python3 crawler.py
npm install
npm run build
gunicorn --bind 0.0.0.0:80 --workers 4 server:app
