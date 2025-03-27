# Discord-Bot

## Environment File
```bash
touch .env

Fill with the following environment variables.
DB_USER=""
DB_PASSWORD=""
DB_HOST=""
DB_PORT=""
DB_DB=""
TOKEN=""
```

## Setup Python Application
```bash
sudo apt install python3-dev python3.12-venv libpq-dev gcc
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## Postgres Vector Extension Setup
https://github.com/pgvector/pgvector
```bash
sudo apt install postgresql-server-dev-16
cd /tmp
git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

## Ollama Setup
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
ollama serve
```