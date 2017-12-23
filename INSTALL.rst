How to start
===============

1. Get Telegram API keys. Do it here: https://my.telegram.org/apps

2. Insert the keys and the channel name in config.py (see config.py.example)

3. Create virtual environment::

    >> virtualenv -p python3 .venv
    >> source .venv/bin/activate
    >> pip3 install -r requirements.txt

4. Run the fetcher::

   >> python3 ./fetcher.py
