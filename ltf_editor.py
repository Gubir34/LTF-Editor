import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import re

DARK_BG = "#486685"  # RGB 72,102,133

class LTFEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("LTF Editor")
        self.ltf_data = {}
        self.current_lang = None
        self.file_path = None
        self.dark_mode = False
        self.icon_label = None

        # Window icon
        try:
            self.icon = tk.PhotoImage(file="ltf.png")
            root.iconphoto(False, self.icon)
        except Exception as e:
            print("Icon not found:", e)

        # Top toolbar
        toolbar = ttk.Frame(root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="New File", command=self.new_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Open File", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Save File", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Toggle Dark Mode", command=self.toggle_theme).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="New Key", command=self.new_entry).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Key", command=self.delete_entry).pack(side=tk.LEFT, padx=2)
        ttk.Label(toolbar, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.refresh_key_tree())
        ttk.Entry(toolbar, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Paned window
        paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left: Language Radio Buttons
        self.lang_frame = ttk.Frame(paned, width=150)
        paned.add(self.lang_frame, weight=0)
        self.lang_var = tk.StringVar()

        # Middle: Key list
        key_frame = ttk.Frame(paned)
        paned.add(key_frame, weight=1)
        self.key_tree = ttk.Treeview(key_frame, columns=("key", "preview"), show="headings", selectmode="browse")
        self.key_tree.heading("key", text="Key")
        self.key_tree.heading("preview", text="Preview")
        self.key_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.key_tree.bind("<<TreeviewSelect>>", self.on_key_select)

        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.context_edit)
        self.context_menu.add_command(label="Rename", command=self.context_rename)
        self.context_menu.add_command(label="Delete", command=self.delete_entry)
        self.key_tree.bind("<Button-3>", self.show_context_menu)

        # Right: Translation editor
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)

        try:
            self.icon_img = tk.PhotoImage(file="ltf.png")
            self.icon_label = tk.Label(right_frame, image=self.icon_img, bg="white")
            self.icon_label.pack(pady=5)
        except Exception as e:
            print("Icon image not found:", e)

        self.text = tk.Text(right_frame, wrap=tk.WORD, bg="white", fg="black", insertbackground="black")
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text.bind("<Control-c>", lambda e: self.root.focus_get().event_generate("<<Copy>>"))
        self.text.bind("<Control-v>", lambda e: self.root.focus_get().event_generate("<<Paste>>"))
        self.text.bind("<Control-x>", lambda e: self.root.focus_get().event_generate("<<Cut>>"))

        # Shortcuts
        self.root.bind_all("<Control-s>", lambda e: self.save_file())
        self.root.bind_all("<Control-o>", lambda e: self.open_file())
        self.root.bind_all("<Control-n>", lambda e: self.new_file())

    # Context menu functions
    def show_context_menu(self, event):
        selected = self.key_tree.identify_row(event.y)
        if selected:
            self.key_tree.selection_set(selected)
            self.context_menu.post(event.x_root, event.y_root)

    def context_edit(self):
        selected = self.key_tree.selection()
        if not selected or not self.current_lang:
            return
        key = selected[0]
        value = self.ltf_data[self.current_lang][key]
        new_val = simpledialog.askstring("Edit Value", f"Edit value for {key}:", initialvalue=value)
        if new_val is not None:
            self.ltf_data[self.current_lang][key] = new_val
            self.refresh_key_tree()
            self.on_key_select(None)

    def context_rename(self):
        selected = self.key_tree.selection()
        if not selected or not self.current_lang:
            return
        old_key = selected[0]
        new_key = simpledialog.askstring("Rename Key", "New key name:", initialvalue=old_key)
        if new_key and new_key != old_key:
            self.ltf_data[self.current_lang][new_key] = self.ltf_data[self.current_lang].pop(old_key)
            self.refresh_key_tree()
            self.key_tree.selection_set(new_key)
            self.on_key_select(None)

    # Dark Mode
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        style = ttk.Style()
        if self.dark_mode:
            style.configure("Treeview", background=DARK_BG, foreground="white", fieldbackground=DARK_BG)
            style.map("Treeview", background=[('selected', '#575757')])
            style.configure("TLabel", background=DARK_BG, foreground="white")
            style.configure("TEntry", fieldbackground="#3e3e3e", foreground="white")
            style.configure("TButton", background="#3e3e3e", foreground="white")
            self.root.configure(bg=DARK_BG)
            self.text.configure(bg="#3e3e3e", fg="white", insertbackground="white")
            if self.icon_label:
                self.icon_label.configure(bg=DARK_BG)
        else:
            style.theme_use('default')
            self.root.configure(bg=None)
            self.text.configure(bg="white", fg="black", insertbackground="black")
            if self.icon_label:
                self.icon_label.configure(bg="white")

    # File operations
    def new_file(self):
        if messagebox.askyesno("New File", "Discard current changes and create new file?"):
            self.ltf_data = {}
            self.current_lang = None
            self.file_path = None
            self.refresh_lang_radio()
            self.refresh_key_tree()
            self.text.delete("1.0", tk.END)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("LTF Files", "*.ltf"), ("All Files", "*.*")])
        if not path:
            return
        self.file_path = path
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.parse_ltf(content)

    def save_file(self):
        if not self.file_path:
            path = filedialog.asksaveasfilename(defaultextension=".ltf", filetypes=[("LTF Files", "*.ltf")])
            if not path:
                return
            self.file_path = path
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("format = LTF\nversion = 1\n\n")
            for lang, entries in self.ltf_data.items():
                f.write(f"[lng={lang}]\n")
                for k, v in entries.items():
                    f.write(f"{k} = {v}\n")
                f.write("\n")
        messagebox.showinfo("Saved", f"{self.file_path} saved!")

    # Parsing
    def parse_ltf(self, content):
        self.ltf_data = {}
        current_lang = None
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            lang_match = re.match(r"\[lng=(.+?)\]", line)
            if lang_match:
                current_lang = lang_match.group(1)
                self.ltf_data[current_lang] = {}
            elif "=" in line and current_lang:
                key, value = line.split("=", 1)
                self.ltf_data[current_lang][key.strip()] = value.strip()
        self.refresh_lang_radio()

    # Language Radio Buttons
    def refresh_lang_radio(self):
        for widget in self.lang_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.lang_frame, text="Language:").pack(pady=5)
        for lang in self.ltf_data.keys():
            rb = ttk.Radiobutton(self.lang_frame, text=lang, variable=self.lang_var, value=lang, command=self.change_language)
            rb.pack(anchor="w", padx=5, pady=2)
        if self.ltf_data:
            first_lang = list(self.ltf_data.keys())[0]
            self.lang_var.set(first_lang)
            self.change_language()

    # Language & Tree Refresh
    def change_language(self):
        self.current_lang = self.lang_var.get()
        self.refresh_key_tree()

    def refresh_key_tree(self):
        self.key_tree.delete(*self.key_tree.get_children())
        if not self.current_lang:
            return
        entries = self.ltf_data[self.current_lang]
        filter_text = self.search_var.get().lower()
        for k, v in entries.items():
            if filter_text in k.lower() or filter_text in v.lower():
                preview = (v[:80] + "...") if len(v) > 80 else v
                self.key_tree.insert("", tk.END, iid=k, values=(k, preview))

    # Key selection
    def on_key_select(self, event):
        selected = self.key_tree.selection()
        if not selected or not self.current_lang:
            return
        key = selected[0]
        value = self.ltf_data[self.current_lang][key]
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, value)
        self.text.bind("<KeyRelease>", lambda e: self.update_value(key))

    def update_value(self, key):
        if self.current_lang and key in self.ltf_data[self.current_lang]:
            self.ltf_data[self.current_lang][key] = self.text.get("1.0", tk.END).rstrip("\n")
            self.refresh_key_tree()

    # Entry operations
    def new_entry(self):
        if not self.current_lang:
            return
        key = simpledialog.askstring("New Key", "Key name:")
        if not key:
            return
        value = simpledialog.askstring("Value", f"Value for {key}:")
        if value is not None:
            self.ltf_data[self.current_lang][key] = value
            self.refresh_key_tree()

    def delete_entry(self):
        selected = self.key_tree.selection()
        if not selected or not self.current_lang:
            return
        key = selected[0]
        if messagebox.askyesno("Delete", f"Delete {key}?"):
            del self.ltf_data[self.current_lang][key]
            self.refresh_key_tree()
            self.text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('default')
    app = LTFEditor(root)
    root.geometry("1200x600")
    root.mainloop()
