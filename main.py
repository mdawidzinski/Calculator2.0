import sys
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

        self.process = ''  # variable for holding all inputs
        self.equal_pressed = False  # check if result() was executed
        self.e_notation = False  # check if result() was executed and e notation was used

        self.display_frame = Frame(bg=self.gui_color)  # frame to display calculation and result
        self.display_frame.pack(expand=True, fill=BOTH)

        self.process_text = Text(self.display_frame, bg=self.gui_color, font=self.button_font, height=1, wrap=WORD,
                                 width=45)  # main widget for calculation display
        self.process_text.grid(row=0, column=0, columnspan=8, sticky='NEWS')

        self.result_label = Label(self.display_frame, text=self.process, bg=self.gui_color, font=self.result_font,
                                  anchor=E)  # label for result display
        self.result_label.grid(row=1, column=1, columnspan=6, sticky='NEWS')

        self.clear_button = Button(self.display_frame, text='C', bg=self.gui_color, font=self.button_font,
                                   borderwidth=0, command=self.clear)  # button for clearing previous widgets
        self.clear_button.grid(row=1, column=0, sticky='W')

        self.back_button = Button(self.display_frame, image=self.arrow_image, activebackground=self.gui_color,
                                  bg=self.gui_color, borderwidth=0, font=self.button_font, command=self.back)
        # button that remove last inputted value or clear everything when self.e_notation = True
        self.back_button.grid(row=1, column=7, sticky='E')

        self.button_frame = Frame(bg=self.gui_color)  # frame for buttons
        self.button_frame.pack(expand=True, fill=BOTH)
        # button dictionary used for button creation and key binding
        self.buttons_list = {7: '7', 8: '8', 9: '9', '\u00F7': '/',
                             4: '4', 5: '5', 6: '6', '\u00D7': '*',
                             1: '1', 2: '2', 3: '3', '-': '-',
                             0: '0', '.': '.', '=': '=', '+': '+'}

        self.operators = {'/': '\u00F7', '*': '\u00D7'}  # button dictionary used for replace signs in proces_text

        self.create_buttons()
        self.grid_configure(self.display_frame)
        self.grid_configure(self.button_frame)
        self.key_binding()

    @staticmethod
    def grid_configure(frame):  # function allows to configure widget weight inside of frame.
        columns, rows = frame.grid_size()  # frame.grid_size() automatically check how any rows and column is in frame
        for i in range(rows):
            frame.rowconfigure(i, weight=1)
        for i in range(columns):
            frame.columnconfigure(i, weight=1)

    def key_binding(self):  # key binding function
        self.root.bind('<Return>', lambda event: self.result())
        self.root.bind('<BackSpace>', lambda event: self.back())
        self.root.bind('<Escape>', lambda event: sys.exit())
        for key in self.buttons_list:
            self.root.bind(str(key), lambda event, digit=key: self.click(str(digit)))

    def update_process_text(self):  # function used to update proces_text
        expression = self.process
        for operator, symbol in self.operators.items():  # conversion operators / and * to unicode symbols
            expression = expression.replace(operator, f'{symbol}')
        '''commands bellow are used to input text from right to left'''
        self.process_text.delete(1.0, END)
        self.process_text.insert(END, expression)
        self.process_text.tag_configure('right', justify='right')
        self.process_text.tag_add('right', '1.0', 'end')

    @staticmethod
    def result_length_limit(value: str) -> bool:  # check if operation result is longer than space in result_label
        if len(value) > 12 and '.' not in value:
            return True
        elif len(value) > 13 and '.' in value:
            return True
        else:
            return False

    def to_scientific_notation(self, value: str) -> str:
        """Function that convert result to e notation with 2 decimal paces"""
        if self.result_length_limit(value):
            self.e_notation = True
            return '{:.2e}'.format(int(value))
        else:
            return value

    def add_value(self, val):  # adding value to self.proces and proces_text
        self.process += val
        self.update_process_text()
        self.equal_pressed = False

    def find_last_math_sign(self) -> Union[int, None]:  # check for index of last math sign or return None
        i = len(self.process) - 1
        while i >= 0:
            if self.process[i] in "+-*/":
                return i
            i -= 1
        return None

    def leading_zero_check(self) -> bool:  # leading zero checker
        if len(self.process) == 1 and self.process[0] == '0':
            return True
        index = self.find_last_math_sign()
        if index is None:
            return False
        z = len(self.process[index + 1:])
        if z == 1 and self.process[index + 1] == '0':
            return True
        # TODO What to do in else situation

    def operational_change(self, val):  # allowing change sign, eg. from + to -
        self.process = self.process[:-1]
        self.add_value(val)

    def add_number(self, value):  # adding number to self.proces and proces_text.
        if self.equal_pressed:
            self.clear()  # clearing everything when statement is True.
        else:
            if self.leading_zero_check():  # remove leading zero
                self.process = self.process[:-1]
        self.add_value(value)

    def add_dot(self, val):   # adding dot to a number
        if not self.process:
            return
        index = self.find_last_math_sign()
        if index is None:
            expression = self.process
        else:
            expression = self.process[index + 1]
        if val not in expression and self.process[-1].isdigit():
            self.add_value(val)
        # TODO What to do in else situation

    def result(self):  # function that trigger after pressing =
        if self.process and self.process[-1].isdigit():
            try:  # divide by zero error check
                expression = str(RoundingMethod().result(eval(self.process)))
                self.process = self.to_scientific_notation(expression)
                self.result_label.config(text=self.process)
                self.update_process_text()
                self.equal_pressed = True
            except ZeroDivisionError:
                messagebox.showerror('Division Error', 'Cannot divide by zero')

    def add_operation(self, value):  # function that handle math sign input
        if not self.process:  # allowing - as first input
            if value == '-':
                self.operational_change(value)
            else:
                return
        if self.process[-1].isdigit():
            try:  # divide by zero error check
                expression = str(RoundingMethod().result(eval(self.process)))
                self.result_label.config(text=self.to_scientific_notation(expression))  # result_label update
                self.process += value
                self.update_process_text()
                self.equal_pressed = False
                self.e_notation = False
            except ZeroDivisionError:
                messagebox.showerror('Division Error', 'Cannot divide by zero')
        else:
            if len(self.process) == 1:  # block operational_change when there is only - in self.proces
                return
            else:
                self.operational_change(value)

    def click(self, val):  # handle input from keys
        if val.isdigit():
            self.add_number(val)
        elif val == '.':
            self.add_dot(val)
        elif val == '=':
            self.result()
        else:
            self.add_operation(val)

    def back(self):  # removing last value
        if self.e_notation:  # clearing everything when e_notation = True, this prevents errors.
            return self.clear()
        self.process = self.process[:-1]
        self.update_process_text()
        self.equal_pressed = False

    def clear(self):  # clearing everything and set both self.equal_pressed and self.e_notation to false
        self.process = ''
        self.process_text.delete(1.0, END)
        self.result_label.config(text=self.process)
        self.equal_pressed = False
        self.e_notation = False

    def create_buttons(self):  # creating all buttons at the same time
        _ = 0
        for symbol, operator in self.buttons_list.items():
            button = Button(self.button_frame, text=symbol, bg=self.gui_color, font=self.button_font, borderwidth=0,
                            command=partial(self.click, operator))
            button.grid(row=_//4, column=_ % 4, sticky='NSEW')
            _ += 1


if __name__ == '__main__':
    root = Tk()
    gui = Calculator(root)
    root.mainloop()
