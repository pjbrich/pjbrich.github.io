import tkinter as tk
from tkinter import ttk, messagebox
import math
import sv_ttk
from PIL import Image, ImageTk

def calculate_geps_performance(Ltop, Wtop, H, Z, Lb=None, Wb=None, performance_goal=None, WQv=None, t=None, output_text=None):
    # Calculate bottom dimensions if not provided
    if Lb is None or Wb is None:
        Lb = Ltop - 2 * H * Z
        Wb = Wtop - 2 * H * Z

    # Calculate GEPS perimeter
    Pgeps = 2 * (Ltop + 7) + 2 * (Wtop + 7)
    Npg = math.floor(Pgeps / 10)
    Npf = math.floor(Pgeps / 70)
    Npo = Npg - Npf

    # Calculate linear feet of GEPS in perimeter
    if H <= 4:
        LFp = (120 * Npf) + (5 * Npo)
    elif H <= 9:
        LFp = (120 * Npf) + (10 * Npo)
    else:
        LFp = (120 * Npf) + (60 * Npo)

    results = {}

    for orientation in ["parallel_L", "parallel_W", "diagonal"]:
        # Determine the length to use for line calculations based on orientation
        if orientation == "parallel_L":
            line_length = Lb
            num_lines = math.floor(Wb / 15)  # Using minimum spacing
        elif orientation == "parallel_W":
            line_length = Wb
            num_lines = math.floor(Lb / 15)  # Using minimum spacing
        elif orientation == "diagonal":
            line_length = math.sqrt(Lb**2 + Wb**2)
            num_lines = math.floor(min(Lb, Wb) / (15 * math.sqrt(2)))  # Using minimum spacing

        # Determine diamond pattern based on line_length
        if line_length <= 34:
            pattern = "A"
            spacing_range = (15, 20)
            iterations_per_line = 1
            lf_per_iteration = 230
            bstr_per_iteration = 12
        elif line_length <= 75:
            pattern = "B"
            spacing_range = (15, 25)
            iterations_per_line = math.floor(line_length / 32)
            lf_per_iteration = 210
            bstr_per_iteration = 24
        else:
            pattern = "C"
            spacing_range = (20, 32)
            iterations_per_line = math.floor(line_length / 32)
            lf_per_iteration = 210
            bstr_per_iteration = 24

        units_per_iteration = 10
        infiltration_per_iteration = 67

        # Calculate the number of lines based on performance goal
        if performance_goal == "max":
            Nl = num_lines
        elif performance_goal == "min":
            Nl = math.ceil(min(Lb, Wb) / spacing_range[1])
        elif performance_goal == "specified":
            if WQv is None or t is None:
                raise ValueError("WQv and t must be provided for specified performance goal")
            F = 6.7  # GEPS per-unit infiltration rate
            Ntotal_required = math.ceil(WQv / (F * t))
            Nbottom_required = Ntotal_required - Npg
            Nl = math.ceil(Nbottom_required / (units_per_iteration * iterations_per_line))
            
            if Nl > num_lines:
                Nl = num_lines
                if output_text:
                    output_text.insert(tk.END, f"Warning: GEPS may not meet the specifications for the given basin and performance target ({orientation}).\n")
                    output_text.insert(tk.END, "Switching to maximum performance calculation.\n")
            elif Nl < math.ceil(min(Lb, Wb) / spacing_range[1]):
                Nl = math.ceil(min(Lb, Wb) / spacing_range[1])

        # Adjust iterations for diagonal orientation
        if orientation == "diagonal":
            iterations_per_line = [math.floor(min(line_length, 
                                                  math.sqrt((Lb - i*spacing_range[0]*math.sqrt(2))**2 + 
                                                            (Wb - i*spacing_range[0]*math.sqrt(2))**2)) / 32) 
                                   for i in range(Nl)]
        else:
            iterations_per_line = [iterations_per_line] * Nl

        Nbottom = sum(it * units_per_iteration for it in iterations_per_line)
        LFb = sum(it * lf_per_iteration for it in iterations_per_line)
        total_bstr = sum(it * bstr_per_iteration for it in iterations_per_line)

        Ntotal = Npg + Nbottom
        performance_24h = 6.7 * Ntotal * 24
        time_to_manage_WQv = WQv / (6.7 * Ntotal) if WQv else None
        LFt = LFp + LFb

        results[orientation] = {
            "Ntotal": Ntotal,
            "LFt": LFt,
            "total_bstr": total_bstr,
            "performance_24h": performance_24h,
            "time_to_manage_WQv": time_to_manage_WQv,
            "pattern": pattern,
            "Nl": Nl,
            "Npg": Npg,
            "LFp": LFp,
            "Nbottom": Nbottom,
            "LFb": LFb,
            "iterations_per_line": iterations_per_line
        }

    return results

def calculate_and_display():
    try:
        Ltop = float(entry_Ltop.get())
        Wtop = float(entry_Wtop.get())
        H = float(entry_H.get())
        Z = float(entry_Z.get())
        Lb = float(entry_Lb.get()) if entry_Lb.get() else None
        Wb = float(entry_Wb.get()) if entry_Wb.get() else None
        performance_goal = performance_var.get()
        WQv = float(entry_WQv.get()) if entry_WQv.get() else None
        t = float(entry_t.get()) if entry_t.get() else None

        # Pass the output_text widget to the calculation function
        results = calculate_geps_performance(Ltop, Wtop, H, Z, Lb, Wb, performance_goal, WQv, t, output_text)

        # Display results in the output box
        for orientation, result in results.items():
            output_text.insert(tk.END, f"\n--- Orientation: {orientation} ---\n")
            output_text.insert(tk.END, f"Total GEPS units: {result['Ntotal']}\n")
            output_text.insert(tk.END, f"GEPS units in perimeter: {result['Npg']}\n")
            output_text.insert(tk.END, f"GEPS units in bottom: {result['Nbottom']}\n")
            output_text.insert(tk.END, f"Total linear feet of GEPS: {result['LFt']:.2f}\n")
            output_text.insert(tk.END, f"Linear feet of GEPS in perimeter: {result['LFp']:.2f}\n")
            output_text.insert(tk.END, f"Linear feet of GEPS in bottom: {result['LFb']:.2f}\n")
            output_text.insert(tk.END, f"Total BSTR: {result['total_bstr']}\n")
            output_text.insert(tk.END, f"Estimated performance in 24 hours: {result['performance_24h']:.2f} CF\n")
            if result['time_to_manage_WQv']:
                output_text.insert(tk.END, f"Estimated time to manage WQv: {result['time_to_manage_WQv']:.2f} hours\n")
            output_text.insert(tk.END, f"Diamond pattern: {result['pattern']}\n")
            output_text.insert(tk.END, f"Number of lines: {result['Nl']}\n")
            output_text.insert(tk.END, f"Iterations per line: {result['iterations_per_line']}\n")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Calculation Error", str(e))

# Create the main window
root = tk.Tk()
sv_ttk.set_theme("light")
root.iconbitmap("exlterra.ico")
root.title("Exlterra GEPS Basin Estimator")
bg_image = Image.open("bg.jpg")  # Replace with your image file
bg_photo = ImageTk.PhotoImage(bg_image)
# Create and place input fields
tk.Label(root, text="Length (Top of slope):").grid(row=0, column=0, sticky="e")
entry_Ltop = tk.Entry(root)
entry_Ltop.grid(row=0, column=1)

tk.Label(root, text="Width (Top of slope):").grid(row=1, column=0, sticky="e")
entry_Wtop = tk.Entry(root)
entry_Wtop.grid(row=1, column=1)

tk.Label(root, text="Height / Depth of basin:").grid(row=2, column=0, sticky="e")
entry_H = tk.Entry(root)
entry_H.grid(row=2, column=1)

tk.Label(root, text="Slope Factor Z (Z:1):").grid(row=3, column=0, sticky="e")
entry_Z = tk.Entry(root)
entry_Z.grid(row=3, column=1)

tk.Label(root, text="Length(Bottom surface) (optional):").grid(row=4, column=0, sticky="e")
entry_Lb = tk.Entry(root)
entry_Lb.grid(row=4, column=1)

tk.Label(root, text="Width(Bottom surface) (optional):").grid(row=5, column=0, sticky="e")
entry_Wb = tk.Entry(root)
entry_Wb.grid(row=5, column=1)

tk.Label(root, text="Performance Goal:").grid(row=6, column=0, sticky="e")
performance_var = tk.StringVar(value="specified")
performance_menu = ttk.Combobox(root, textvariable=performance_var, values=["max", "min", "specified"])
performance_menu.grid(row=6, column=1)

tk.Label(root, text="WQv in CF (for specified):").grid(row=7, column=0, sticky="e")
entry_WQv = tk.Entry(root)
entry_WQv.grid(row=7, column=1)

tk.Label(root, text="t in hours (for specified):").grid(row=8, column=0, sticky="e")
entry_t = tk.Entry(root)
entry_t.grid(row=8, column=1)

# Create and place the calculate button
calculate_button = tk.Button(root, text="Estimate", command=calculate_and_display)
calculate_button.grid(row=9, column=0, columnspan=2)

# Create and place the output text area
output_text = tk.Text(root, height=30, width=60)
output_text.grid(row=10, column=0, columnspan=2)


# Start the GUI event loop
root.mainloop()
