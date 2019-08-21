# tango-with-django

*Learning how to tango with Django... and Material Design!*

## About

This is a [Django](https://www.djangoproject.com/) web application for users to view, like and categorise resources for learning Python.
This project was built following the [Tango with Django](https://www.tangowithdjango.com/) guide, with the addition of Material Design using [MDC Web](https://material.io/develop/web).

## Getting Started

### Prerequisites

An installation of [Python](https://www.python.org/) version 3.5 or later is required to run the Django site locally.

An installation of [Node.js](https://nodejs.org) version 8 or later is required to build the MDC Web assets.

### Installation

Clone the source from this repository.

```shell
git clone https://github.com/martindes01/tango-with-django.git
cd tango-with-django
```

Create and activate a Python virtual environment, specifying a suitable path `<path>`.
A common name for the environment directory is `.venv`.

```shell
python3 -m venv <path>
source <path>/Scripts/activate
```

Install the Python dependencies listed in [requirements.txt](requirements.txt).

```shell
pip install --requirement requirements.txt
```

Install the Node.js production and development dependencies listed in [package.json](package.json).

```shell
npm install
```

## Usage

To compile the MDC Web assets, execute the `build` script.

```shell
npm run build
```

To create or update the database, execute the `makemigrations` and `migrate` commands of the `manage.py` script.
These commands create schema migrations based on changes to the models and apply these migrations to the database, respectively.

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

To run the site locally, execute the `runserver` command of the `manage.py` script, optionally specifying the local IP address `<address>` and port number `<port>`.
This will serve the site to `<address>:<port>`.
If unspecified, `<address>` defaults to `localhost` and `<port>` defaults to `8000`.

```shell
python3 manage.py runserver [[<address>:]<port>]
```

To populate the database with sample data, run the `populate_rango.py` script.

```shell
python3 populate_rango.py
```

To manage the database, execute the `createsuperuser` command of the `manage.py` script and follow the prompts.
This will create a superuser account with access to the administration interface at `<address>:<port>/admin/`.

```shell
python3 manage.py createsuperuser
```

To run the unit tests, execute the `test` command of the `manage.py` script.

```shell
python3 manage.py test
```

## License

This project is distributed under the terms of the MIT License.
See [LICENSE](LICENSE) for more information.
