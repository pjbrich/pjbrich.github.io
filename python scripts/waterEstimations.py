import tkinter as tk
from tkinter import messagebox

def calculate_infiltration(event=None):
    try:
        total_geps = int(geps_entry.get())
        surface_area = float(area_entry.get())
        depth = float(depth_entry.get())

        gal_over_hour = total_geps * 50
        cubic_over_hour = gal_over_hour / 7.48
        water_volume_cf = surface_area * depth
        time_to_infiltrate = water_volume_cf / cubic_over_hour

        result = f"Total GEPS units: {total_geps}\n"
        result += f"Total Gallons infiltrated per Hour: {gal_over_hour}\n"
        result += f"Total Cubic Feet infiltrated per Hour: {cubic_over_hour:.2f}\n"
        result += f"Water Volume in Cubic Feet: {water_volume_cf:.2f}\n"
        result += f"Total hours of infiltration: {time_to_infiltrate:.2f}"

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# Create the main window
window = tk.Tk()
window.title("Infiltration Estimator")
window.geometry("400x500")

# Create and place widgets
tk.Label(window, text="Total number of GEPS units:").pack(pady=5)
geps_entry = tk.Entry(window)
geps_entry.pack()

tk.Label(window, text="Surface area of water (sq ft):").pack(pady=5)
area_entry = tk.Entry(window)
area_entry.pack()

tk.Label(window, text="Depth of water (ft):").pack(pady=5)
depth_entry = tk.Entry(window)
depth_entry.pack()

#uses enter for an input too 
calculate_button = tk.Button(window, text="Calculate", command=calculate_infiltration)
calculate_button.pack(pady=10)
window.bind('<Return>', lambda event:calculate_infiltration())


result_text = tk.Text(window, height=10, width=50)
result_text.pack(pady=10)

# Start the GUI event loop
window.mainloop()
