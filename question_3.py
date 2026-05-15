def add_item(item, cart=[]):
    cart.append(item)
    return cart


print(add_item("apple"))
print(add_item("banana"))
print(add_item("milk", cart=["bread"]))
print(add_item("eggs"))


def add_item_fixed(item, cart=None):
    if cart is None:
        cart = []

    cart.append(item)
    return cart


print(add_item_fixed("apple"))
print(add_item_fixed("banana"))


def create_cart(owner, discount=0):
    return {
        "owner": owner,
        "items": [],
        "discount": discount
    }


def add_to_cart(cart, name, price, qty=1):
    cart["items"].append({
        "name": name,
        "price": price,
        "qty": qty
    })


def update_price(price_tuple, new_price):
    try:
        price_tuple[0] = new_price
    except TypeError as e:
        print(e)


def calculate_total(cart):
    total = 0

    for item in cart["items"]:
        total += item["price"] * item["qty"]

    discount_amount = total * (cart["discount"] / 100)

    return total - discount_amount


cart1 = create_cart("Aarav", 10)
cart2 = create_cart("Riya", 5)

add_to_cart(cart1, "Laptop", 50000, 1)
add_to_cart(cart1, "Mouse", 1000, 2)

add_to_cart(cart2, "Phone", 30000, 1)
add_to_cart(cart2, "Charger", 1500, 1)

print(cart1)
print(cart2)

print("Total for Aarav:", calculate_total(cart1))
print("Total for Riya:", calculate_total(cart2))

price_data = (1000,)

update_price(price_data, 2000)


"""
discount=0 is safe because integers are immutable.

cart=[] is dangerous because lists are mutable and shared between function calls.

Rebinding means assigning a variable to a new object.
Mutating means changing the existing object.

Mutable:
list, dict, set

Immutable:
tuple, str, int

When a list is passed into a function and modified,
the changes reflect outside because lists are mutable
and passed by object reference.
"""