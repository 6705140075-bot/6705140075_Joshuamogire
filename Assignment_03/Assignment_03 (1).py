import io
import contextlib

# ==============================================================================
# LEGACY STORE SYSTEM — unchanged
# ==============================================================================
PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]

TAXRATE = 0.07
foodtax = 0.0

ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]


def calc(o):
    global TAXRATE
    n = o[0]
    t = o[1]
    items = o[2]
    sub = 0.0
    tax = 0.0
    print("Receipt for " + n + " (" + t + ")")
    print("-" * 40)
    for it in items:
        pi = it[0]
        q = it[1]
        p = PRODUCTS[pi][1]
        nm = PRODUCTS[pi][0]
        cat = PRODUCTS[pi][2]
        line = p * q
        sub = sub + line
        if cat == "food":
            tax = tax + line * foodtax
        else:
            tax = tax + line * TAXRATE
        print(nm + " x" + str(q) + " = " + str(line))
    d = 0.0
    if t == "none":
        d = 0.0
    elif t == "silver":
        if sub > 100:
            d = sub * 0.05
        else:
            d = sub * 0.02
    elif t == "gold":
        if sub > 100:
            d = sub * 0.10
        else:
            d = sub * 0.05
    elif t == "platinum":
        if sub > 100:
            d = sub * 0.15
        else:
            d = sub * 0.10
    totalqty = 0
    for it in items:
        totalqty = totalqty + it[1]
    if totalqty >= 10:
        d = d + sub * 0.03
    total = sub - d + tax
    pts = 0
    if t == "none":
        pts = int(total // 10)
    elif t == "silver":
        pts = int(total // 10) * 2
    elif t == "gold":
        pts = int(total // 10) * 3
    elif t == "platinum":
        pts = int(total // 10) * 5
    print("-" * 40)
    print("Subtotal: " + str(round(sub, 2)))
    print("Discount: " + str(round(d, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(pts))
    print("")
    return total


def legacy_main():
    grand = 0.0
    for o in ORDERS:
        grand = grand + calc(o)
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


def capture(fn):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn()
    return buf.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)

# ==============================================================================
# REFACTORED SOLUTION
# ==============================================================================
TAX_RATE = 0.07
FOOD_CATEGORY = "food"
FOOD_TAX_RATE = 0.0
DISCOUNT_THRESHOLD = 100
BULK_QTY_THRESHOLD = 10
BULK_DISCOUNT_RATE = 0.03
POINTS_DIVISOR = 10


class Product:
    def __init__(self, name, price, category):
        if not name:
            raise ValueError("Product name cannot be empty")
        if price < 0:
            raise ValueError("Product price cannot be negative")
        if not category:
            raise ValueError("Product category cannot be empty")
        self.name = name
        self.price = price
        self.category = category

    def tax_rate(self):
        return FOOD_TAX_RATE if self.category == FOOD_CATEGORY else TAX_RATE


class OrderItem:
    def __init__(self, product, quantity):
        if not isinstance(product, Product):
            raise TypeError("product must be a Product")
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        self.product = product
        self.quantity = quantity

    def line_total(self):
        return self.product.price * self.quantity

    def tax_amount(self):
        return self.line_total() * self.product.tax_rate()


class Customer:
    def discount_rate(self, subtotal):
        return 0.0

    @property
    def points_multiplier(self):
        return 1

    @property
    def tier_name(self):
        return "none"


class SilverCustomer(Customer):
    @property
    def tier_name(self):
        return "silver"

    def discount_rate(self, subtotal):
        return 0.05 if subtotal > DISCOUNT_THRESHOLD else 0.02

    @property
    def points_multiplier(self):
        return 2


class GoldCustomer(Customer):
    @property
    def tier_name(self):
        return "gold"

    def discount_rate(self, subtotal):
        return 0.10 if subtotal > DISCOUNT_THRESHOLD else 0.05

    @property
    def points_multiplier(self):
        return 3


class PlatinumCustomer(Customer):
    @property
    def tier_name(self):
        return "platinum"

    def discount_rate(self, subtotal):
        return 0.15 if subtotal > DISCOUNT_THRESHOLD else 0.10

    @property
    def points_multiplier(self):
        return 5


class Order:
    def __init__(self, customer_name, customer, items):
        if not customer_name:
            raise ValueError("Customer name cannot be empty")
        if not isinstance(customer, Customer):
            raise TypeError("customer must be a Customer")
        if not items:
            raise ValueError("Order must contain items")
        self.customer_name = customer_name
        self.customer = customer
        self.items = items

    def subtotal(self):
        return sum(item.line_total() for item in self.items)

    def discount(self):
        subtotal = self.subtotal()
        discount = subtotal * self.customer.discount_rate(subtotal)
        total_quantity = sum(item.quantity for item in self.items)
        if total_quantity >= BULK_QTY_THRESHOLD:
            discount += subtotal * BULK_DISCOUNT_RATE
        return discount

    def tax(self):
        return sum(item.tax_amount() for item in self.items)

    def total(self):
        return self.subtotal() - self.discount() + self.tax()

    def points(self):
        return int(self.total() // POINTS_DIVISOR) * self.customer.points_multiplier

    def receipt(self):
        lines = [
            "Receipt for " + self.customer_name + " (" + self.customer.tier_name + ")",
            "-" * 40,
        ]
        for item in self.items:
            lines.append(
                item.product.name
                + " x"
                + str(item.quantity)
                + " = "
                + str(item.line_total())
            )
        lines.extend([
            "-" * 40,
            "Subtotal: " + str(round(self.subtotal(), 2)),
            "Discount: " + str(round(self.discount(), 2)),
            "Tax: " + str(round(self.tax(), 2)),
            "Total: " + str(round(self.total(), 2)),
            "Points earned: " + str(self.points()),
            "",
        ])
        return "\n".join(lines)


def customer_from_tier(tier):
    customer_types = {
        "none": Customer,
        "silver": SilverCustomer,
        "gold": GoldCustomer,
        "platinum": PlatinumCustomer,
    }
    if tier not in customer_types:
        raise ValueError("Unknown membership tier")
    return customer_types[tier]()


def build_products():
    return [
        Product(name, price, category)
        for name, price, category in PRODUCTS
    ]


def build_orders():
    products = build_products()
    orders = []
    for name, tier, raw_items in ORDERS:
        customer = customer_from_tier(tier)
        items = [
            OrderItem(products[index], quantity)
            for index, quantity in raw_items
        ]
        orders.append(Order(name, customer, items))
    return orders


def refactored_main():
    grand = 0.0
    for order in build_orders():
        print(order.receipt())
        grand += order.total()
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


def _check():
    try:
        your_output = capture(refactored_main)
    except NotImplementedError:
        print("Solution not implemented yet.\n")
        print("Below is the TARGET output your refactor must reproduce exactly:\n")
        print(GOLDEN_OUTPUT)
        return

    if your_output == GOLDEN_OUTPUT:
        print("PASS - behaviour is unchanged. Your refactor is safe.\n")
    else:
        print("FAIL - the output changed, so this is not yet a valid refactor.\n")
        g = GOLDEN_OUTPUT.splitlines()
        y = your_output.splitlines()
        for i in range(max(len(g), len(y))):
            gl = g[i] if i < len(g) else "<no line>"
            yl = y[i] if i < len(y) else "<no line>"
            if gl != yl:
                print("First difference at line " + str(i + 1) + ":")
                print("  expected: " + repr(gl))
                print("  yours:    " + repr(yl))
                break


if __name__ == "__main__":
    _check()
