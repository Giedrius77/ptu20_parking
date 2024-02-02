import PySimpleGUI as sg
import sqlite3

connection = sqlite3.connect('fridge.db')
cursor = connection.cursor()

def add(product, quantity):
    with connection:
        try:
            cursor.execute(('INSERT INTO Fridge(Product, Quantity)'
            'VALUES (?,?);'),(product, quantity))
        except Exception:
            cursor.execute(('UPDATE Fridge SET Quantity = Quantity + ? WHERE Product = ?'),(quantity, product))
def content():
    with connection:
        cursor.execute('DELETE FROM Fridge Where Quantity = 0;')
        cursor.execute('SELECT Product, Quantity FROM Fridge')
        fridge = cursor.fetchall()
        return fridge
    
def remove(quantity, product):
    with connection:
        cursor.execute(('UPDATE Fridge SET Quantity = Quantity - ? WHERE Product = ?;'),
        (quantity, product))
main_layout = [ 
[sg.Button('Add product', key = '-ADD-', font = 'Arial 23'), 
sg.Button('Eat product', key = '-REMOVE-', font = 'Arial 23')],
[sg.Table(values = content(), headings= ('Product', 'Quantity'), key= '-table-', 
expand_x=True, expand_y=True, font = 'Arial 23', justification='left')],
[sg.Text('Enter Product: '), sg.Input('', key = '-Product-')],
[sg.Text('Enter Quantity: '), sg.Input('', key = '-Quantity-')] 
]

window = sg.Window('Fridge', main_layout, size = (370,700),element_padding=12, text_justification='center',element_justification='center', font = 'Arial 23')
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    if event == '-ADD-':
        add(values['-Product-'], values['-Quantity-'])
        window['-table-'].update(values=content())
    elif event == '-REMOVE-':
        remove(values['-Quantity-'],values['-Product-'])
        window['-table-'].update(values=content())
    

# reikia susikurti lentele!!!!

#     CREATE TABLE Fridge(
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# Product TEXT UNIQUE,
# Quantity INTEGER);
# DROP TABLE Fridge