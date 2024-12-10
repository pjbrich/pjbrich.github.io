# Created by: BGR - 10/30/2024
# Updated on: 12/10/2024
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient


def fetch_documents(search_query=None):
    client = MongoClient('localhost', 27017) #update to QNAP once implemented
    db = client['Workshop']
    collection = db['HAZL Hydraulic Fittings']

    #our query is made up of Column Names (defined in the spreadsheet)
    # If there's a search query, use it to filter the documents
    if search_query:
        query = {
            "$or": [
                {"Description/Name": {"$regex": search_query, "$options": "i"}},
                {"Part#": {"$regex": search_query, "$options": "i"}},
                {"Supplier": {"$regex": search_query, "$options": "i"}},
                {"#/RIG": {"$regex": search_query, "$options": "i"}}
            ]
        }
    else:
        query = {}

    documents = list(collection.find(query, {"Description/Name":1, "Part#":1, "Supplier":1, "#/RIG":1, "_id":0}))
    client.close()
    return documents
#added a search_query for document fetching
def display_documents(search_query=None):
    documents = fetch_documents(search_query) #uses search_query to "look" into each document, we can find multiple results this way. 
    text_widget.delete('1.0', tk.END)  # Clear existing text
    for doc in documents:
        name = doc.get("Description/Name", "N/A")
        partNO = doc.get("Part#", "N/A")
        supplier = doc.get("Supplier", "N/A")
        perRIG = doc.get("#/RIG", "N/A")
        text_widget.insert(tk.END, f"Name: {name}\nPart#: {partNO}\nSupplier#: {supplier}\nperRIG#: {perRIG}\n\n")

#uses the search query to fetch doucments and displays them (since we're in display_document())
def search():
    query = search_entry.get()
    display_documents(query)

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

# Initial display of documents
display_documents()

# Start the Tkinter event loop
root.mainloop()
