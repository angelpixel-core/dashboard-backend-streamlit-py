---
id: dashboard-backend-streamlit-py
aliases: []
tags: []
---

# Dashboard Backend StreamLit Python

## Entrypoint Convention
This project uses `app.py` as the canonical Streamlit entrypoint.

Why `app.py` and not `main.py`:
- In Streamlit, the entrypoint is the file passed to `streamlit run`.
- Using `app.py` makes intent explicit for UI-first apps and avoids CLI confusion.

Run locally:
```sh
make dev
# or
python -m streamlit run app.py
```

## Setup Virtual Env
```sh
python -m venv .venv
```

## Env Activation
```
source .venv/bin/activate
```


## Reload Session
```sh
exec $SHELL
```

## Setup Package Manager
```sh
brew install uv
# uv init
```

## Setup Streamlit
```sh
uv add streamlit pandas plotly
```
