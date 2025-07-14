import tkinter as tk
import math

# Define some colors for consistency
COLOR_PRIMARY = "#4CAF50"  # A nice green
COLOR_ACCENT = "#FFC107"  # Amber
COLOR_NUMBER = "#FAFAFA"  # Off-white
COLOR_OPERATOR = "#E0E0E0"  # Light gray
COLOR_SPECIAL = "#FF5722"  # Deep Orange for 'C' and '='
COLOR_TEXT_DARK = "#212121"  # Dark gray for text
COLOR_TEXT_LIGHT = "#FFFFFF"  # White for text


class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("300x450")  # Increased height
        master.resizable(False, False)
        master.configure(bg=COLOR_TEXT_DARK)

        self.display_var = tk.StringVar()
        self.display_var.set("0")

        self.after_equals_or_error = False

        self._create_display()
        self._create_buttons()
        # Keyboard input remains commented out
        # self._bind_keyboard_events()

    def _create_display(self):
        self.entry_field = tk.Entry(
            self.master,
            textvariable=self.display_var,
            font=('Arial', 28, 'bold'),
            bd=10,
            insertwidth=4,
            justify='right',
            relief='flat',
            bg=COLOR_TEXT_DARK,
            fg=COLOR_PRIMARY,
            insertbackground=COLOR_PRIMARY
        )
        self.entry_field.pack(pady=15, padx=15, fill=tk.X)

    def _create_buttons(self):
        button_frame = tk.Frame(self.master, bg=COLOR_TEXT_DARK)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Modified layout: Add '0' to the top row between '^' and 'sqrt'
        button_layout = [
            ['^', '0', 'sqrt', ''],  # '0' button re-added here

            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['AC', 'DEL', '=', '+']
        ]

        num_rows = len(button_layout)
        num_cols = len(button_layout[0])

        for row_index, row_buttons in enumerate(button_layout):
            for col_index, button_text in enumerate(row_buttons):
                if not button_text:
                    continue

                btn_bg = COLOR_NUMBER
                btn_fg = COLOR_TEXT_DARK
                btn_active_bg = "#E0E0E0"

                if button_text in ['/', '*', '-', '+', '^']:
                    btn_bg = COLOR_OPERATOR
                    btn_fg = COLOR_TEXT_DARK
                    btn_active_bg = "#BDBDBD"
                elif button_text in ['AC', 'DEL', 'sqrt']:
                    btn_bg = COLOR_SPECIAL
                    btn_fg = COLOR_TEXT_LIGHT
                    btn_active_bg = "#D84315"
                elif button_text == '=':
                    btn_bg = COLOR_PRIMARY
                    btn_fg = COLOR_TEXT_LIGHT
                    btn_active_bg = "#388E3C"
                elif button_text == '.':  # If we re-add '.' later
                    btn_bg = COLOR_NUMBER
                    btn_fg = COLOR_TEXT_DARK
                    btn_active_bg = "#E0E0E0"
                # Else it will default to COLOR_NUMBER, which is correct for '0' and other digits

                button = tk.Button(
                    button_frame,
                    text=button_text,
                    font=('Arial', 18, 'bold'),
                    bg=btn_bg,
                    fg=btn_fg,
                    activebackground=btn_active_bg,
                    activeforeground=btn_fg,
                    relief='flat',
                    bd=1,
                    command=lambda b=button_text: self.button_click(b)
                )
                button.grid(row=row_index, column=col_index, padx=3, pady=3, sticky=tk.NSEW)

        for i in range(num_cols):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(num_rows):
            button_frame.grid_rowconfigure(i, weight=1)

    def button_click(self, char):
        current_display = self.display_var.get()
        operators = ['/', '*', '-', '+', '^']

        if char == 'AC':
            self.display_var.set("0")
            self.after_equals_or_error = False
            return

        elif char == 'DEL':
            if self.after_equals_or_error or current_display.startswith("Error"):
                self.display_var.set("0")
                self.after_equals_or_error = False
            elif len(current_display) > 1:
                self.display_var.set(current_display[:-1])
            else:
                self.display_var.set("0")
            return

        elif char == 'sqrt':
            try:
                value = float(current_display)
                if value < 0:
                    self.display_var.set("Error: Neg sqrt")
                else:
                    result = str(math.sqrt(value))
                    if '.' in result and len(result.split('.')[1]) > 5:
                        result = f"{float(result):.5f}"
                    self.display_var.set(result)
                self.after_equals_or_error = True
            except ValueError:
                self.display_var.set("Error: Invalid Input")
                self.after_equals_or_error = True
            except Exception:
                self.display_var.set("Error")
                self.after_equals_or_error = True
            return

        elif char == '=':
            try:
                expression_to_eval = current_display.replace('^', '**')
                result = str(eval(expression_to_eval))
                self.display_var.set(result)
                self.after_equals_or_error = True
            except ZeroDivisionError:
                self.display_var.set("Error: Div by 0")
                self.after_equals_or_error = True
            except (SyntaxError, NameError):
                self.display_var.set("Error: Invalid Expr")
                self.after_equals_or_error = True
            except Exception:
                self.display_var.set("Error")
                self.after_equals_or_error = True
            return

        # Common input handling for numbers and operators (including '^')
        if self.after_equals_or_error or current_display.startswith("Error"):
            if char.isdigit() or char == '.':
                self.display_var.set(char)
            elif char in operators:
                if current_display.startswith("Error"):
                    if char == '^':
                        self.display_var.set("Error: Invalid Start")
                    else:
                        self.display_var.set("0" + char)
                else:
                    self.display_var.set(current_display + ('**' if char == '^' else char))
            self.after_equals_or_error = False
            return

        # Handle '0' as initial input
        # Note: This block handles a fresh '0' input, not when '0' is part of a multi-digit number
        if current_display == "0":
            if char.isdigit() and char != '0':  # If input is '1'-'9', replace '0' with it
                self.display_var.set(char)
            elif char == '.':  # If input is '.', make it "0."
                self.display_var.set("0.")
            elif char in operators:  # If input is an operator, allow "0+" etc. (but not '0^')
                if char == '^':
                    return  # Cannot start with ^
                self.display_var.set(current_display + char)
            # If char is '0' and display is '0', do nothing (prevents "00")
            return

            # Handle decimal point logic
        if char == '.':
            last_number_segment = ""
            last_op_index = -1
            temp_display = current_display.replace('**', '^')  # Temporarily replace ** to match '^'
            for op in operators:
                op_index = temp_display.rfind(op)
                if op_index > last_op_index:
                    last_op_index = op_index

            if last_op_index != -1:
                last_number_segment = current_display[last_op_index + 1:]
            else:
                last_number_segment = current_display

            if '.' in last_number_segment:
                return

        # Handle operators
        if char in operators:
            last_two_chars = current_display[-2:] if len(current_display) >= 2 else ""
            if last_two_chars == '**' or (current_display and current_display[-1] in ['/', '*', '-', '+']):
                if last_two_chars == '**':
                    self.display_var.set(current_display[:-2] + ('**' if char == '^' else char))
                else:
                    self.display_var.set(current_display[:-1] + ('**' if char == '^' else char))
                return

            if current_display == "" and char != '-':
                return

            if char == '^' and (current_display == "" or current_display[-1] in operators):
                self.display_var.set("Error: Invalid Start")
                self.after_equals_or_error = True
                return

        # Default: append the character or '**' for '^'
        self.display_var.set(current_display + ('**' if char == '^' else char))


# --- Main part of the script ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()