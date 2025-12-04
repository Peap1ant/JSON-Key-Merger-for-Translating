import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class JsonKeyMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Key Merger")
        self.root.geometry("550x220")  # Fixed window size
        self.root.resizable(False, False)  # Disable resizing

        # Initialize variables
        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar()

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Main frame with padding
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Input Area (Using Grid)
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # --- Source File Row ---
        lbl_source = tk.Label(input_frame, text="Source JSON:", width=12, anchor="w", font=("Arial", 10, "bold"))
        lbl_source.grid(row=0, column=0, pady=5)

        entry_source = tk.Entry(input_frame, textvariable=self.source_path, width=45)
        entry_source.grid(row=0, column=1, padx=5, pady=5)

        btn_source = tk.Button(input_frame, text="Browse", command=self.select_source, width=10)
        btn_source.grid(row=0, column=2, padx=5, pady=5)

        # --- Target File Row ---
        lbl_target = tk.Label(input_frame, text="Target JSON:", width=12, anchor="w", font=("Arial", 10, "bold"))
        lbl_target.grid(row=1, column=0, pady=5)

        entry_target = tk.Entry(input_frame, textvariable=self.target_path, width=45)
        entry_target.grid(row=1, column=1, padx=5, pady=5)

        btn_target = tk.Button(input_frame, text="Browse", command=self.select_target, width=10)
        btn_target.grid(row=1, column=2, padx=5, pady=5)

        # 2. Action Button Area
        btn_run = tk.Button(main_frame, text="Merge Keys & Save (to Target Folder)", 
                            command=self.process_json, bg="#e1e1e1", height=2, font=("Arial", 11))
        btn_run.pack(fill=tk.X)

    def select_source(self):
        filename = filedialog.askopenfilename(title="Select Source JSON", filetypes=[("JSON files", "*.json")])
        if filename:
            self.source_path.set(filename)

    def select_target(self):
        filename = filedialog.askopenfilename(title="Select Target JSON", filetypes=[("JSON files", "*.json")])
        if filename:
            self.target_path.set(filename)

    def process_json(self):
        s_path = self.source_path.get()
        t_path = self.target_path.get()

        if not s_path or not t_path:
            messagebox.showwarning("Warning", "Please select both source and target files.")
            return

        try:
            # Read files
            with open(s_path, "r", encoding="utf-8") as f:
                source_data = json.load(f)
            
            with open(t_path, "r", encoding="utf-8") as f:
                target_data = json.load(f)

            # Validate structure
            if not isinstance(source_data, dict) or not isinstance(target_data, dict):
                messagebox.showerror("Error", "Top-level structure of JSON must be an Object (Dictionary).")
                return

            # Logic: Merge keys
            added_count = 0
            for key in source_data.keys():
                if key not in target_data:
                    target_data[key] = ""  # Assign empty string as requested
                    added_count += 1

            # Generate output path (based on target file location)
            target_dir = os.path.dirname(t_path)
            target_filename = os.path.basename(t_path)
            filename_no_ext = os.path.splitext(target_filename)[0]
            
            output_filename = f"{filename_no_ext}_integrated.json"
            output_path = os.path.join(target_dir, output_filename)

            # Write file
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(target_data, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("Success", f"Operation Complete!\n\n[Keys Added]: {added_count}\n[Saved Path]: {output_path}")

        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonKeyMergerApp(root)
    root.mainloop()