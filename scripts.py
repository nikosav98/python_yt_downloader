from pytube import YouTube
import PySimpleGUI as sg
import os
import re

def process_request(url, quality):
    video = YouTube(url)
    if video is None: return
    video_streams = video.streams.filter(res=quality,progressive=True)
    
    # Get available video qualities
    available_qualities = [stream.resolution for stream in video_streams]
    print(available_qualities)
    if quality not in available_qualities:
        error_handler(2)
        return
    
    try:
        # Choose the desired video quality
        chosen_stream = video_streams.get_by_resolution(quality)
        file_path = os.path.join(os.path.expanduser("~"), "Downloads", chosen_stream.default_filename)
        # Download the video
        chosen_stream.download(output_path=file_path)
        pop_msg("Video downloaded successfully")

    except Exception as e:
        error_handler(3)
        
def error_handler(errorN):
    '''
    0 : default error
    1 : invalid link
    2 : quality not supported
    3 : failed to download video
    '''
    if errorN == 0:
        pop_msg("Error")
    elif errorN == 1:
        pop_msg("Invalid link (link not found)")
    elif errorN == 2:
        pop_msg("The chosen quality is not supported")
    elif errorN == 3:
        pop_msg("Failed to download video")


def pop_msg(msg):
    try:
        sg.Popup(msg)
    except Exception as e:
        print(f"An error occurred while displaying the popup message: {str(e)}")

def valid_url(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        video_id = match.group(1)
        print(video_id)
        return True
    else:
        return False