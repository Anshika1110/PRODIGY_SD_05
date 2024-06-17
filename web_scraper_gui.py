import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from bs4 import BeautifulSoup
import csv

def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        products = soup.find_all('div', class_='product-tuple-listing')

        scraped_data = []

        for product in products:
            name = product.find('p', class_='product-title').text.strip()
            price = product.find('span', class_='product-price').text.strip()
            rating_tag = product.find('div', class_='filled-stars')
            rating = rating_tag['style'] if rating_tag else 'No rating'

            scraped_data.append((name, price, rating))

        return scraped_data

    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []

def display_data(data):
    for i in tree.get_children():
        tree.delete(i)

    for item in data:
        tree.insert('', 'end', values=item)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Price', 'Rating'])
            writer.writerows(scraped_data)
        messagebox.showinfo("Success", f"Data successfully written to {file_path}")

def fetch_and_display_data():
    global scraped_data
    url = url_entry.get()
    scraped_data = scrape_data(url)
    display_data(scraped_data)

# Create the main window
root = tk.Tk()
root.title("Web Scraper")

# URL entry
tk.Label(root, text="Enter the URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)
url_entry.insert(0, 'https://www.snapdeal.com/products/mobiles-mobile-phones')

# Fetch and display button
fetch_button = tk.Button(root, text="Fetch and Display Data", command=fetch_and_display_data)
fetch_button.grid(row=1, column=0, columnspan=2, pady=10)

# Treeview widget for displaying data
columns = ('Product Name', 'Price', 'Rating')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('Product Name', text='Product Name')
tree.heading('Price', text='Price')
tree.heading('Rating', text='Rating')
tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Save button
save_button = tk.Button(root, text="Save to CSV", command=save_file)
save_button.grid(row=3, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
