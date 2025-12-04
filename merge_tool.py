import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class JsonKeyMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Key Sync Tool")
        self.root.geometry("550x280")  # Increased height for the checkbox
        self.root.resizable(False, False)

        # Initialize variables
        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar()
        self.delete_option = tk.BooleanVar()  # Variable for the checkbox

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Input Area
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # --- Source File ---
        lbl_source = tk.Label(input_frame, text="Source JSON:", width=12, anchor="w", font=("Arial", 10, "bold"))
        lbl_source.grid(row=0, column=0, pady=5)

        entry_source = tk.Entry(input_frame, textvariable=self.source_path, width=45)
        entry_source.grid(row=0, column=1, padx=5, pady=5)

        btn_source = tk.Button(input_frame, text="Browse", command=self.select_source, width=10)
        btn_source.grid(row=0, column=2, padx=5, pady=5)

        # --- Target File ---
        lbl_target = tk.Label(input_frame, text="Target JSON:", width=12, anchor="w", font=("Arial", 10, "bold"))
        lbl_target.grid(row=1, column=0, pady=5)

        entry_target = tk.Entry(input_frame, textvariable=self.target_path, width=45)
        entry_target.grid(row=1, column=1, padx=5, pady=5)

        btn_target = tk.Button(input_frame, text="Browse", command=self.select_target, width=10)
        btn_target.grid(row=1, column=2, padx=5, pady=5)

        # 2. Options Area (New Checkbox)
        option_frame = tk.Frame(main_frame)
        option_frame.pack(fill=tk.X, pady=(10, 15))
        
        chk_delete = tk.Checkbutton(
            option_frame, 
            text="Delete keys in Target that are not in Source (Strict Sync)", 
            variable=self.delete_option,
            onvalue=True, 
            offvalue=False,
            font=("Arial", 10)
        )
        chk_delete.pack(anchor="w")

        # 3. Action Button
        btn_run = tk.Button(main_frame, text="Process & Save (to Target Folder)", 
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

            if not isinstance(source_data, dict) or not isinstance(target_data, dict):
                messagebox.showerror("Error", "Top-level structure must be a Dictionary (Object).")
                return

            added_count = 0
            deleted_count = 0

            # 1. Add missing keys (Source -> Target)
            for key in source_data.keys():
                if key not in target_data:
                    target_data[key] = ""
                    added_count += 1
            
            # 2. Delete extra keys (Target - Source) if Checkbox is selected
            if self.delete_option.get():
                # Identify keys to remove
                keys_to_remove = [k for k in target_data.keys() if k not in source_data]
                for k in keys_to_remove:
                    del target_data[k]
                    print(f"Deleted key: {k}")
                    deleted_count += 1

            # Generate output path
            target_dir = os.path.dirname(t_path)
            target_filename = os.path.basename(t_path)
            filename_no_ext = os.path.splitext(target_filename)[0]
            
            output_filename = f"{filename_no_ext}_integrated.json"
            output_path = os.path.join(target_dir, output_filename)

            # Write file
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(target_data, f, ensure_ascii=False, indent=4)

            # Success Message
            msg = f"Operation Complete!\n\n[Keys Added]: {added_count}"
            if self.delete_option.get():
                msg += f"\n[Keys Deleted]: {deleted_count}"
            msg += f"\n\n[Saved Path]: {output_path}"

            messagebox.showinfo("Success", msg)

        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonKeyMergerApp(root)
    root.mainloop()