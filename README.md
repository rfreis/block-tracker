![GitHub](https://img.shields.io/github/license/rfreis/block-tracker)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/rfreis/block-tracker)
[![CI](https://github.com/rfreis/block-tracker/actions/workflows/ci.yaml/badge.svg)](https://github.com/rfreis/block-tracker/actions/workflows/ci.yaml)
[![Coverage](https://img.shields.io/codecov/c/github/rfreis/block-tracker/main.svg)](https://codecov.io/github/rfreis/block-tracker?branch=main)
![GitHub Repo stars](https://img.shields.io/github/stars/rfreis/block-tracker)

# Block Tracker

This repository runs with `Django 4.1` on `Docker`, `docker-compose` and `postgresql`.

## Supported protocols

Initially it supports only Bitcoin with P2PKH/P2WPKH addresses. The project aims to support multiple assets in multiple protocols.

## Requirements

To make this run you must have installed:

* docker
* docker-compose

## Formatting

To run black before commiting, install `pre-commit`:

```bash
make pre-commit-install
```

## Running application

```bash
make start-local
```

## Stopping application

```bash
make stop
```

## Local bash

```bash
make local-bash
```

## Logs

```bash
make logs
```

## Tests

```bash
make test # shortcut to e2e and unit tests
make unit
make e2e
make integration
```

# Emails

We use [mailhog](https://github.com/mailhog/MailHog) to display the emails sent by SMTP on development server.

The emails sent to SMTP server on `localhost:1025` gets available on [localhost:8025](http://localhost:8025).

## Workers

### Blockbook websocket

```bash
python manage.py wss_blockbook <ProtocolType attribute>
python manage.py wss_blockbook BITCOIN
python manage.py wss_blockbook BITCOIN_TESTNET
```

### Celery background worker

```bash
python -m celery -A app worker
```
