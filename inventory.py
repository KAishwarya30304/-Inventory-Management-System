import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import psycopg2


class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Inventory Management")
        self.root.geometry("600x500")

        # Load and set background image
        self.bg_image = Image.open(r"C:\Users\a\Downloads\Inventory Management System Logo, HD Png Download , Transparent Png Image - PNGitem.jpeg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Welcome label
        self.label_welcome = tk.Label(self.root, text="Welcome to Inventory Management System", font=("Arial", 30, "bold"), fg="blue")
        self.label_welcome.pack(pady=30)

        # Info label
        self.label_info = tk.Label(self.root, text="Please login to access the system", font=("Arial", 19))
        self.label_info.pack(pady=10)

        # Login button
        self.button_login = tk.Button(self.root, text="Login", font=("Arial", 18, "bold"), command=self.open_login_window)
        self.button_login.pack(pady=20)

    def open_login_window(self):
        """Open the login window."""
        self.root.destroy()
        login_window = tk.Tk()
        LoginWindow(login_window)
        login_window.mainloop()


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x500")

        # Load and set background image
        self.bg_image = Image.open(r"C:\Users\a\Videos\inventory management.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Login frame
        self.frame_login = tk.Frame(self.root, bg="beige")
        self.frame_login.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Username input
        self.label_username = tk.Label(self.frame_login, text="Username:", fg="black", font=("Arial", 22, "bold"), bg="beige")
        self.label_username.grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 16))
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        # Password input
        self.label_password = tk.Label(self.frame_login, text="Password:", fg="black", font=("Arial", 22, "bold"), bg="beige")
        self.label_password.grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(self.frame_login, show="*", font=("Arial", 16))
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        # Login button
        self.button_login = tk.Button(self.frame_login, text="Login", command=self.login, bg="black", fg="white", font=("Arial", 16, "bold"))
        self.button_login.grid(row=2, columnspan=2, padx=5, pady=5)

        # Bind Enter key to the login function
        self.root.bind('<Return>', lambda event: self.login())

    def login(self):
        """Authenticate user login."""
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "1" and password == "1234":
            self.root.destroy()
            app = InventoryManagementApp(tk.Tk())
        else:
            messagebox.showerror("Error", "Invalid username or password")


class InventoryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x700")

        # Load and set background image
        self.bg_image = Image.open(r"C:\Users\a\Videos\ak.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create database connection
        self.create_database_connection()

        # Create frames for options and products display
        self.frame_options = tk.Frame(self.root, bg="beige")
        self.frame_options.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.frame_treeview = tk.Frame(self.root)
        self.frame_treeview.place(relx=0.5, rely=0.4, anchor=tk.CENTER, relwidth=1, relheight=0.5)

        # Create buttons for various functionalities
        self.create_product_buttons()

        # Create treeview to display products
        self.create_treeview()
        
        # Show all products initially
        self.show_products()

    def create_database_connection(self):
        """Establish a database connection."""
        try:
            self.db_connection = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="1234",  # Avoid hardcoding sensitive information in production
                host="localhost"
            )
            self.cursor = self.db_connection.cursor()
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to the database: {e}")

    def create_product_buttons(self):
        """Create buttons for product management."""
        button_names = [
            ("Insert Product", self.insert_product), 
            ("Search", self.search_product),
            ("Show Categories", self.show_categories),
            ("Delete Product", self.delete_product),
            ("Modify Product Name", self.modify_product_name),
            ("Show Products", self.show_products)
        ]

        for i, (text, command) in enumerate(button_names):
            button = tk.Button(self.frame_options, text=text, command=command, bg="black", fg="white", font=("Arial", 16, "bold"))
            button.grid(row=0, column=i, padx=5, pady=5)

    def create_treeview(self):
        """Create a treeview for displaying product information."""
        self.tree = ttk.Treeview(self.frame_treeview, columns=("ID", "Name", "Category ID", "Quantity", "Price", "Description"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col in ("ID", "Quantity", "Price") else 150)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_tree_item_double_click)

    def fetch_data(self, sql, values=None):
        """Fetch data from the database."""
        try:
            self.cursor.execute(sql, values) if values else self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching data: {e}")
            return []

    def execute_query(self, sql, values):
        """Execute a query and commit changes to the database."""
        try:
            self.cursor.execute(sql, values)
            self.db_connection.commit()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while executing query: {e}")

    def display_treeview(self, items, categories=False):
        """Display products or categories in the treeview."""
        # Clear existing items in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Define the columns based on whether we're showing categories or products
        if categories:
            self.tree["columns"] = ("ID", "Category Name")
            self.tree.heading("ID", text="Category ID")
            self.tree.heading("Category Name", text="Category Name")
            
            # Insert categories into the treeview
            for category in items:
                self.tree.insert("", tk.END, values=(category[0], category[1]))  # Category ID and Name
        else:
            self.tree["columns"] = ("ID", "Name", "Category ID", "Quantity", "Price", "Description")
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)

            # Insert products into the treeview
            for product in items:
                self.tree.insert("", tk.END, values=product)

    def insert_product(self):
        """Insert a new product into the database."""
        product_name = simpledialog.askstring("Input", "Enter the product name:")
        category_id = simpledialog.askinteger("Input", "Enter the category ID:")
        quantity = simpledialog.askinteger("Input", "Enter the quantity:")
        price = simpledialog.askfloat("Input", "Enter the price:")
        description = simpledialog.askstring("Input", "Enter the description:")

        if product_name and category_id is not None and quantity is not None and price is not None and description:
            sql = "INSERT INTO Products (product_name, category_id, quantity, price, description) VALUES (%s, %s, %s, %s, %s)"
            self.execute_query(sql, (product_name, category_id, quantity, price, description))
            self.show_products()
        else:
            messagebox.showwarning("Input Error", "Please provide all required information.")

    def search_product(self):
        """Search for a product in the database."""
        search_query = simpledialog.askstring("Search", "Enter product name to search:")
        sql = "SELECT * FROM Products WHERE product_name ILIKE %s"
        products = self.fetch_data(sql, (f"%{search_query}%",))
        self.display_treeview(products)

    def show_categories(self):
        """Show all categories in the treeview."""
        sql = "SELECT * FROM Categories"
        categories = self.fetch_data(sql)
        self.display_treeview(categories, categories=True)

    def delete_product(self):
        """Delete a product from the database."""
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item, "values")[0]
            sql = "DELETE FROM Products WHERE id = %s"
            self.execute_query(sql, (product_id,))
            self.show_products()
        else:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")

    def modify_product_name(self):
        """Modify the name of a product in the database."""
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item, "values")[0]
            new_name = simpledialog.askstring("Input", "Enter the new product name:")
            if new_name:
                sql = "UPDATE Products SET product_name = %s WHERE id = %s"
                self.execute_query(sql, (new_name, product_id))
                self.show_products()
        else:
            messagebox.showwarning("Selection Error", "Please select a product to modify.")

    def show_products(self):
        """Show all products in the treeview."""
        sql = "SELECT * FROM Products"
        products = self.fetch_data(sql)
        self.display_treeview(products)

    def on_tree_item_double_click(self, event):
        """Handle double-click on treeview item."""
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item, "values")[0]
            messagebox.showinfo("Product Details", f"Details for Product ID: {product_id}")

    def __del__(self):
        """Close the database connection when the app is closed."""
        if hasattr(self, 'db_connection'):
            self.cursor.close()
            self.db_connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    WelcomePage(root)
    root.mainloop()
