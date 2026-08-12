from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

# In-memory "database" for demo purposes
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
    {"id": 2, "name": "Bob",   "email": "bob@example.com",   "age": 25},
]

products = [
    {"id": 1, "name": "Laptop",     "price": 999.99,
        "category": "electronics", "stock": 10},
    {"id": 2, "name": "Coffee Mug", "price": 12.50,
        "category": "kitchen",     "stock": 50},
    {"id": 3, "name": "Notebook",   "price": 4.99,
        "category": "office",      "stock": 200},
    {"id": 4, "name": "Headphones", "price": 79.99,
        "category": "electronics", "stock": 25},
    {"id": 5, "name": "Desk Lamp",  "price": 24.99,
        "category": "office",      "stock": 15},
]

server_start_time = datetime.now(timezone.utc)

# Root route - lists available endpoints


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Postman Demo API is running!",
        "endpoints": {
            "GET    /users":              "Get all users",
            "GET    /users/<id>":         "Get a user by ID",
            "GET    /users/search?name=": "Search users by name",
            "POST   /users":              "Create a new user",
            "PUT    /users/<id>":         "Update a user",
            "DELETE /users/<id>":         "Delete a user",
            "GET    /products":           "Get all products",
            "GET    /products/<id>":      "Get a product by ID",
            "GET    /products/category/<cat>": "Get products by category",
            "POST   /products":           "Create a new product",
            "PUT    /products/<id>":      "Update a product",
            "DELETE /products/<id>":      "Delete a product",
            "GET    /health":             "Health check",
            "GET    /stats":              "API statistics",
        }
    }), 200

# GET all users


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# GET a single user by ID


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# POST - create a new user


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "name and email are required"}), 400
    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "name": data["name"],
        "email": data["email"],
    }
    users.append(new_user)
    return jsonify(new_user), 201

# PUT - update an existing user


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user.update({k: v for k, v in data.items() if k in ("name", "email")})
    return jsonify(user), 200

# DELETE - remove a user


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200


# --- Search users by name (query param) ---

@app.route("/users/search", methods=["GET"])
def search_users():
    name_query = request.args.get("name", "").lower()
    if not name_query:
        return jsonify({"error": "Provide a 'name' query parameter, e.g. /users/search?name=alice"}), 400
    results = [u for u in users if name_query in u["name"].lower()]
    return jsonify({"count": len(results), "results": results}), 200

# --- Products CRUD ---


@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get("category")
    if category:
        filtered = [p for p in products if p["category"].lower() ==
                    category.lower()]
        return jsonify({"count": len(filtered), "results": filtered}), 200
    return jsonify(products), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@app.route("/products/category/<string:category>", methods=["GET"])
def get_products_by_category(category):
    results = [p for p in products if p["category"].lower() ==
               category.lower()]
    return jsonify({"category": category, "count": len(results), "results": results}), 200


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    required = ["name", "price", "category", "stock"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Required fields: {', '.join(required)}"}), 400
    new_product = {
        "id": products[-1]["id"] + 1 if products else 1,
        "name": data["name"],
        "price": float(data["price"]),
        "category": data["category"],
        "stock": int(data["stock"]),
    }
    products.append(new_product)
    return jsonify(new_product), 201


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.get_json()
    for k, v in data.items():
        if k in ("name", "price", "category", "stock"):
            product[k] = type(product[k])(v) if k in ("price", "stock") else v
    return jsonify(product), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    global products
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    products = [p for p in products if p["id"] != product_id]
    return jsonify({"message": f"Product {product_id} deleted"}), 200

# --- Health check ---


@app.route("/health", methods=["GET"])
def health_check():
    uptime = datetime.now(timezone.utc) - server_start_time
    return jsonify({
        "status": "healthy",
        "uptime_seconds": round(uptime.total_seconds(), 2),
        "users_count": len(users),
        "products_count": len(products),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), 200

# --- API statistics ---


@app.route("/stats", methods=["GET"])
def stats():
    total_stock_value = sum(p["price"] * p["stock"] for p in products)
    categories = {}
    for p in products:
        cat = p["category"]
        categories[cat] = categories.get(cat, 0) + 1
    avg_user_age = sum(u.get("age", 0)
                       for u in users) / len(users) if users else 0
    return jsonify({
        "users": {
            "total": len(users),
            "average_age": round(avg_user_age, 2),
        },
        "products": {
            "total": len(products),
            "total_stock_value": round(total_stock_value, 2),
            "by_category": categories,
        },
    }), 200


if __name__ == "__main__":
    print("API running at http://127.0.0.1:8000")
    app.run(debug=True, port=8000)
