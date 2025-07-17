import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from etl_pipeline import run_pipeline

def run_etl_and_display():
    try:
        df, filepath = run_pipeline()
        messagebox.showinfo("ETL Completed", f"Data saved to: {filepath}")
        show_csv(df)
    except Exception as e:
        messagebox.showerror("ETL Error", str(e))

def show_csv(df):
    for widget in frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(frame)
    tree.pack(fill="both", expand=True)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# GUI setup
app = tk.Tk()
app.title("ETL Pipeline GUI")
app.geometry("700x400")

btn = tk.Button(app, text="▶ Run ETL Pipeline", command=run_etl_and_display)
btn.pack(pady=10)

frame = tk.Frame(app)
frame.pack(fill="both", expand=True)

app.mainloop()
