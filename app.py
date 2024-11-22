import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import messagebox, ttk


# Hàm kết nối đến cơ sở dữ liệu
def connect_to_db(username, password):
    try:
        connection = psycopg2.connect(
            dbname="quanly_quanao",
            user=username,
            password=password,
            host="localhost"
        )
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        return connection
    except psycopg2.OperationalError as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None


# Chức năng tìm kiếm sản phẩm
def search_product(connection, product_name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM products WHERE product_name ILIKE %s"
            cursor.execute(query, ('%' + product_name + '%',))
            return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tìm sản phẩm: {e}")
        return None


# Chức năng thêm sản phẩm mới
def add_product(connection, product_name, product_price, category_id):
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO products (product_name, product_price, category_id) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (product_name, product_price, category_id))
            connection.commit()
            messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {e}")


# Hàm cài đặt kiểu dáng cho ứng dụng
def set_style(widget):
    style = ttk.Style(widget)
    style.theme_use("clam")
    style.configure(
        "TButton",
        font=("Arial", 12, "bold"),
        background="#42a5f5",
        foreground="#ffffff",
        padding=8,
    )
    style.map(
        "TButton",
        background=[("active", "#1565c0")],
    )


# Giao diện đăng nhập
def login_form():
    window = tk.Tk()
    window.title("Đăng Nhập Hệ Thống")
    window.geometry("500x300")
    window.configure(bg="#e3f2fd")
    set_style(window)

    tk.Label(
        window, text="ĐĂNG NHẬP HỆ THỐNG", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#1565c0"
    ).pack(pady=20)

    login_frame = tk.Frame(window, bg="#e3f2fd")
    login_frame.pack(pady=20)

    tk.Label(login_frame, text="Tên đăng nhập:", font=("Arial", 12), bg="#e3f2fd", fg="#333333").grid(
        row=0, column=0, padx=10, pady=10
    )
    username_entry = ttk.Entry(login_frame, width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_frame, text="Mật khẩu:", font=("Arial", 12), bg="#e3f2fd", fg="#333333").grid(
        row=1, column=0, padx=10, pady=10
    )
    password_entry = ttk.Entry(login_frame, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        if username.strip() == "" or password.strip() == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin!")
        else:
            connection = connect_to_db(username, password)
            if connection:
                window.destroy()
                show_menu(connection)

    ttk.Button(window, text="Đăng Nhập", command=login_action).pack(pady=15)
    window.mainloop()


# Giao diện menu sau khi đăng nhập
def show_menu(connection):
    menu_window = tk.Tk()
    menu_window.title("Menu Quản Lý")
    menu_window.geometry("400x300")
    menu_window.configure(bg="#e3f2fd")
    set_style(menu_window)

    tk.Label(
        menu_window, text="CHỨC NĂNG QUẢN LÝ", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#1565c0"
    ).pack(pady=20)

    ttk.Button(menu_window, text="Tìm kiếm sản phẩm", command=lambda: search_product_form(connection)).pack(
        pady=10
    )
    ttk.Button(menu_window, text="Thêm sản phẩm", command=lambda: add_product_form(connection)).pack(pady=10)

    menu_window.mainloop()


# Giao diện tìm kiếm sản phẩm
def search_product_form(connection):
    search_window = tk.Tk()
    search_window.title("Tìm kiếm sản phẩm")
    search_window.geometry("500x400")
    search_window.configure(bg="#e3f2fd")
    set_style(search_window)

    tk.Label(
        search_window, text="Tìm Kiếm Sản Phẩm", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#1565c0"
    ).pack(pady=20)

    search_frame = tk.Frame(search_window, bg="#e3f2fd")
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Nhập tên sản phẩm:", font=("Arial", 12), bg="#e3f2fd", fg="#333333").grid(
        row=0, column=0, padx=10, pady=10
    )
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    result_text = tk.Text(search_window, width=60, height=10, wrap="word")
    result_text.pack(pady=10)

    def search_action():
        product_name = search_entry.get()
        result = search_product(connection, product_name)
        result_text.delete(1.0, tk.END)
        if result:
            for row in result:
                result_text.insert(tk.END, f"ID: {row[0]}, Tên: {row[1]}, Giá: {row[2]}, Loại: {row[3]}\n")
        else:
            result_text.insert(tk.END, "Không tìm thấy sản phẩm nào.\n")

    ttk.Button(search_window, text="Tìm kiếm", command=search_action).pack(pady=10)
    search_window.mainloop()


# Giao diện thêm sản phẩm
def add_product_form(connection):
    add_window = tk.Tk()
    add_window.title("Thêm sản phẩm mới")
    add_window.geometry("500x400")
    add_window.configure(bg="#e3f2fd")
    set_style(add_window)

    tk.Label(
        add_window, text="Thêm Sản Phẩm Mới", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#1565c0"
    ).pack(pady=20)

    add_frame = tk.Frame(add_window, bg="#e3f2fd")
    add_frame.pack(pady=10)

    tk.Label(add_frame, text="Tên sản phẩm:", font=("Arial", 12), bg="#e3f2fd", fg="#333333").grid(
        row=0, column=0, padx=10, pady=10
    )
    product_name_entry = ttk.Entry(add_frame, width=30)
    product_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(add_frame, text="Giá sản phẩm:", font=("Arial", 12), bg="#e3f2fd", fg="#333333").grid(
        row=1, column=0, padx=10, pady=10
    )
    product_price_entry = ttk.Entry(add_frame, width=30)
    product_price_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(add_frame, text="Mã loại sản phẩm:", font=("Arial", 12), bg="#e3f2fd", fg="#333333").grid(
        row=2, column=0, padx=10, pady=10
    )
    category_id_entry = ttk.Entry(add_frame, width=30)
    category_id_entry.grid(row=2, column=1, padx=10, pady=10)

    def add_action():
        product_name = product_name_entry.get()
        product_price = product_price_entry.get()
        category_id = category_id_entry.get()
        if product_name and product_price and category_id:
            add_product(connection, product_name, float(product_price), int(category_id))

    ttk.Button(add_window, text="Thêm sản phẩm", command=add_action).pack(pady=20)
    add_window.mainloop()


# Khởi chạy ứng dụng
login_form()
