# Created by: BGR - 10/30/2024
# Updated on: 11/14/2024
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient

def fetch_documents():
    client = MongoClient('localhost', 27017)
    db = client['Inventory']
    collection = db['Products']
    
    # Only retrieve Name and Amount fields
    documents = list(collection.find({}, {"Name": 1, "Amount": 1, "_id": 0}))
    client.close()
    return documents

def display_documents():
    documents = fetch_documents()
    text_widget.delete('1.0', tk.END)  # Clear existing text
    for doc in documents:
        name = doc.get("Name", "N/A")
        amount = doc.get("Amount", "N/A")
        text_widget.insert(tk.END, f"Name: {name}\nAmount: {amount}\n\n")

# Create the main window
root = tk.Tk()
root.title("MongoDB Document Viewer - Name & Amount")
root.geometry("400x300")

# Create and pack a frame
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Create a text widget with scrollbar
text_widget = tk.Text(frame, wrap=tk.WORD, width=50, height=15)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
text_widget.configure(yscrollcommand=scrollbar.set)

# Pack the text widget and scrollbar
text_widget.pack(side="left", fill=tk.BOTH, expand=True)
scrollbar.pack(side="right", fill="y")

# Create and pack a refresh button
refresh_button = ttk.Button(root, text="Refresh", command=display_documents)
refresh_button.pack(pady=10)

# Initial display of documents
display_documents()

# Start the Tkinter event loop
root.mainloop()
