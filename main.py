from tkinter import *
from tkinter import messagebox
from RoundingMethod import RoundingMethod
from functools import partial
from typing import Union

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title('Calculator')
        self.root.geometry('350x450')
        self.root.resizable(0, 0)

        self.gui_color = '#9DF1DF'
        self.button_font = ('Arial', '28')
        self.result_font = ('Arial', '16')
        self.arrow_image = PhotoImage(file='back_arrow.png')

        self.proces = ''
        self.equal_pressed = False
        self.e_notation = False

        self.display_frame = Frame(bg=self.gui_color)
        self.display_frame.pack(expand=True, fill=BOTH)

        self.proces_text = Text(self.display_frame, bg=self.gui_color, font=self.button_font, height=1, wrap=WORD,
                                width=45)
        self.proces_text.grid(row=0, column=0, columnspan=8, sticky='NEWS')

        self.result_label = Label(self.display_frame, text=self.proces, bg=self.gui_color, font=self.result_font,
                                  anchor=E)
        self.result_label.grid(row=1, column=1, columnspan=6, sticky='NEWS')

        self.clear_button = Button(self.display_frame, text='C', bg=self.gui_color, font=self.button_font,
                                   borderwidth=0, command=self.clear)
        self.clear_button.grid(row=1, column=0, sticky='W')

        self.back_button = Button(self.display_frame, image=self.arrow_image, activebackground=self.gui_color,
                                  bg=self.gui_color, borderwidth=0, font=self.button_font, command=self.back)
        self.back_button.grid(row=1, column=7, sticky='E')

        self.button_frame = Frame(bg=self.gui_color)
        self.button_frame.pack(expand=True, fill=BOTH)

        self.buttons_list = {7 : '7', 8 : '8', 9 : '9', '\u00F7' : '/',
                             4 : '4', 5 : '5', 6 : '6', '\u00D7' : '*' ,
                             1 : '1', 2 : '2', 3 : '3', '-' : '-',
                             0 : '0', '.' : '.', '=' : '=', '+' : '+'}

        self.operators = {'/': '\u00F7', '*': '\u00D7'}

        self.create_buttons()
        self.grid_configure(self.display_frame)
        self.grid_configure(self.button_frame)
        self.key_binding()

    @staticmethod
    def grid_configure(frame):
        columns, rows = frame.grid_size()
        for i in range(rows):
            frame.rowconfigure(i, weight=1)
        for i in range(columns):
            frame.columnconfigure(i, weight=1)

    def key_binding(self):
        self.root.bind('<Return>', lambda event: self.result())
        self.root.bind('<BackSpace>', lambda event: self.back())
        for key in self.buttons_list:
            self.root.bind(str(key), lambda event, digit=key: self.click(str(digit)))

    def update_proces_text(self):
        expression = self.proces
        for operator, symbol in self.operators.items():
            expression = expression.replace(operator, f'{symbol}')
        self.proces_text.delete(1.0, END)
        self.proces_text.insert(END, expression)
        self.proces_text.tag_configure('right', justify='right')
        self.proces_text.tag_add('right', '1.0', 'end')

    @staticmethod
    def result_length_limit(value: str) -> bool:
        if len(value) > 12 and '.' not in value:
            return True
        elif len(value) > 13 and '.' in value:
            return True
        else:
            return False

    def to_scientific_notation(self, value: str) ->str:
        if self.result_length_limit(value):
            self.e_notation = True
            return '{:.2e}'.format(int(value))
        else:
            return value

    def add_value(self, val):
        self.proces += val
        self.update_proces_text()
        self.equal_pressed = False

    def find_last_math_sign(self) -> Union[int, None]:
        i = len(self.proces) - 1
        while i >= 0:
            if self.proces[i] in "+-*/%":
                return i
            i -= 1
        return None

    def leading_zero_check(self) -> bool:
        if len(self.proces) == 1 and self.proces[0] == '0':
            return True
        index = self.find_last_math_sign()
        if index is None:
            return False
        z = len(self.proces[index + 1:])
        if z == 1 and self.proces[index + 1] == '0':
            return True

    def operational_change(self, val):
        self.proces = self.proces[:-1]
        self.add_value(val)

    def add_number(self, value):
        if self.equal_pressed or self.e_notation:
            self.clear()
        else:
            if self.leading_zero_check():
                self.proces = self.proces[:-1]
        self.add_value(value)

    def add_dot(self,val):
        if not self.proces:
            return
        index = self.find_last_math_sign()
        if index is None:
            expression = self.proces
        else:
            expression = self.proces[index + 1]
        if val not in expression and self.proces[-1].isdigit():
            self.add_value(val)

    def result(self):
        if self.proces and self.proces[-1].isdigit():
            try:
                expression = str(RoundingMethod().result(eval(self.proces)))
                self.proces = self.to_scientific_notation(expression)
                self.result_label.config(text=self.proces)
                self.update_proces_text()
                self.equal_pressed = True
            except ZeroDivisionError:
                messagebox.showerror('Division Error', 'Cannot divide by zero')

    def add_operation(self,value):
        if not self.proces:
            if value == '-':
                self.operational_change(value)
            else:
                return
        if self.proces[-1].isdigit():
            try:
                expression = str(RoundingMethod().result(eval(self.proces)))
                self.result_label.config(text=self.to_scientific_notation(expression))
                self.proces += value
                self.update_proces_text()
                self.equal_pressed = False
                self.e_notation = False
            except ZeroDivisionError:
                messagebox.showerror('Division Error', 'Cannot divide by zero')
        else:
            if len(self.proces) == 1:
                return
            else:
                self.operational_change(value)

    def click(self, val):
        if val.isdigit():
            self.add_number(val)
        elif val == '.':
            self.add_dot(val)
        elif val == '=':
            self.result()
        else:
            self.add_operation(val)

    def back(self):
        if self.e_notation:
            return self.clear()
        self.proces = self.proces[:-1]
        self.update_proces_text()
        self.equal_pressed = False

    def clear(self):
        self.proces = ''
        self.proces_text.delete(1.0, END)
        self.result_label.config(text=self.proces)
        self.equal_pressed = False
        self.e_notation = False

    def create_buttons(self):
        _ = 0
        for symbol, operator in self.buttons_list.items():
            button = Button(self.button_frame, text=symbol, bg=self.gui_color, font=self.button_font, borderwidth=0,
                            command= partial(self.click,operator))
            button.grid(row=_//4, column=_%4, sticky='NSEW')
            _ += 1


if __name__ == '__main__':
    root = Tk()
    gui = Calculator(root)
    root.mainloop()
