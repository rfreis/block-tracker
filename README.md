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
make test
```

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
