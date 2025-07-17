import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

def open_csv():
    # Open file dialog to pick CSV file
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Select your CSV file"
    )
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path)
        show_csv(df)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV:\n{e}")

def show_csv(df):
    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create table
    tree = ttk.Treeview(frame)
    tree.pack(fill="both", expand=True)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for i, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Initialize GUI window
root = tk.Tk()
root.title("CSV Viewer Interface")
root.geometry("700x400")

# Button to load CSV
btn = tk.Button(root, text="📂 Load CSV File", command=open_csv)
btn.pack(pady=10)

# Frame for table
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Run the app
root.mainloop()
