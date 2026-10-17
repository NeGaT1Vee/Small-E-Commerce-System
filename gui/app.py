import tkinter as tk
from tkinter import ttk, messagebox

from exceptions import ValidationError
from models.category import Category
from models.customer import Customer
from models.product import Product
from store.store import Store
from file_manager.file_manager import FileManager

# the kinds of error our classes raise when something is invalid
ERRORS = (ValidationError, ValueError, TypeError)


class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-commerce Store")
        self.root.geometry("950x620")

        # load saved data (starts empty the first time)
        self.fm = FileManager("data")
        try:
            self.store = self.fm.load_store()
        except ERRORS as error:
            messagebox.showerror("Could not load data", str(error))
            self.store = Store([], [], [])

        # tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.categories_tab = ttk.Frame(notebook)
        self.products_tab = ttk.Frame(notebook)
        self.customers_tab = ttk.Frame(notebook)
        self.shop_tab = ttk.Frame(notebook)
        self.orders_tab = ttk.Frame(notebook)
        self.dashboard_tab = ttk.Frame(notebook)

        notebook.add(self.categories_tab, text="Categories")
        notebook.add(self.products_tab, text="Products")
        notebook.add(self.customers_tab, text="Customers")
        notebook.add(self.shop_tab, text="Shop / Cart")
        notebook.add(self.orders_tab, text="Orders")
        notebook.add(self.dashboard_tab, text="Dashboard")

        self.build_categories_tab()
        self.build_products_tab()
        self.build_customers_tab()
        self.build_shop_tab()
        self.build_orders_tab()
        self.build_dashboard_tab()

        # save button at the bottom
        bottom = ttk.Frame(self.root)
        bottom.pack(fill="x", padx=5, pady=5)
        ttk.Button(bottom, text="Save data", command=self.save_data).pack(side="right")

        self.refresh_all()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ------------------------------------------------------------
    # small helpers
    # ------------------------------------------------------------
    def show_error(self, error):
        messagebox.showerror("Error", str(error))

    def make_tree(self, parent, columns, widths):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)
        for i in range(len(columns)):
            tree.heading(columns[i], text=columns[i])
            tree.column(columns[i], width=widths[i])
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        return tree

    def clear_tree(self, tree):
        for row in tree.get_children():
            tree.delete(row)

    def clear_entries(self, entries):
        for entry in entries:
            entry.delete(0, tk.END)

    # ------------------------------------------------------------
    # categories tab
    # ------------------------------------------------------------
    def build_categories_tab(self):
        form = ttk.Frame(self.categories_tab)
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="ID:").grid(row=0, column=0, padx=3)
        self.cat_id_entry = ttk.Entry(form, width=15)
        self.cat_id_entry.grid(row=0, column=1, padx=3)

        ttk.Label(form, text="Name:").grid(row=0, column=2, padx=3)
        self.cat_name_entry = ttk.Entry(form, width=25)
        self.cat_name_entry.grid(row=0, column=3, padx=3)

        ttk.Button(form, text="Add category", command=self.add_category).grid(row=0, column=4, padx=5)

        self.categories_tree = self.make_tree(
            self.categories_tab, ("ID", "Name", "Products"), (120, 300, 100))

    def add_category(self):
        try:
            category = Category(self.cat_id_entry.get(), self.cat_name_entry.get())
            self.store.add_category(category)
        except ERRORS as error:
            self.show_error(error)
            return
        self.clear_entries([self.cat_id_entry, self.cat_name_entry])
        self.refresh_all()

    def refresh_categories(self):
        self.clear_tree(self.categories_tree)
        products = self.store.products
        for category in self.store.categories:
            self.categories_tree.insert("", "end", values=(
                category.category_id, category.name, category.count_products(products)))

    # ------------------------------------------------------------
    # products tab
    # ------------------------------------------------------------
    def build_products_tab(self):
        # search row
        search_row = ttk.Frame(self.products_tab)
        search_row.pack(fill="x", padx=5, pady=5)
        ttk.Label(search_row, text="Search:").pack(side="left")
        self.search_entry = ttk.Entry(search_row, width=25)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_row, text="Search", command=self.search_products).pack(side="left")
        ttk.Button(search_row, text="Show all", command=self.refresh_products).pack(side="left", padx=5)

        self.products_tree = self.make_tree(
            self.products_tab, ("ID", "Name", "Price", "Stock", "Category"),
            (80, 250, 100, 80, 180))

        # add product form
        form = ttk.LabelFrame(self.products_tab, text="Add product")
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="ID:").grid(row=0, column=0, padx=3, pady=3)
        self.prod_id_entry = ttk.Entry(form, width=10)
        self.prod_id_entry.grid(row=0, column=1, padx=3)

        ttk.Label(form, text="Name:").grid(row=0, column=2, padx=3)
        self.prod_name_entry = ttk.Entry(form, width=20)
        self.prod_name_entry.grid(row=0, column=3, padx=3)

        ttk.Label(form, text="Price:").grid(row=0, column=4, padx=3)
        self.prod_price_entry = ttk.Entry(form, width=10)
        self.prod_price_entry.grid(row=0, column=5, padx=3)

        ttk.Label(form, text="Stock:").grid(row=1, column=0, padx=3, pady=3)
        self.prod_stock_entry = ttk.Entry(form, width=10)
        self.prod_stock_entry.grid(row=1, column=1, padx=3)

        ttk.Label(form, text="Category:").grid(row=1, column=2, padx=3)
        self.prod_category_combo = ttk.Combobox(form, width=25, state="readonly")
        self.prod_category_combo.grid(row=1, column=3, padx=3)

        ttk.Button(form, text="Add product", command=self.add_product).grid(row=1, column=5, padx=5)

    def add_product(self):
        category_text = self.prod_category_combo.get()
        if category_text == "":
            messagebox.showerror("Error", "Choose a category first (add one in the Categories tab)")
            return
        category_id = category_text.split(" - ")[0]

        category = None
        for item in self.store.categories:
            if item.category_id == category_id:
                category = item

        try:
            price = float(self.prod_price_entry.get())
            stock = int(self.prod_stock_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and stock a whole number")
            return

        try:
            product = Product(self.prod_id_entry.get(), self.prod_name_entry.get(),
                              price, stock, category)
            self.store.add_product(product)
        except ERRORS as error:
            self.show_error(error)
            return

        self.clear_entries([self.prod_id_entry, self.prod_name_entry,
                            self.prod_price_entry, self.prod_stock_entry])
        self.refresh_all()

    def search_products(self):
        results = self.store.search_products(self.search_entry.get())
        self.refresh_products(results)

    def refresh_products(self, products=None):
        if products is None:
            products = self.store.products
        self.clear_tree(self.products_tree)
        for product in products:
            self.products_tree.insert("", "end", values=(
                product.product_id, product.name, format(product.price, ".2f"),
                product.stock, product.category.name))

    # ------------------------------------------------------------
    # customers tab
    # ------------------------------------------------------------
    def build_customers_tab(self):
        form = ttk.LabelFrame(self.customers_tab, text="Add customer")
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="ID:").grid(row=0, column=0, padx=3, pady=3)
        self.cust_id_entry = ttk.Entry(form, width=10)
        self.cust_id_entry.grid(row=0, column=1, padx=3)

        ttk.Label(form, text="Name:").grid(row=0, column=2, padx=3)
        self.cust_name_entry = ttk.Entry(form, width=20)
        self.cust_name_entry.grid(row=0, column=3, padx=3)

        ttk.Label(form, text="Email:").grid(row=1, column=0, padx=3, pady=3)
        self.cust_email_entry = ttk.Entry(form, width=25)
        self.cust_email_entry.grid(row=1, column=1, columnspan=2, padx=3)

        ttk.Label(form, text="Phone:").grid(row=1, column=3, padx=3)
        self.cust_phone_entry = ttk.Entry(form, width=15)
        self.cust_phone_entry.grid(row=1, column=4, padx=3)

        ttk.Button(form, text="Add customer", command=self.add_customer).grid(row=1, column=5, padx=5)

        self.customers_tree = self.make_tree(
            self.customers_tab, ("ID", "Name", "Email", "Phone"), (80, 200, 250, 150))

    def add_customer(self):
        try:
            customer = Customer(self.cust_id_entry.get(), self.cust_name_entry.get(),
                                self.cust_email_entry.get(), self.cust_phone_entry.get())
            self.store.add_customer(customer)
        except ERRORS as error:
            self.show_error(error)
            return
        self.clear_entries([self.cust_id_entry, self.cust_name_entry,
                            self.cust_email_entry, self.cust_phone_entry])
        self.refresh_all()

    def refresh_customers(self):
        self.clear_tree(self.customers_tree)
        for customer in self.store.customers:
            self.customers_tree.insert("", "end", values=(
                customer.customer_id, customer.name, customer.email, customer.phone))

    # ------------------------------------------------------------
    # shop / cart tab
    # ------------------------------------------------------------
    def build_shop_tab(self):
        top = ttk.Frame(self.shop_tab)
        top.pack(fill="x", padx=5, pady=5)

        ttk.Label(top, text="Customer:").grid(row=0, column=0, padx=3, pady=3)
        self.customer_combo = ttk.Combobox(top, width=25, state="readonly")
        self.customer_combo.grid(row=0, column=1, padx=3)
        self.customer_combo.bind("<<ComboboxSelected>>", self.on_customer_selected)

        ttk.Label(top, text="Product:").grid(row=1, column=0, padx=3, pady=3)
        self.product_combo = ttk.Combobox(top, width=25, state="readonly")
        self.product_combo.grid(row=1, column=1, padx=3)

        ttk.Label(top, text="Quantity:").grid(row=1, column=2, padx=3)
        self.qty_entry = ttk.Entry(top, width=6)
        self.qty_entry.insert(0, "1")
        self.qty_entry.grid(row=1, column=3, padx=3)

        ttk.Button(top, text="Add to cart", command=self.add_to_cart).grid(row=1, column=4, padx=5)

        self.cart_tree = self.make_tree(
            self.shop_tab, ("Product", "Price", "Quantity", "Subtotal"), (250, 100, 100, 120))

        cart_buttons = ttk.Frame(self.shop_tab)
        cart_buttons.pack(fill="x", padx=5)
        ttk.Button(cart_buttons, text="Remove selected", command=self.remove_from_cart).pack(side="left")
        self.cart_total_label = ttk.Label(cart_buttons, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.cart_total_label.pack(side="right")

        pay = ttk.LabelFrame(self.shop_tab, text="Payment")
        pay.pack(fill="x", padx=5, pady=8)

        self.payment_var = tk.StringVar(value="card")
        ttk.Radiobutton(pay, text="Card", variable=self.payment_var, value="card").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(pay, text="Cash", variable=self.payment_var, value="cash").grid(row=0, column=1, padx=5)
        ttk.Label(pay, text="Card last 4 digits:").grid(row=0, column=2, padx=5)
        self.card_entry = ttk.Entry(pay, width=8)
        self.card_entry.grid(row=0, column=3, padx=3)
        ttk.Button(pay, text="Checkout", command=self.checkout).grid(row=0, column=4, padx=15)

    def get_selected_customer(self):
        text = self.customer_combo.get()
        if text == "":
            return None
        customer_id = text.split(" - ")[0]
        for customer in self.store.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def on_customer_selected(self, event):
        self.refresh_cart()

    def add_to_cart(self):
        customer = self.get_selected_customer()
        product_text = self.product_combo.get()
        if customer is None or product_text == "":
            messagebox.showerror("Error", "Choose a customer and a product")
            return
        product_id = product_text.split(" - ")[0]

        try:
            quantity = int(self.qty_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a whole number")
            return

        try:
            self.store.add_to_cart(customer.customer_id, product_id, quantity)
        except ERRORS as error:
            self.show_error(error)
            return
        self.refresh_cart()

    def remove_from_cart(self):
        customer = self.get_selected_customer()
        selected = self.cart_tree.selection()
        if customer is None or len(selected) == 0:
            messagebox.showerror("Error", "Select a cart line to remove")
            return
        index = int(selected[0])
        item = customer.cart.items[index]
        try:
            customer.cart.remove_item(item)
        except ERRORS as error:
            self.show_error(error)
            return
        self.refresh_cart()

    def refresh_cart(self):
        self.clear_tree(self.cart_tree)
        customer = self.get_selected_customer()
        if customer is None:
            self.cart_total_label.config(text="Total: $0.00")
            return
        index = 0
        for item in customer.cart.items:
            self.cart_tree.insert("", "end", iid=str(index), values=(
                item.product.name, format(item.product.price, ".2f"),
                item.quantity, format(item.subtotal(), ".2f")))
            index += 1
        self.cart_total_label.config(text="Total: $" + format(customer.cart.total(), ".2f"))

    def checkout(self):
        customer = self.get_selected_customer()
        if customer is None:
            messagebox.showerror("Error", "Choose a customer first")
            return

        try:
            if self.payment_var.get() == "card":
                order = self.store.checkout(customer.customer_id, "card",
                                            card_last4=self.card_entry.get())
            else:
                order = self.store.checkout(customer.customer_id, "cash")
        except ERRORS as error:
            self.show_error(error)
            return

        messagebox.showinfo("Order placed",
                            "Order " + order.order_id + " is paid.\nTotal: $" +
                            format(order.total(), ".2f"))
        self.card_entry.delete(0, tk.END)
        self.refresh_all()

    def refresh_combos(self):
        customer_values = []
        for customer in self.store.customers:
            customer_values.append(customer.customer_id + " - " + customer.name)
        self.customer_combo["values"] = customer_values

        product_values = []
        for product in self.store.products:
            product_values.append(product.product_id + " - " + product.name)
        self.product_combo["values"] = product_values

        category_values = []
        for category in self.store.categories:
            category_values.append(category.category_id + " - " + category.name)
        self.prod_category_combo["values"] = category_values

    # ------------------------------------------------------------
    # orders tab
    # ------------------------------------------------------------
    def build_orders_tab(self):
        self.orders_tree = self.make_tree(
            self.orders_tab, ("Order ID", "Customer", "Date", "Status", "Total"),
            (120, 120, 120, 120, 120))
        ttk.Button(self.orders_tab, text="Cancel selected order",
                   command=self.cancel_order).pack(anchor="w", padx=5, pady=5)

    def cancel_order(self):
        selected = self.orders_tree.selection()
        if len(selected) == 0:
            messagebox.showerror("Error", "Select an order first")
            return
        order_id = selected[0]
        for order in self.store.orders:
            if order.order_id == order_id:
                try:
                    order.cancel()
                except ERRORS as error:
                    self.show_error(error)
                    return
        self.refresh_all()

    def refresh_orders(self):
        self.clear_tree(self.orders_tree)
        for order in self.store.orders:
            self.orders_tree.insert("", "end", iid=order.order_id, values=(
                order.order_id, order.customer_id, order.created_on.isoformat(),
                order.status.value, format(order.total(), ".2f")))

    # ------------------------------------------------------------
    # dashboard tab
    # ------------------------------------------------------------
    def build_dashboard_tab(self):
        self.dashboard_label = ttk.Label(self.dashboard_tab, text="", font=("Arial", 14), justify="left")
        self.dashboard_label.pack(anchor="w", padx=20, pady=20)
        ttk.Button(self.dashboard_tab, text="Refresh", command=self.refresh_dashboard).pack(anchor="w", padx=20)

    def refresh_dashboard(self):
        stats = self.store.dashboard_status()
        text = "Customers: " + str(stats["customers"]) + "\n"
        text += "Products: " + str(stats["products"]) + "\n"
        text += "Orders today: " + str(stats["today_orders"]) + "\n"
        text += "Total sales: $" + format(stats["total_sales"], ".2f")
        self.dashboard_label.config(text=text)

    # ------------------------------------------------------------
    # refresh everything / save / close
    # ------------------------------------------------------------
    def refresh_all(self):
        self.refresh_categories()
        self.refresh_products()
        self.refresh_customers()
        self.refresh_combos()
        self.refresh_cart()
        self.refresh_orders()
        self.refresh_dashboard()

    def save_data(self):
        try:
            self.fm.save_store(self.store)
        except Exception as error:
            messagebox.showerror("Could not save", str(error))
            return
        messagebox.showinfo("Saved", "Data saved to the 'data' folder.")

    def on_close(self):
        try:
            self.fm.save_store(self.store)
        except Exception as error:
            messagebox.showerror("Could not save", str(error))
        self.root.destroy()