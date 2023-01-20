from tkinter import *
from tkinter import messagebox
from Rounding import Rounding

button_font = ('Arial', '28')  # TODO put in class

# TODO limit znaków, dopasowanie labeli do tekstu
# TODO? po pierwszym działaniu każda cyfra zmienia wynik?
# TODO ADD special_buttons
# TODO polish buttons

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title('Calculator')
        self.root.resizable(0, 0)

        self.gui_color = '#9DF1DF'

        self.proces = ' '

        self.display_frame = Frame(bg=self.gui_color)
        self.display_frame.pack(expand=True, fill=BOTH)

        self.proces_label = Label(self.display_frame, text=self.proces, bg=self.gui_color, font=button_font,
                                  width=15, anchor=E)
        self.proces_label.grid(row=0, column=0, columnspan=4)

        self.result_label = Label(self.display_frame, text=self.proces, bg=self.gui_color, font=button_font,
                                  width=10, anchor=E)
        self.result_label.grid(row=1, column=0, columnspan=3, sticky=EW)

        self.del_bt = Button(self.display_frame, text='B', width=4, borderwidth=0, font=button_font, command=self.back)
        self.del_bt.grid(row=1, column=3)

        self.button_frame = Frame(bg=self.gui_color)
        self.button_frame.pack(expand=True, fill=BOTH)

        self.buttons_list = [7, 8, 9, '/',
                             4, 5, 6, '*',
                             1, 2, 3, '-',
                             0, '.', '=', '+']

        self.create_buttons()
        self.special_buttons = {'**': 'x\u02b8', '**0.5': '\u221ax'}
        self.key_binding()

    def key_binding(self):
        self.root.bind('<Return>', lambda event: self.result())
        for key in self.buttons_list:
            self.root.bind(str(key), lambda event, digit=key: self.click(str(digit)))

    def round_up(self,value):
        pass

    def dot(self, val):  # doesn't work after backspace till beginning
        i = 0
        while True:
            if self.proces[-1 - i].isdigit():
                i += 1
            elif self.proces[-1 - i] == val:
                break
            else:
                self.proces += val
                self.proces_label.config(text=self.proces)
                break

    def add_digit(self, val):  # TODO add value
        self.proces += val
        self.proces_label.config(text=self.proces)

    def minus(self, val):
        if self.proces[-1].isdigit():
            self.result_label.config(text=str(eval(self.proces)))  # TODO def,
            self.proces += val
            self.proces_label.config(text=self.proces)
        else:  # TODO operational change, funkcja
            self.proces = self.proces[:-1]
            self.proces += val
            self.proces_label.config(text=self.proces)

    def result(self):  # TODO clearing proces, after inserting digit....
        if self.proces[-1].isdigit():
            try:
                self.proces = str(Rounding().result(eval(self.proces)))
                self.result_label.config(text=self.proces)
                self.proces_label.config(text=self.proces)
            except ZeroDivisionError:
                messagebox.showerror('Division Error', 'Cannot divide by zero')

    def click(self, val):
        if val.isdigit():  # TODO solve problem when 0 is 1st. digit
            self.add_digit(val)
        elif val == '.':
            if self.proces[-1].isdigit():
                self.dot(val)
        elif val == '-':
            self.minus(val)
        elif val == '=':  # TODO Result only after any operation?
            self.result()
        else:
            if self.proces != ' ':  # TODO def
                if self.proces[-1].isdigit():
                    try:
                        self.result_label.config(text=str(eval(self.proces)))
                        self.proces += val
                        self.proces_label.config(text=self.proces)
                    except ZeroDivisionError:
                        messagebox.showerror('Division Error', 'Cannot divide by zero')
                else:
                    if self.proces == '-':
                        pass
                    else:
                        self.proces = self.proces[:-1]
                        self.proces += val
                        self.proces_label.config(text=self.proces)

    def back(self):
        self.proces = self.proces[:-1]
        self.proces_label.config(text=self.proces)

    def clear(self):
        self.proces = ' '
        self.proces_label.config(text=self.proces)
        self.result_label.config(text=self.proces)

    def create_buttons(self):
        row_value = 0
        column_value = 0
        for i in self.buttons_list:
            button = Button(self.button_frame, text=str(i), bg=self.gui_color, font=button_font, borderwidth=0,
                            command=lambda x=str(i): self.click(x))
            button.grid(row=row_value, column=column_value, sticky=NSEW)
            column_value += 1
            if column_value == 4:
                row_value += 1
                column_value = 0

    # temp button
        self.backb = Button(self.button_frame, text='clear', command=self.clear)
        self.backb.grid(row=7, column=0)


if __name__ == '__main__':
    root = Tk()
    gui = Calculator(root)
    root.mainloop()
