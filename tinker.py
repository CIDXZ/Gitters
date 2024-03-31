import tkinter as tk

window = tk.Tk()
window.title("Simple Calc")
window.geometry("450x350")

operand1 = ""
operand2 = ""
operation = ""

def new_entry(new_value):
    existing_value = entry.get()
    new_value = existing_value + new_value
    entry.delete(0,'end')
    entry.insert(0, new_value)

def oper(op):
    global operand1 
    global operation
    operand1 = entry.get()
    entry.delete(0,'end')
    operation = op


def ans():
    global operand1, operand2, operation

    operand2 = entry.get()
    entry.delete(0,'end')

    if operation == "+":
        result = int(operand1) + int(operand2)
        entry.insert(0, result)
    if operation == "-":
        result = int(operand1) - int(operand2)
        entry.insert(0, result)
    if operation == "*":
        result = int(operand1) * int(operand2)
        entry.insert(0, result)
    if operation == "/":
        result = int(operand1) / int(operand2)
        entry.insert(0, result)
    
def all_clear():
    entry.delete(0,'end')

entry = tk.Entry(window, width = 25, font = ("Arial 20"))
entry.place(x = 50, y = 50)

button1 = tk.Button(window, text = "1", fg = "blue", command = lambda : new_entry("1"))
button1.place(x = 100, y = 100)

button2 = tk.Button(window, text = "2", fg = "blue", command = lambda : new_entry("2"))
button2.place(x = 150, y = 100)

button3 = tk.Button(window, text = "3", fg = "blue", command = lambda : new_entry("3"))
button3.place(x = 200, y = 100)

button4 = tk.Button(window, text = "+", fg = "green", command = lambda : oper("+"))
button4.place(x = 250, y = 100)

button5 = tk.Button(window, text = "4", fg = "blue", command = lambda : new_entry("4"))
button5.place(x = 100, y = 130)

button6 = tk.Button(window, text = "5", fg = "blue", command = lambda : new_entry("5"))
button6.place(x = 150, y = 130)

button7 = tk.Button(window, text = "6", fg = "blue", command = lambda : new_entry("6"))
button7.place(x = 200, y = 130)

button8 = tk.Button(window, text = "-", fg = "green", command = lambda : oper("-"))
button8.place(x = 250, y = 130)

button9 = tk.Button(window, text = "7", fg = "blue", command = lambda : new_entry("7"))
button9.place(x = 100, y = 160)

button10 = tk.Button(window, text = "8", fg = "blue", command = lambda : new_entry("8"))
button10.place(x = 150, y = 160)

button11 = tk.Button(window, text = "9", fg = "blue", command = lambda : new_entry("9"))
button11.place(x = 200, y = 160)

button12 = tk.Button(window, text = "*", fg = "green", command = lambda : oper("*"))
button12.place(x = 250, y = 160)

button13 = tk.Button(window, text = "AC", fg = "red", command = all_clear)
button13.place(x = 100, y = 190)

button14 = tk.Button(window, text = "0", fg = "blue", command = lambda : new_entry("0"))
button14.place(x = 150, y = 190)

button15 = tk.Button(window, text = "=", fg = "red", command = ans)
button15.place(x = 200, y = 190)

button16 = tk.Button(window, text = "/", fg = "green", command = lambda : oper("/"))
button16.place(x = 250, y = 190)


window.mainloop()