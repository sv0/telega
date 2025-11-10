# Telega v. 0.0.1

[![Python application](https://github.com/sv0/telega/actions/workflows/python-app.yml/badge.svg)](https://github.com/sv0/telega/actions/workflows/python-app.yml)

API to check if phone number is connected to Telegram account.

Inspired by [bellingcat telegram-phone-number-checker](https://github.com/bellingcat/telegram-phone-number-checker)

## Install

Install Python requirements

```shell

    apt-get install python3-venv

```

Clone the repository

```shell

    git clone https://github.com/sv0/telega.git
    cd telega

```

Create and activate Python virtual environment

```shell

    python3 -m vevv .venv
    source .venv/bin/activate

```

Install required Python packages within virtual environment

```shell

    pip install --requirement requirements.txt

```

## Usage

```shell

    uvicorn telega.app:app

```
