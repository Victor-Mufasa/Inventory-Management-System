from flask import Flask, request, jsonify
import openfoodfacts

app = Flask(__name__)

# Create the OpenFoodFacts client once
off_api = openfoodfacts.API(user_agent="SummativeLab/1.0")

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "barcode": "0025293000003",
        "price": 4.99,
        "stock": 25,
    },
    {
        "id": 2,
        "product_name": "Peanut Butter",
        "brands": "Jif",
        "barcode": "0051500250017",
        "price": 3.49,
        "stock": 40,
    },
    {
        "id": 3,
        "product_name": "Whole Wheat Bread",
        "brands": "Dave's Killer Bread",
        "barcode": "0013764000008",
        "price": 5.99,
        "stock": 15,
    },
]


@app.route("/inventory", methods=["GET"])
def get_all():
    return jsonify(inventory), 200


@app.route("/inventory/<int:id>", methods=["GET"])
def get_one(id):
    item = next((i for i in inventory if i["id"] == id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def create():
    data = request.get_json()

    # Check required fields
    if "product_name" not in data or "price" not in data or "stock" not in data:
        return jsonify({"error": "product_name, price, stock are required"}), 400

    new_id = max([i["id"] for i in inventory], default=0) + 1
    new_item = {
        "id": new_id,
        "product_name": data["product_name"],
        "brands": data.get("brands", ""),
        "barcode": data.get("barcode", ""),
        "price": data["price"],
        "stock": data["stock"],
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


@app.route("/inventory/<int:id>", methods=["PATCH"])
def update(id):
    data = request.get_json()
    item = next((i for i in inventory if i["id"] == id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Update whatever fields were sent
    for key in ["product_name", "brands", "barcode", "price", "stock"]:
        if key in data:
            item[key] = data[key]

    return jsonify(item), 200


@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete(id):
    global inventory
    item = next((i for i in inventory if i["id"] == id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory = [i for i in inventory if i["id"] != id]
    return jsonify({"message": f"Item {id} deleted"}), 200


# ---------- SEARCH on OpenFoodFacts ----------
@app.route("/inventory/search", methods=["GET"])
def search():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({"error": "Provide ?barcode= or ?name="}), 400

    try:
        if barcode:
            # SDK returns flat dict, e.g. {"code": "...", "product_name": "..."}
            result = off_api.product.get(barcode, fields=["code", "product_name", "brands"])
            if not result or result.get("status") == 0:
                return jsonify({"error": "Product not found"}), 404
            return jsonify({"status": 1, "product": result}), 200

        else:
            # Search returns {"count": N, "products": [...]}
            result = off_api.product.text_search(name, page_size=1)
            products = result.get("products", [])
            if not products:
                return jsonify({"error": "Product not found"}), 404
            return jsonify({"status": 1, "product": products[0]}), 200

    except Exception:
        return jsonify({"error": "OpenFoodFacts failed"}), 404


@app.route("/inventory/import", methods=["POST"])
def import_item():
    data = request.get_json()
    barcode = data.get("barcode")

    if not barcode:
        return jsonify({"error": "barcode is required"}), 400

    try:
        result = off_api.product.get(barcode, fields=["code", "product_name", "brands"])
        if not result or result.get("status") == 0:
            return jsonify({"error": "Product not found on OpenFoodFacts"}), 404
    except Exception:
        return jsonify({"error": "OpenFoodFacts failed"}), 404

    new_id = max([i["id"] for i in inventory], default=0) + 1
    new_item = {
        "id": new_id,
        "product_name": result.get("product_name", "Unknown"),
        "brands": result.get("brands", ""),
        "barcode": result.get("code", ""),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)