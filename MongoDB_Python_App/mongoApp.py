# Created by: BGR - 10/30/2024
# Updated on: 12/27/2024

import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

def fetch_documents(search_query=None):
    client = MongoClient('localhost', 27017) #update to QNAP once implemented
    db = client['Workshop']
    collection = db['Master Hydraulic Fittings']

    if search_query:
        query = {
            "$or": [
                {"Description/Name": {"$regex": search_query, "$options": "i"}},
                {"Part#": {"$regex": search_query, "$options": "i"}},
                {"Supplier": {"$regex": search_query, "$options": "i"}},
                {"Current Stock": {"$regex": search_query, "$options": "i"}},
                {"Comparison": {"$regex": search_query, "$options": "i"}},
                {"Notes": {"$regex": search_query, "$options": "i"}}
            ]
        }
    else:
        query = {}

    documents = list(collection.find(query))
    client.close()
    return documents

def display_documents(search_query=None):
    documents = fetch_documents(search_query)
    text_widget.delete('1.0', tk.END)
    for doc in documents:
        id_str = str(doc.get("_id", "N/A"))
        name = doc.get("Description/Name", "N/A")
        partNO = doc.get("Part#", "N/A")
        supplier = doc.get("Supplier", "N/A")
        currentStock = doc.get("Current Stock", "N/A")
        comparison = doc.get("Comparison", "N/A")
        notes = doc.get("Notes", "N/A")
        text_widget.insert(tk.END, f"ID: {id_str}\nName: {name}\nPart#: {partNO}\nSupplier#: {supplier}\nCurrent Stock: {currentStock}\nComparison#: {comparison}\nNotes: {notes}\n\n")

def search():
    query = search_entry.get()
    display_documents(query)

def update_document():
    query = search_entry.get()
    if not query:
        tk.messagebox.showerror("Error", "Please enter a Part# to update")
        return

    update_window = tk.Toplevel(root)
    update_window.title("Update Document")
    update_window.geometry("400x300")

    fields = ["Description/Name", "Part#", "Supplier", "Current Stock", "Comparison", "Notes"]
    entries = {}

    for field in fields:
        frame = ttk.Frame(update_window)
        frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(frame, text=field).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        entries[field] = entry

    def save_update():
        client = MongoClient('localhost', 27017)
        db = client['Workshop']
        collection = db['Master Hydraulic Fittings']

        update_data = {field: entry.get() for field, entry in entries.items() if entry.get()}
        result = collection.update_one({"Part#": query}, {"$set": update_data})

        if result.modified_count > 0:
            tk.messagebox.showinfo("Success", "Document updated successfully")
            display_documents(query)
        else:
            tk.messagebox.showerror("Error", "No document found with the given Part#")

        client.close()
        update_window.destroy()

    ttk.Button(update_window, text="Save", command=save_update).pack(pady=10)

# Create the main window
root = tk.Tk()
root.title("MongoDB Document Viewer - Master List")
root.geometry("800x600")

# Create and pack a frame
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Create a search bar
search_frame = ttk.Frame(frame)
search_frame.pack(fill=tk.X, pady=(0, 10))

search_entry = ttk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

search_button = ttk.Button(search_frame, text="Search", command=search)
search_button.pack(side=tk.RIGHT)

# Create a text widget with scrollbar
text_widget = tk.Text(frame, wrap=tk.WORD, width=50, height=15)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
text_widget.configure(yscrollcommand=scrollbar.set)

# Pack the text widget and scrollbar
text_widget.pack(side="left", fill=tk.BOTH, expand=True)
scrollbar.pack(side="right", fill="y")

# Create and pack a refresh button
refresh_button = ttk.Button(root, text="Refresh", command=lambda: display_documents())
refresh_button.pack(pady=10)

# Create and pack an update button
update_button = ttk.Button(root, text="Update", command=update_document)
update_button.pack(pady=10)

# Initial display of documents
display_documents()

# Start the Tkinter event loop
root.mainloop()
