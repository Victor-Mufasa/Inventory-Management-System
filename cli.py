import requests

BASE = "http://127.0.0.1:5555"


def view_all():
    response = requests.get(f"{BASE}/inventory")
    for item in response.json():
        print(f"  ID {item['id']}: {item['product_name']} - ${item['price']} ({item['stock']} in stock)")


def view_one():
    item_id = input("Item ID: ")
    response = requests.get(f"{BASE}/inventory/{item_id}")
    print(response.json())


def add_item():
    name = input("Product name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    response = requests.post(f"{BASE}/inventory", json={
        "product_name": name,
        "price": price,
        "stock": stock,
    })
    print(response.json())


def update_item():
    item_id = input("Item ID to update: ")
    price = input("New price (blank to skip): ")
    stock = input("New stock (blank to skip): ")

    data = {}
    if price:
        data["price"] = float(price)
    if stock:
        data["stock"] = int(stock)

    response = requests.patch(f"{BASE}/inventory/{item_id}", json=data)
    print(response.json())


def delete_item():
    item_id = input("Item ID to delete: ")
    response = requests.delete(f"{BASE}/inventory/{item_id}")
    print(response.json())


def search_off():
    mode = input("Search by (1) name or (2) barcode: ")

    if mode == "1":
        name = input("Name: ")
        response = requests.get(f"{BASE}/inventory/search", params={"name": name})
    else:
        barcode = input("Barcode: ")
        response = requests.get(f"{BASE}/inventory/search", params={"barcode": barcode})

    print(response.json())

    if response.status_code == 200 and input("Add to inventory? (y/n): ") == "y":
        price = float(input("Price: "))
        stock = int(input("Stock: "))
        barcode = response.json()["product"]["code"]
        response = requests.post(f"{BASE}/inventory/import", json={
            "barcode": barcode,
            "price": price,
            "stock": stock,
        })
        print(response.json())


def main():
    while True:
        print("\n1. View all   2. View one   3. Add   4. Update   5. Delete   6. Search OFF   0. Exit")
        choice = input("Choice: ")

        if choice == "1":
            view_all()
        elif choice == "2":
            view_one()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_off()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()