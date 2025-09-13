import requests

BASE_URL = "http://127.0.0.1:5000/items"

def fetch_page(page=1, per_page=10):
    """Fetch a single page of items."""
    params = {"page": page, "per_page": per_page}
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Error fetching page {page}")
        return []
    data = response.json()
    items = data.get("items", [])
    print(f"Page {page} fetched {len(items)} items")
    return items

# Interactive loop
current_page = 1
per_page = 10

while True:
    command = input("Enter command (n=next, p=prev, q=quit): ").strip().lower()
    if command == "n":
        current_page += 1
    elif command == "p" and current_page > 1:
        current_page -= 1
    elif command == "q":
        break
    else:
        print("Invalid command, use n, p, or q")
        continue

    items = fetch_page(current_page, per_page)
    for item in items:
        print(item)
    if not items:
        print("No more items to display.")
        current_page -= 1