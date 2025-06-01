import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
import os

# --- Constants ---
# Conversion factors to base units
# Base unit for Dry is gram (g)
DRY_UNITS_TO_BASE = {
    "g": 1.0,
    "oz (weight)": 28.3495,
    "lb": 453.592,
}
# Base unit for Liquid is milliliter (ml)
LIQUID_UNITS_TO_BASE = {
    "ml": 1.0,
    "fl oz (US)": 29.5735,
    "L": 1000.0,
    "cup (US fluid)": 236.588,
    "pint (US fluid)": 473.176,
    "quart (US fluid)": 946.353,
    "gallon (US fluid)": 3785.41,
}

# Units to display in output columns (and their conversion factor from the base unit)
# For Dry (base: g)
DRY_OUTPUT_UNITS = {
    "per g": 1.0,
    "per oz (weight)": DRY_UNITS_TO_BASE["oz (weight)"],  # grams per oz
    "per lb": DRY_UNITS_TO_BASE["lb"],          # grams per lb
}
# For Liquid (base: ml)
LIQUID_OUTPUT_UNITS = {
    "per ml": 1.0,
    "per fl oz (US)": LIQUID_UNITS_TO_BASE["fl oz (US)"],  # ml per fl oz
    "per L": LIQUID_UNITS_TO_BASE["L"],              # ml per L
}


class UnitCostCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Cost Calculator")
        self.root.geometry("900x700")  # Adjusted size

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Or 'alt', 'default', 'classic'

        self.session_unit_type = None  # "Dry" or "Liquid"
        self.session_title = "Untitled Session"  # Track session title
        self.input_rows_data = []  # Stores dicts of tk.Vars for each row
        self.input_row_frames = []  # Stores the Frame widget for each input row

        self._setup_ui()
        self.add_input_row(is_initial_row=True)  # Add the first row initially

    def _setup_ui(self):
        # --- Session Title Frame ---
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)

        ttk.Label(title_frame, text="Session:").pack(side=tk.LEFT, padx=5)
        self.session_title_label = ttk.Label(
            title_frame, text=self.session_title, font=("TkDefaultFont", 10, "bold"))
        self.session_title_label.pack(side=tk.LEFT, padx=5)

        # --- Controls Frame ---
        controls_frame = ttk.Frame(self.root, padding="10")
        controls_frame.pack(fill=tk.X)

        # File operations
        ttk.Button(controls_frame, text="Save Session",
                   command=self.save_session).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Load Session",
                   command=self.load_session).pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(controls_frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, padx=10, fill=tk.Y)

        self.add_row_button = ttk.Button(
            controls_frame, text="+ Add Product", command=self.add_input_row_button_action)
        self.add_row_button.pack(side=tk.LEFT, padx=5)
        # Disabled until session type is set
        self.add_row_button.config(state=tk.DISABLED)

        self.calculate_button = ttk.Button(
            controls_frame, text="Calculate & Compare", command=self.calculate_costs)
        self.calculate_button.pack(side=tk.LEFT, padx=5)
        self.calculate_button.config(state=tk.DISABLED)

        reset_button = ttk.Button(
            controls_frame, text="Reset All", command=self.reset_session)
        reset_button.pack(side=tk.LEFT, padx=5)

        # --- Input Area (Scrollable) ---
        input_area_container = ttk.Frame(self.root, padding="5")
        input_area_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(input_area_container)
        scrollbar = ttk.Scrollbar(
            input_area_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Results Area ---
        results_frame = ttk.Frame(self.root, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)

        results_frame.grid_columnconfigure(0, weight=1)  # Make Treeview expand
        results_frame.grid_rowconfigure(0, weight=1)    # Make Treeview expand

        self.results_tree = ttk.Treeview(results_frame, show='headings')
        # Use grid for Treeview
        self.results_tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar for Treeview (in case of many columns or long content)
        tree_ysb = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.results_tree.yview)
        tree_ysb.grid(row=0, column=1, sticky='ns')
        tree_xsb = ttk.Scrollbar(
            results_frame, orient="horizontal", command=self.results_tree.xview)
        tree_xsb.grid(row=1, column=0, sticky='ew')
        self.results_tree.configure(
            yscrollcommand=tree_ysb.set, xscrollcommand=tree_xsb.set)

    def _on_unit_type_selected(self, row_idx, is_initial_call=False):
        row_data = self.input_rows_data[row_idx]
        selected_type = row_data["unit_type_var"].get()

        if not selected_type:  # No selection yet
            row_data["unit_combobox"].set('')
            row_data["unit_combobox"].config(values=[], state=tk.DISABLED)
            return

        if self.session_unit_type is None:  # First time a type is selected in this session
            self.session_unit_type = selected_type
            # Lock this type for all existing and future rows
            for i, r_data in enumerate(self.input_rows_data):
                r_data["unit_type_var"].set(self.session_unit_type)
                r_data["unit_type_combobox"].config(
                    state=tk.DISABLED if i > 0 or not is_initial_call else tk.NORMAL)
            # Enable adding more rows
            self.add_row_button.config(state=tk.NORMAL)
            self.calculate_button.config(state=tk.NORMAL)  # Enable calculation

        elif selected_type != self.session_unit_type:
            # This case should ideally not happen if UI logic is correct
            messagebox.showerror(
                "Type Mismatch", f"Session is locked to '{self.session_unit_type}'. Please reset if you want to change types.")
            row_data["unit_type_var"].set(self.session_unit_type)  # Revert
            return

        # Update unit options for the current row
        if self.session_unit_type == "Dry":
            row_data["unit_combobox"].config(values=list(
                DRY_UNITS_TO_BASE.keys()), state='readonly')
        elif self.session_unit_type == "Liquid":
            row_data["unit_combobox"].config(values=list(
                LIQUID_UNITS_TO_BASE.keys()), state='readonly')
        else:
            row_data["unit_combobox"].config(values=[], state=tk.DISABLED)

        if not row_data["unit_var"].get() in row_data["unit_combobox"]["values"]:
            row_data["unit_combobox"].set('')

    def add_input_row(self, is_initial_row=False):
        row_idx = len(self.input_row_frames)
        row_frame = ttk.Frame(self.scrollable_frame, padding="5")
        row_frame.pack(fill=tk.X, pady=2)
        self.input_row_frames.append(row_frame)

        row_data = {
            "name_var": tk.StringVar(),
            "price_var": tk.StringVar(),
            "quantity_var": tk.StringVar(),
            "unit_type_var": tk.StringVar(),
            "unit_var": tk.StringVar(),
        }

        ttk.Label(row_frame, text=f"{row_idx+1}.",
                  width=3).pack(side=tk.LEFT, padx=2)

        ttk.Label(row_frame, text="Product:").pack(side=tk.LEFT, padx=2)
        name_entry = ttk.Entry(
            row_frame, textvariable=row_data["name_var"], width=20)
        name_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(row_frame, text="Price ($):").pack(side=tk.LEFT, padx=2)
        price_entry = ttk.Entry(
            row_frame, textvariable=row_data["price_var"], width=7)
        price_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(row_frame, text="Quantity:").pack(side=tk.LEFT, padx=2)
        qty_entry = ttk.Entry(
            row_frame, textvariable=row_data["quantity_var"], width=7)
        qty_entry.pack(side=tk.LEFT, padx=2)

        # Unit Type Combobox
        ttk.Label(row_frame, text="Type:").pack(side=tk.LEFT, padx=2)
        unit_type_cb = ttk.Combobox(row_frame, textvariable=row_data["unit_type_var"],
                                    values=["Dry", "Liquid"], width=7, state='readonly')
        unit_type_cb.pack(side=tk.LEFT, padx=2)
        row_data["unit_type_combobox"] = unit_type_cb
        # The lambda needs default arg for row_idx, or it will use the loop's last value
        unit_type_cb.bind("<<ComboboxSelected>>", lambda event, r_idx=row_idx: self._on_unit_type_selected(
            r_idx, is_initial_call=is_initial_row))

        # Unit Combobox
        ttk.Label(row_frame, text="Unit:").pack(side=tk.LEFT, padx=2)
        unit_cb = ttk.Combobox(
            row_frame, textvariable=row_data["unit_var"], width=15, state=tk.DISABLED)
        unit_cb.pack(side=tk.LEFT, padx=2)
        row_data["unit_combobox"] = unit_cb

        # Remove Button for the row (optional, but good UX)
        remove_button = ttk.Button(
            row_frame, text="-", command=lambda r_idx=row_idx: self.remove_input_row(r_idx), width=3)
        remove_button.pack(side=tk.LEFT, padx=2)
        # Store to potentially disable
        row_data["remove_button"] = remove_button

        self.input_rows_data.append(row_data)

        # If session type already set (i.e., not the very first row action)
        if self.session_unit_type:
            row_data["unit_type_var"].set(self.session_unit_type)
            unit_type_cb.config(state=tk.DISABLED)
            self._on_unit_type_selected(row_idx)  # Populate units
        elif not is_initial_row:  # Adding subsequent rows before type is selected
            # Keep disabled until first row sets type
            unit_type_cb.config(state=tk.DISABLED)

        if len(self.input_rows_data) == 1:  # Only one row
            remove_button.config(state=tk.DISABLED)
        elif len(self.input_rows_data) > 1 and self.input_rows_data[0]["remove_button"]["state"] == tk.DISABLED:
            # Enable remove for first row if another is added
            self.input_rows_data[0]["remove_button"].config(state=tk.NORMAL)

    def add_input_row_button_action(self):
        self.add_input_row(is_initial_row=False)

    def remove_input_row(self, row_idx_to_remove):
        if len(self.input_rows_data) <= 1:
            messagebox.showinfo(
                "Info", "Cannot remove the last row. Use Reset All instead.")
            return

        self.input_row_frames[row_idx_to_remove].destroy()
        del self.input_row_frames[row_idx_to_remove]
        del self.input_rows_data[row_idx_to_remove]

        # Re-label rows and update remove button commands and states
        for i, frame in enumerate(self.input_row_frames):
            # Update label (first child of frame is the index label)
            label_widget = frame.winfo_children()[0]
            label_widget.config(text=f"{i+1}.")
            # Update remove button command
            remove_button_widget = self.input_rows_data[i]["remove_button"]
            remove_button_widget.config(
                command=lambda r_idx=i: self.remove_input_row(r_idx))

        if len(self.input_rows_data) == 1:  # If back to one row
            self.input_rows_data[0]["remove_button"].config(state=tk.DISABLED)

        # Update scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def calculate_costs(self):
        if not self.session_unit_type:
            messagebox.showerror(
                "Error", "Please select a Unit Type for the first item.")
            return

        products_data = []
        valid_input_found = False

        for i, row_data_vars in enumerate(self.input_rows_data):
            name = row_data_vars["name_var"].get().strip()
            price_str = row_data_vars["price_var"].get()
            quantity_str = row_data_vars["quantity_var"].get()
            unit = row_data_vars["unit_var"].get()
            # Should be self.session_unit_type
            unit_type = row_data_vars["unit_type_var"].get()

            if not name and not price_str and not quantity_str and not unit:  # Skip entirely empty rows silently
                continue

            if not name:
                name = f"Product {i+1}"  # Default name

            try:
                price = float(price_str)
                quantity = float(quantity_str)
                if price < 0 or quantity <= 0:
                    raise ValueError(
                        "Price must be non-negative and quantity must be positive.")
                if not unit:
                    raise ValueError("Unit must be selected.")
            except ValueError as e:
                messagebox.showerror(
                    "Input Error", f"Row {i+1}: Invalid input for price, quantity, or unit.\nDetails: {e}")
                continue

            valid_input_found = True
            base_unit_conversion_map = DRY_UNITS_TO_BASE if unit_type == "Dry" else LIQUID_UNITS_TO_BASE

            if unit not in base_unit_conversion_map:
                messagebox.showerror(
                    "Error", f"Row {i+1}: Unit '{unit}' is not recognized for type '{unit_type}'.")
                continue

            qty_in_base_unit = quantity * base_unit_conversion_map[unit]
            price_per_base_unit = price / qty_in_base_unit

            products_data.append({
                "name": name,
                "original_price": price,
                "original_quantity": quantity,
                "original_unit": unit,
                "unit_type": unit_type,
                "price_per_base_unit": price_per_base_unit
            })

        if not valid_input_found:
            messagebox.showinfo(
                "Info", "No valid product data entered to calculate.")
            # Clear previous results if any
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            self.results_tree["columns"] = []
            return

        if not products_data:  # Handles case where rows had partial data but failed validation
            return

        # Sort by price_per_base_unit (best value first)
        products_data.sort(key=lambda p: p["price_per_base_unit"])

        # Display results
        self._display_results(products_data)

    def _display_results(self, products_data):
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        if not products_data:
            self.results_tree["columns"] = []
            return

        # Define columns based on session type
        common_cols = ["Product", "Orig. Price", "Orig. Qty", "Orig. Unit"]
        if self.session_unit_type == "Dry":
            output_unit_cols = list(DRY_OUTPUT_UNITS.keys())
            price_format_precision = {"per g": 5,
                                      "per oz (weight)": 4, "per lb": 2}
            output_units_map = DRY_OUTPUT_UNITS
        else:  # Liquid
            output_unit_cols = list(LIQUID_OUTPUT_UNITS.keys())
            price_format_precision = {"per ml": 5,
                                      "per fl oz (US)": 4, "per L": 2}
            output_units_map = LIQUID_OUTPUT_UNITS

        all_cols = common_cols + \
            [f"$ {col_name}" for col_name in output_unit_cols]
        self.results_tree["columns"] = all_cols

        for col_name in all_cols:
            self.results_tree.heading(col_name, text=col_name)
            self.results_tree.column(col_name, anchor=tk.W, width=100 if col_name not in [
                                     "Product", "Orig. Unit"] else 150)
            if col_name == "Product":
                self.results_tree.column(col_name, width=180)
            if "Orig." in col_name:
                self.results_tree.column(col_name, anchor=tk.E, width=80)
            if "$" in col_name:
                self.results_tree.column(col_name, anchor=tk.E, width=100)

        for i, product in enumerate(products_data):
            values = [
                product["name"],
                f"${product['original_price']:.2f}",
                f"{product['original_quantity']}",
                product["original_unit"]
            ]
            for unit_name, factor_from_base in output_units_map.items():
                # price_per_output_unit = price_per_base_unit * base_units_per_output_unit
                price_val = product["price_per_base_unit"] * factor_from_base
                precision = price_format_precision.get(unit_name, 2)
                values.append(f"${price_val:.{precision}f}")

            tag = "best_buy" if i == 0 else "normal"
            self.results_tree.tag_configure(
                "best_buy", background="lightgreen")
            self.results_tree.insert("", tk.END, values=values, tags=(tag,))

    def save_session(self):
        if not self.input_rows_data:
            messagebox.showinfo("Info", "No data to save.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            title="Save Session"
        )

        if not filename:
            return

        try:
            # Create XML structure
            root_elem = ET.Element("session")

            # Add session title (filename without path and extension)
            title_elem = ET.SubElement(root_elem, "title")
            title_elem.text = os.path.splitext(os.path.basename(filename))[0]

            # Add unit type
            if self.session_unit_type:
                unit_type_elem = ET.SubElement(root_elem, "unit_type")
                unit_type_elem.text = self.session_unit_type

            # Add products
            products_elem = ET.SubElement(root_elem, "products")

            for row_data in self.input_rows_data:
                # Only save rows with some data
                if (row_data["name_var"].get().strip() or
                    row_data["price_var"].get().strip() or
                        row_data["quantity_var"].get().strip()):

                    product_elem = ET.SubElement(products_elem, "product")

                    name_elem = ET.SubElement(product_elem, "name")
                    name_elem.text = row_data["name_var"].get().strip()

                    price_elem = ET.SubElement(product_elem, "price")
                    price_elem.text = row_data["price_var"].get().strip()

                    quantity_elem = ET.SubElement(product_elem, "quantity")
                    quantity_elem.text = row_data["quantity_var"].get().strip()

                    unit_type_elem = ET.SubElement(product_elem, "unit_type")
                    unit_type_elem.text = row_data["unit_type_var"].get()

                    unit_elem = ET.SubElement(product_elem, "unit")
                    unit_elem.text = row_data["unit_var"].get()

            # Write to file
            tree = ET.ElementTree(root_elem)
            ET.indent(tree, space="  ", level=0)  # Pretty formatting
            tree.write(filename, encoding="utf-8", xml_declaration=True)

            # Update session title
            self.session_title = os.path.splitext(
                os.path.basename(filename))[0]
            self.session_title_label.config(text=self.session_title)

            messagebox.showinfo("Success", f"Session saved as '{filename}'")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session:\n{str(e)}")

    def load_session(self):
        # Warning dialog if there's existing data
        if self.input_rows_data and any(
            row_data["name_var"].get().strip() or
            row_data["price_var"].get().strip() or
            row_data["quantity_var"].get().strip()
            for row_data in self.input_rows_data
        ):
            result = messagebox.askyesnocancel(
                "Warning",
                "Loading a session will replace all current data.\n\nDo you want to continue?",
                icon=messagebox.WARNING
            )
            if result != True:  # User clicked No or Cancel
                return

        filename = filedialog.askopenfilename(
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            title="Load Session"
        )

        if not filename:
            return

        try:
            # Parse XML
            tree = ET.parse(filename)
            root_elem = tree.getroot()

            if root_elem.tag != "session":
                messagebox.showerror("Error", "Invalid session file format.")
                return

            # Clear current session
            self.reset_session()

            # Load session title
            title_elem = root_elem.find("title")
            if title_elem is not None and title_elem.text:
                self.session_title = title_elem.text
            else:
                self.session_title = os.path.splitext(
                    os.path.basename(filename))[0]
            self.session_title_label.config(text=self.session_title)

            # Load unit type
            unit_type_elem = root_elem.find("unit_type")
            if unit_type_elem is not None and unit_type_elem.text:
                self.session_unit_type = unit_type_elem.text

            # Load products
            products_elem = root_elem.find("products")
            if products_elem is not None:
                products = products_elem.findall("product")

                if not products:
                    # No products, keep the initial empty row
                    if self.session_unit_type:
                        # Set the unit type for the initial row
                        self.input_rows_data[0]["unit_type_var"].set(
                            self.session_unit_type)
                        self._on_unit_type_selected(0, is_initial_call=True)
                        self.add_row_button.config(state=tk.NORMAL)
                        self.calculate_button.config(state=tk.NORMAL)
                else:
                    # Remove the initial empty row first
                    if self.input_rows_data:
                        self.input_row_frames[0].destroy()
                        del self.input_row_frames[0]
                        del self.input_rows_data[0]

                    # Add rows for each product
                    for i, product_elem in enumerate(products):
                        is_first = (i == 0)
                        self.add_input_row(is_initial_row=is_first)
                        row_data = self.input_rows_data[-1]

                        # Load product data
                        name_elem = product_elem.find("name")
                        if name_elem is not None and name_elem.text:
                            row_data["name_var"].set(name_elem.text)

                        price_elem = product_elem.find("price")
                        if price_elem is not None and price_elem.text:
                            row_data["price_var"].set(price_elem.text)

                        quantity_elem = product_elem.find("quantity")
                        if quantity_elem is not None and quantity_elem.text:
                            row_data["quantity_var"].set(quantity_elem.text)

                        unit_type_elem = product_elem.find("unit_type")
                        if unit_type_elem is not None and unit_type_elem.text:
                            row_data["unit_type_var"].set(unit_type_elem.text)

                        unit_elem = product_elem.find("unit")
                        if unit_elem is not None and unit_elem.text:
                            row_data["unit_var"].set(unit_elem.text)

                        # Trigger unit type selection to set up the units dropdown
                        if is_first and self.session_unit_type:
                            self._on_unit_type_selected(
                                len(self.input_rows_data) - 1, is_initial_call=True)

            # Enable buttons if we have a session type
            if self.session_unit_type:
                self.add_row_button.config(state=tk.NORMAL)
                self.calculate_button.config(state=tk.NORMAL)

            # Auto-calculate if we have valid data
            self.calculate_costs()

            messagebox.showinfo(
                "Success", f"Session '{self.session_title}' loaded successfully!")

        except ET.ParseError as e:
            messagebox.showerror(
                "Error", f"Failed to parse XML file:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session:\n{str(e)}")

    def reset_session(self):
        # Clear input rows
        for frame in self.input_row_frames:
            frame.destroy()
        self.input_row_frames.clear()
        self.input_rows_data.clear()

        # Clear results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results_tree["columns"] = []

        # Reset session state
        self.session_unit_type = None
        self.session_title = "Untitled Session"
        self.session_title_label.config(text=self.session_title)
        self.add_row_button.config(state=tk.DISABLED)
        self.calculate_button.config(state=tk.DISABLED)

        # Add one initial blank row
        self.add_input_row(is_initial_row=True)


if __name__ == "__main__":
    main_root = tk.Tk()
    app = UnitCostCalculatorApp(main_root)
    main_root.mainloop()
