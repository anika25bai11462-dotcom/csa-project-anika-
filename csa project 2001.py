import datetime

class MenuItem:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

class Order:
    def __init__(self, table_number):
        self.table_number = table_number
        self.items = {}  # Changed to dict: {MenuItem: quantity}
        self.status = "Open"
        self.timestamp = datetime.datetime.now()

    def add_item(self, menu_item, qty):
        if menu_item in self.items:
            self.items[menu_item] += qty
        else:
            self.items[menu_item] = qty
        print(f"✔ Added {qty}x {menu_item.name} to Table {self.table_number}")

    def calculate_total(self, tax_rate=0.08):
        subtotal = sum(item.price * qty for item, qty in self.items.items())
        tax = subtotal * tax_rate
        return subtotal, tax, subtotal + tax

class RestaurantManager:
    def __init__(self):
        self.menu = []
        self.orders = {}
        self.total_revenue = 0.0  # Tracking daily sales

    def add_menu_item(self, name, price, category):
        self.menu.append(MenuItem(name, price, category))

    def show_menu(self):
        print(f"\n{'--- BISTRO MENU ---':^40}")
        categories = sorted(set(item.category for item in self.menu))
        for cat in categories:
            print(f"\n[{cat.upper()}]")
            for item in self.menu:
                if item.category == cat:
                    print(f" > {item.name:<20} ${item.price:>6.2f}")

    def find_item(self, name):
        """Helper to find item by name string"""
        for item in self.menu:
            if item.name.lower() == name.lower():
                return item
        return None

    def generate_receipt(self, table_num):
        if table_num not in self.orders:
            print("❌ No active order for this table.")
            return

        order = self.orders[table_num]
        sub, tax, total = order.calculate_total()
        self.total_revenue += total # Add to daily sales
        
        print("\n" + "="*40)
        print(f"{'PYTHON BISTRO':^40}")
        print(f"Table: {table_num:<10} | {order.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print("-" * 40)
        for item, qty in order.items.items():
            line_total = item.price * qty
            print(f"{qty:>2}x {item.name:<22} ${line_total:>8.2f}")
        print("-" * 40)
        print(f"{'Subtotal:':<28} ${sub:>8.2f}")
        print(f"{'Tax (8%):':<28} ${tax:>8.2f}")
        print(f"{'TOTAL:':<28} ${total:>8.2f}")
        print(f"{'THANK YOU!':^40}")
        print("="*40 + "\n")
        
        del self.orders[table_num] # Clear table after payment

# --- Main Application Loop ---
def main():
    bistro = RestaurantManager()
    # Initial Menu Setup
    bistro.add_menu_item("Cheeseburger", 12.50, "Mains")
    bistro.add_menu_item("Veggie Pizza", 15.00, "Mains")
    bistro.add_menu_item("Truffle Fries", 6.50, "Sides")
    bistro.add_menu_item("Garden Salad", 8.00, "Sides")
    bistro.add_menu_item("Iced Tea", 3.00, "Drinks")
    bistro.add_menu_item("Craft Beer", 7.00, "Drinks")

    while True:
        print("\n" + "█"*40)
        print("  MAIN TERMINAL - SELECT OPTION")
        print("  1. View Menu\n  2. New/Update Order\n  3. Checkout Table\n  4. Manager Dashboard\n  5. Exit")
        choice = input("Select: ")

        if choice == "1":
            bistro.show_menu()

        elif choice == "2":
            try:
                t_num = int(input("Table Number: "))
                if t_num not in bistro.orders:
                    bistro.orders[t_num] = Order(t_num)
                
                while True:
                    item_name = input("Enter Item Name (or 'done'): ")
                    if item_name.lower() == 'done': break
                    
                    item = bistro.find_item(item_name)
                    if item:
                        qty = int(input(f"How many {item.name}s?: "))
                        bistro.orders[t_num].add_item(item, qty)
                    else:
                        print("❌ Item not found. Check spelling!")
            except ValueError:
                print("❌ Invalid input. Please use numbers for table/quantity.")

        elif choice == "3":
            try:
                t_num = int(input("Enter Table Number to Bill: "))
                bistro.generate_receipt(t_num)
            except ValueError:
                print("❌ Invalid table number.")

        elif choice == "4":
            print(f"\n--- MANAGER DASHBOARD ---")
            print(f"Active Tables: {len(bistro.orders)}")
            print(f"Total Daily Revenue: ${bistro.total_revenue:.2f}")

        elif choice == "5":
            print("System shutting down...")
            break

if __name__ == "__main__":
    main()
