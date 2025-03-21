#created by Benjamin Ricahrds - 03/03/2025
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math 


def calculate_infiltration(event=None):
    try:
        total_geps = int(geps_entry.get())
        surface_area = float(area_entry.get())
        depth = float(depth_entry.get())
        

        #gallons per hour
        gal_over_hour = total_geps * 50

        #depth in inches
        depth_in = depth * 12

        #cubic feet per hour
        cubic_over_hour = gal_over_hour / 7.48
        water_volume = surface_area * depth_in
        time_to_infiltrate = water_volume / cubic_over_hour
        
        #need to convert time_to_infiltrate in HH:MM, split up the time 
        integer_part = math.trunc(time_to_infiltrate)
        fract_part = time_to_infiltrate - integer_part

        fract_part_int = turnIntoHHMM(fract_part)


        #-----------------------------METRIC---------------------------------------------

        cubic_meter_over_hour = gal_over_hour / 264.172
        depth_m = depth / 1000
        water_volume_m = surface_area * depth_m
        time_to_infiltrate_m = water_volume_m / cubic_meter_over_hour

           #need to convert time_to_infiltrate in HH:MM, split up the time 
        integer_part_m = math.trunc(time_to_infiltrate_m)
        fract_part_m = time_to_infiltrate_m - integer_part_m

        fract_part_int_m = turnIntoHHMM(fract_part_m)

        #fract_part_m = fract_part_m * 60
        #fract_part_m = math.ceil(fract_part_m)
        #fract_part_int = int(fract_part_m) + (1 if fract_part_m > int(fract_part_m) else 0)

        # Display results
        #--------------------------------------------------------------------------------
        if unit_var.get() == "Imperial":
            # Update result display
            result_text.delete(1.0, tk.END)
            result_text.tag_configure("title", font=("Consolas", 12))
            result_text.tag_configure("body", font=("Consolas", 12))
            
            result_text.insert(tk.END, "Infiltration Results\n", "title")
            result_text.insert(tk.END, f"Total GEPS units: {total_geps}\n", "body")
            #result_text.insert(tk.END, f"Total Gallons infiltrated per Hour: {gal_over_hour}\n", "body")
            result_text.insert(tk.END, f"Total Cubic Feet infiltrated per Hour: {cubic_over_hour:.2f}\n", "body")
            result_text.insert(tk.END, f"Total Cubic Feet infiltrated per Day: {cubic_over_hour*24:.2f}\n", "body")

            result_text.insert(tk.END, f"Water Volume in Cubic Feet: {water_volume:.2f}\n", "body")
            result_text.insert(tk.END, f"Total hours to infiltrate {water_volume:.2f}cf of water: {integer_part} hours and {fract_part_int} minutes", "body")
            #result_text.insert(tk.END, f"Total hours to infiltrate {water_volume:.2f}cf of water: {time_to_infiltrate:.2f}", "body")
        else:
             # Update result display
            result_text.delete(1.0, tk.END)
            result_text.tag_configure("title", font=("Consolas", 12))
            result_text.tag_configure("body", font=("Consolas", 12))

            result_text.insert(tk.END, "Infiltration Results\n", "title")
            result_text.insert(tk.END, f"Total GEPS units: {total_geps}\n", "body")
            result_text.insert(tk.END, f"Total Cubic Meter infiltrated per Hour: {cubic_meter_over_hour:.2f}\n", "body")
            result_text.insert(tk.END, f"Total Cubic Meter infiltrated per Day: {cubic_meter_over_hour*24:.2f}\n", "body")
            result_text.insert(tk.END, f"Water Volume in Cubic meters: {water_volume_m:.2f}\n", "body")
            result_text.insert(tk.END, f"Total hours to infiltrate {water_volume_m:.2f} cubic meters of water: {integer_part_m} hours and {fract_part_int_m} minutes", "body")

            #result_text.insert(tk.END, f"Total hours to infiltrate {water_volume_m:.2f}m^3 of water: {time_to_infiltrate_m:.2f}", "body")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

def update_labels(event):
    if unit_var.get() == "Imperial":
        area_label.config(text="Surface area of water (sq ft):")
        depth_label.config(text="Depth of water (in):")
        calculate_infiltration()
    else:
        area_label.config(text="Surface area of water (sq m):")
        depth_label.config(text="Depth of water (mm):")
        calculate_infiltration()

#turns the fractional hours lopped off during truncation, and turns it into whole minutes!
def turnIntoHHMM (time):
    
    time = time * 60
    time = math.ceil(time)
    newTime = int(time) + (1 if time > int(time) else 0)
    return newTime

def turnIntoDDHH (time):
    
    time = time * 60
    time = math.ceil(time)
    newTime = int(time) + (1 if time > int(time) else 0)
    return newTime

# Create the main window
window = tk.Tk()
window.title("Infiltration Estimator")
window.geometry("1280x960")

# Create and place widgets
tk.Label(window, text="Total number of GEPS units:").pack(pady=5)
geps_entry = tk.Entry(window)
geps_entry.pack()

unit_var = tk.StringVar(value="Imperial")
unit_dropdown = ttk.Combobox(window, textvariable=unit_var, values=["Imperial", "Metric"], state="readonly")
unit_dropdown.pack(pady=5)
unit_dropdown.bind("<<ComboboxSelected>>", update_labels)

area_label = tk.Label(window, text="Surface area of water (sq ft):")
area_label.pack(pady=5)
area_entry = tk.Entry(window)
area_entry.pack()

depth_label = tk.Label(window, text="Depth of water (in):")
depth_label.pack(pady=5)
depth_entry = tk.Entry(window)
depth_entry.pack()

calculate_button = tk.Button(window, text="Calculate", command=calculate_infiltration)
calculate_button.pack(pady=10)
window.bind('<Return>', lambda event: calculate_infiltration())

result_text = tk.Text(window, height=100, width=200)
result_text.pack(pady=10)

# Start the GUI event loop
window.mainloop()
