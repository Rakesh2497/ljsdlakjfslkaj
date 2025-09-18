# save as server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data
ITEMS = [
    {"id": i, "name": f"Item {i}"} for i in range(1, 51)  # 50 items
]

@app.route("/items", methods=["GET"])
def get_items():
    # Pagination parameters
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    # Calculate start and end indices
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = ITEMS[start:end]

    return jsonify({"items": paginated_items})

if __name__ == "__main__":
    app.run(debug=True)
