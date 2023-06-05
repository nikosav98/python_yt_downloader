import time
import PySimpleGUI as sg
import scripts as scripts
import threading

quality_options = ['360p', '720p', '1080p', '4k']
selected_quality = quality_options[0]

def download_thread(url, quality):
    scripts.process_request(url, quality)
    
sg.theme('DarkBlack')
layout = [
    [sg.Text('Enter YouTube URL: '), sg.InputText(key='-URL-'), sg.Button('+')],
    [sg.Text('Choose video quality: '), sg.Combo(quality_options, default_value=quality_options[0], key='dropdown',enable_events=True)],
    [sg.Push(), sg.Button('Start'), sg.Button('Cancel'), sg.Push()],
    [sg.Push(), sg.Text('', key='progress'), sg.Push()],
]

window = sg.Window('YT Video Downloader', layout)

while True:
    event, values = window.read()

    # If the window is closed or Cancel button is clicked, break the loop
    if event == sg.WINDOW_CLOSED:
        break

    if event == 'dropdown':
        selected_quality = values['dropdown']

    if event == 'Start':
        print(selected_quality)
        if scripts.valid_url(values['-URL-']):
            window['progress'].update('Downloading...')
            window.read(timeout=500)
            threading.Thread(target=download_thread, args=(values['-URL-'], selected_quality)).start()
        else:
            scripts.error_handler(1)

        window['-URL-'].update('')
        window['progress'].update('')
        if event == 'Cancel':
            break


window.close()