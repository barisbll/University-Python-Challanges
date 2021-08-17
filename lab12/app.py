import requests, json, sqlite3, os
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk
import PIL.Image


# 4 style the app
# 5 add in menu some style config
# 5.5 add a status line at the bottom of the app
# 6 add comments to your code for readability

def run():
    window_app()


# Call starwars api and turn information to a dictionary
def download_data():

    data = []

    # Go until 10 because of string values in int data
    for e in range(1, 10):
        url = f'https://swapi.dev/api/people/{e}'
        response = requests.request('GET', url)
        res_dict = json.loads(response.text)

        planet_response = requests.request('GET', res_dict['homeworld'])
        planet_response_dict = json.loads(planet_response.text)

        t_dict = {
            'name': res_dict['name'],
            'height': res_dict['height'],
            'mass': res_dict['mass'],
            'planet_name': planet_response_dict['name'],
            'gravity': planet_response_dict['gravity'],
            'population': planet_response_dict['population']
        }

        data.append(t_dict)

    return data


# It saves downloaded data to the db for the first time
def save_sqlite(data):

    # removes file before each save call of db
    remove_file()

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS starwars(
    name TEXT PRIMARY KEY,
    height INT,
    mass INT,
    planet_name TEXT,
    gravity TEXT,
    population INT);
    """)

    for e in data:
        cursor.execute("""
            INSERT INTO starwars(name, height, mass, planet_name, gravity, population) 
            VALUES(?, ?, ?, ?, ?, ?);
            """,
            (e['name'], int(e['height']), int(e['mass']), e['planet_name'], e['gravity'], int(e['population'])))

    conn.commit()


def remove_file():
    if 'test.db' in os.listdir('./'):
        os.remove('test.db')
    else:
        pass


def get_data():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM starwars
    """)

    starwars = cursor.fetchall()
    return  starwars


def draw_plot():
    starwars = get_data()

    height = []
    mass = []

    for e in starwars:
        e = list(e)

        height.append(e[1])
        mass.append(e[2])

    np_height = np.array(height)
    np_mass = np.array(mass)

    fig, axe = plt.subplots()
    axe.plot(np.arange(0, len(np_height)),np_height, label='Height')
    axe.plot(np.arange(0, len(np_mass)), np_mass, label='Mass')

    axe.legend()

    fig.savefig('plot.png')



def window_app():

    # Creating the Window
    window = tk.Tk()
    window.geometry('1000x1000')
    window.title = 'Starwars App'


    # Creating the labels
    display_label = tk.Label(master=window, width=200)
    display_label.pack()

    status_label = tk.Label(master=window, width=200)
    status_label.pack()



    # Download data if it isn't downloaded make operations
    # Draw the plot and saves it
    def show_info():
        status_label['text'] = 'Downloading data from API'

        if 'test.db' not in os.listdir('./'):
            data = download_data()
            save_sqlite(data)
            show_chart_button['state'] = 'normal'

        show_chart_button['state'] = 'normal'

        starwars = get_data()
        str_buffer = ''

        sumOfHeight = 0
        sumOfMass = 0


        for e in starwars:
            e = list(e)
            str_buffer += f"""Name -> {e[0]}, height -> {e[1]} weight -> {e[2]} planet -> {e[3]} \n"""

            sumOfHeight += e[1]
            sumOfMass += e[2]

        display_label['text'] = str_buffer + '\n\n'

        statistics = f'Sum of Height -> {sumOfHeight} \n' \
                     f'Sum of Mass -> {sumOfMass} \n' \
                     f'Average Height -> {round(sumOfHeight/len(starwars), 2)} \n' \
                     f'Average Mass -> {round(sumOfMass / len(starwars), 2)}'

        display_label['text'] += statistics

        draw_plot()



    show_info_button = tk.Button(master=window, text='Show Information', command=show_info)
    show_info_button.pack()



    # Cleaning the text of display layout
    def clear_info():
        status_label['text'] = 'Making Data Unvisible'
        display_label['text'] = ''

    clear_label_button = tk.Button(master=window, text='Clear Info', command=clear_info)
    clear_label_button.pack()



    # Taking plot creating a canvas and showing it with the plot
    tk_img = ImageTk.PhotoImage(PIL.Image.open('plot.png'))
    canvas = tk.Canvas(master=window, width=900, height=900)


    def show_chart():
        status_label['text'] = 'Showing the plot'
        img = canvas.create_image(200, 100, anchor = tk.NW, image=tk_img)
        canvas.pack()

    show_chart_button = tk.Button(master=window, text='Show Chart', command=show_chart)
    show_chart_button.pack()
    show_chart_button['state'] = 'disabled'

    def remove_chart():
        status_label['text'] = 'Making chart unvisible'
        canvas.pack_forget()

    remove_chart_button = tk.Button(master=window, text='Remove Chart', command=remove_chart)
    remove_chart_button.pack()



    # Menu

    menubar = tk.Menu(window)

    def exit_app():
        exit()

    exit_menu = tk.Menu(menubar, tearoff=0)
    exit_menu.add_command(label='Quit', command=exit_app)

    def clean_db():
        status_label['text'] = 'Cleaning The Database'
        remove_file()
        show_chart_button['state'] = 'disabled'

    db_clean_menu = tk.Menu(menubar, tearoff=0)
    db_clean_menu.add_command(label='Clean Database', command=clean_db)

    def blue():
        status_label['text'] = 'Printing to blue'
        window.configure(bg='blue')

    def red():
        status_label['text'] = 'Printing to red'
        window.configure(bg='red')

    def green():
        status_label['text'] = 'Printing to green'
        window.configure(bg='green')

    style_menu = tk.Menu(menubar, tearoff=0)
    style_menu.add_command(label='Blue', command=blue)
    style_menu.add_command(label='Red', command=red)
    style_menu.add_command(label='Green', command=green)

    menubar.add_cascade(label='File', menu=exit_menu)
    menubar.add_cascade(label='Clean', menu=db_clean_menu)
    menubar.add_cascade(label='Style', menu=style_menu)

    window.config(menu=menubar)






    window.mainloop()


run()



