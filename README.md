[![Python, Flask, etc.](https://github.com/JParramore/search-engine/workflows/Python%20application/badge.svg)](https://github.com/JParramore/search-engine/actions)
[![React](https://github.com/JParramore/search-engine/workflows/Node.js%20CI/badge.svg)](https://github.com/JParramore/search-engine/actions)

# search-engine

Ubtuntu 20.04 installation:

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