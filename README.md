# Inventory Management System

A simple Flask REST API for managing retail inventory, with a command-line interface (CLI) and OpenFoodFacts integration.

Built as a summative lab for the Python REST API module.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Project Installation](#project-installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [CURL Requests](#curl-requests)
- [Running Tests](#running-the-tests)
- [External API](#external-api--openfoodfacts)
- [Contact](#contact)
- [License](#license)

## Features

- Full CRUD operations on inventory items (Create, Read, Update, Delete)
- Fetch product details from OpenFoodFacts by barcode or product name
- Import products from OpenFoodFacts directly into inventory
- Interactive CLI menu to talk to the API
- Unit tests with pytest (external API calls are mocked)
- In-memory storage using a simple Python list

## Project Structure

```text
Inventory-Management-System/
├── app.py # Flask API with all routes
├── cli.py # Command-line interface
├── LICENSE # MIT License
├── requirements.txt # Dependencies
├── README.md # This file
└── .gitignore # Ignored files (venv, caches)
```

## Project Installation

### Creating the virtual environment

```bash
python -m venv venv
```

### Activating the virtual environment

```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Installing dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Project

### Start the API

In Terminal 1 (with venv activated):

```bash
python app.py
```

The server runs at http://127.0.0.1:5555.

### Run the CLI

In Terminal 2 (with venv activated):

```bash
python cli.py
```

You'll see a menu:

```text
1. View all   2. View one   3. Add   4. Update   5. Delete   6. Search OFF   0. Exit
```

Note: If you change the port in app.py, update BASE in cli.py to match.

## API Endpoints

GET	/inventory - Get all items

GET	/inventory/<id> - Get a single item

POST	/inventory - Add a new item

PATCH	/inventory/<id> - Update an item

DELETE	/inventory/<id> - Delete an item

GET	/inventory/search?barcode=... - Look up a product on OpenFoodFacts by barcode

GET	/inventory/search?name=... - Search OpenFoodFacts by name

POST	/inventory/import - Import a product from OpenFoodFacts into inventory

## CURL requests

Get all items:

```bash
curl http://127.0.0.1:5555/inventory
```

Get one Item:

```bash
curl http://127.0.0.1:5555/inventory/1
```

Create a new item:

```bash
curl -X POST http://127.0.0.1:5555/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name":"Oat Milk","price":3.99,"stock":20}'
```

Update an item:

```bash
curl -X PATCH http://127.0.0.1:5555/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price":9.99}'
```

Delete an item:

```bash
curl -X DELETE http://127.0.0.1:5555/inventory/2
```

Search OpenFoodFacts by barcode:

```bash
curl "http://127.0.0.1:5555/inventory/search?barcode=3017620422003"
```

Search OpenFoodFacts by name:

```bash
curl "http://127.0.0.1:5555/inventory/search?name=nutella"
```

Import a product from OpenFoodFacts:

```bash
curl -X POST http://127.0.0.1:5555/inventory/import \
  -H "Content-Type: application/json" \
  -d '{"barcode":"3017620422003","price":6.99,"stock":12}'
```

## External API — OpenFoodFacts

The project uses the [official OpenFoodFacts Python SDK](https://github.com/openfoodfacts/openfoodfacts-python)

```bash
import openfoodfacts

off_api = openfoodfacts.API(user_agent="InventoryLab/1.0 (student@example.com)")
```

- The SDK requires a User-Agent string — it is set once in app.py.

Two SDK methods are used:

off_api.product.get(code, fields=[...]) — look up a product by barcode

off_api.product.text_search(query) — search products by name

If OpenFoodFacts is unreachable or returns no result, the API responds with a clean JSON error (HTTP 404) — the app never crashes.

Note: Search and import endpoints require an internet connection. If OpenFoodFacts is temporarily down, the API returns a JSON error and the rest of the app (CRUD, CLI, tests) continues to work normally.

## Contact

Feel free to reach out to <rickvick142@gmail.com> or <victorkipkemboi241@gmail.com>

## License

MIT License

Copyright © 2026 Victor Kipkemboi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
