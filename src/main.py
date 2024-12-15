from nicegui import app, ui
from nicegui.events import KeyEventArguments
from model import get_recommendations, get_results_info
import numpy as np
# this file needs pywebview to work (add as dependency in documentation)

movieTitle, filterType, filterValue = '', '', ''

result = list()

def handle_key(e: KeyEventArguments):
    if e.key == 'Enter' and not e.action.repeat:
        if e.action.keydown:
            buttonEvent(movieTitle,filterType,filterValue)
keyboard = ui.keyboard(on_key=handle_key, ignore=['select','button','textarea'])

def buttonEvent(mT,fT,fV):
    try:
        if len(mT.value) == 0:
            ui.notify("Error - Please Enter a Movie Title", position="top", color="red", timeout=3000, progress=True)
            return
    except:
        ui.notify("Error - Please Enter a Movie Title", position="top", color="red", timeout=3000, progress=True)
        return

    if fT.value != "None":
        try:
            if len(fV.value) == 0:
                ui.notify("Error - Please Enter a Filter Value", position="top", color="red", timeout=3000, progress=True)
                return
        except:
            ui.notify("Error - Please Enter a Filter Value", position="top", color="red", timeout=3000, progress=True)
            return

    try: len(fV.value)
    except:
        fV.value = ""

    result = get_recommendations(mT.value, fT.value, fV.value)
    if type(result) == np.ndarray:
        ui.notify(result[1], position="top", color="red", timeout=5000, progress=True)
        return
    result = get_results_info(result)
    for movie in result:
        print(movie)
    make_grid.refresh(result)
    ui.notify("Selected " + str(len(result)) + " Recommendations", position='top')    


app.native.window_args['title'] = "AI Movie Recommender"
app.native.window_args['min_size'] = (1280, 720)

ui.add_head_html('<style>body {background-color: #F7F2EA; }</style>')
ui.colors(primary='#6571F3')

with ui.column().classes('w-full items-center'):
    with ui.row().classes('justify-center gap-y-1 font-bold'):
        ui.label('Welcome, please enter a Movie Title followed by an optional Filter to further refine your search!')
        ui.label('Known GUI Bug: If search produces no results, DO NOT spam the button but continue to attempt searching and it will eventually appear.')



with ui.column().classes('w-full items-center bg-[#E6D4B4] py-5'):
    with ui.row().classes():
        movieTitle = (ui.input('Movie Title')
                      .classes('w-96 bg-[#F7F2EA] self-center text-lg')
                      .props('clearable outlined square stack-label=true clear-icon="close"'))
        filterType = (ui.select(["None", "Director", "Actor", "Genre", "Year"], value="None")
                      .classes('bg-[#F7F2EA] self-center w-32 text-lg')
                      .props('outlined square label=Filter stack-label=true'))
        filterValue = (ui.input('Filter Value')
                       .classes('w-80 bg-[#F7F2EA] self-center text-lg ')
                       .props('clearable outlined square stack-label=true clear-icon="close"'))
        (ui.button('Generate', on_click=lambda: buttonEvent(movieTitle,filterType,filterValue))
            .classes('text-[21px] rounded-none self-center w-40 h-14 tracking-wide'))


def make_card(movie):
    with ui.card().classes('w-96 bg-[#E6D4B4] justify-center mx-2 my-2').props('square'):
        ui.image(movie['poster_link'])
        with ui.card_section().classes('w-full mt-0 bg-[#F7F2EA]').props('rounded'):
            ui.label(movie['title']).classes('font-bold text-lg')
            with ui.row().classes('px-0 mx-0 gap-x-2'):
                ui.icon('star', color='gold').classes('w-1 self-center space-x-0')
                ui.label(movie['imdb_rating']).classes('self-center space-x-0')
                ui.label(movie['year']).classes('italic self-center space-x-0')
            ui.label(movie['genre'].replace(","," |"))


@ui.refreshable
def make_grid(result):
    grid = ui.grid(columns='auto auto auto').classes('w-full justify-center py-8')
    with grid:
            for movie in result:
                make_card(movie)

make_grid(result)


ui.run(native=True, window_size=(1280, 1000), fullscreen=False)