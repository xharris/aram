# ARAM

## setup

```
python -m venv env
pip install -r requirements.txt
```

Create an .env file

```
RIOT_API_KEY=<your-api-key>
```

`py main.py`

## notes

- when using `lol.arams(id, max=300)`, the larger `max` is, the longer it will take to complete due to the `RATE_LIMIT` set in lol.py. If you're using a fully registered project api key, you can tweak `RATE_LIMIT` to make stuff faster.
