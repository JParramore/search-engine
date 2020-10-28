[![Python, Flask, etc.](https://github.com/JParramore/search-engine/workflows/Python%20application/badge.svg)](https://github.com/JParramore/search-engine/actions)
[![React](https://github.com/JParramore/search-engine/workflows/Node.js%20CI/badge.svg)](https://github.com/JParramore/search-engine/actions)

# search-engine

This project allows users to search technical blogs!

<br>

There are three core modules:

- `crawler.py` — a web crawler that utilizes the `requests` module to crawl entire websites from a seed file in `db/seed.yaml`

- `indexer.py` — an indexer which exports functionality to store websites in an SQLite database with efficient indexing

- `query.py` — a query module which, given a search term, retrieves and ranks websites by three heuristics (frequency, location, distance)


<br>

A Flask application in `server.py` serves a React application that allows users to interact with the project.

<br>

## Preview

![An image of search results for 'C99'](https://github.com/JParramore/search-engine/blob/master/public/preview.png)

<br>

## Ubtuntu 20.04 installation

```bash
sudo ufw enable
sudo ufw allow 8080
sudo apt update
sudo apt install gunicorn
sudo apt install python3-pip
pip3 install -r requirements.txt
bash setup.sh
```

Run:

```bash
bash start.sh
```