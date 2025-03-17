# Dear user, before we begin, you may need to install the following libraries:
# 1. tkinter
# 2. pygame
# 3. PIL
# Moreover, you may need to install the font file "PressStart2P.ttf", which can be found in the same directory as this file. You need to open the file, press install on the screen, and restart your computer for the font to be installed.
# Lastly, we hope you enjoy our leaderboard implementation as much as we enjoyed making (and crying over) it. Thank you for your time.

import tkinter as tk
import pygame
from tkinter.font import Font
from PIL import Image, ImageTk
from SkipList import createNode, createSkipList, insert, delete, search, display, maxLevel

pygame.init()
music = pygame.mixer.Sound("scoreping.mp3") 

maxLevel = 5
current_page = 0
players_count = 0


# Functions for buttons

# This function is used to add a player to the leaderboard. It first retrieves the name and score from the respective entry fields.
# Then it inserts the player into the skip list (which is used to maintain the leaderboard) with the score as the key and the name as
# the value. The players_count is incremented by 1. The leaderboard is then updated and all windows are hidden. Finally, the entry
# fields for name and score are cleared.    
def add_player():
    global players_count
    name = name_entry.get()
    score = int(score_entry.get())
    insert(skipList, (int(score), name))
    players_count += 1
    update_leaderboard()
    hide_all_windows()
    name_entry.delete(0, tk.END)
    score_entry.delete(0, tk.END)

# This function is used to delete a player from the leaderboard. It first retrieves the name from the delete_entry field. Then it
# deletes the player from the skip list. The players_count is decremented by 1. The leaderboard is then updated and all windows are 
# hidden. Finally, the entry field for name is cleared.
def delete_player():
    global players_count
    name = delete_entry.get()
    delete(skipList, name)
    players_count -= 1
    update_leaderboard()
    hide_all_windows()
    delete_entry.delete(0, tk.END)

# This function is used to search for a player in the leaderboard. It first retrieves the name from the search_entry field. Then it 
# searches for the player in the skip list. If the player is found, it displays a message with the player's rank, name, and score. If 
# the player is not found, it displays a message indicating that the player was not found. All windows are then hidden, and the
# search_entry field is cleared.
def search_player():
    name = search_entry.get()
    found, player = search(skipList, name)
    if found:
        show_search_True_screen(player)
    else:
        show_search_False_screen()


# Functions for traversing leaderboard

# This function is used to move to the previous page of the leaderboard. It decrements the current_page by 1 and updates the
# leaderboard display.
def go_left():
    global current_page
    if current_page > 0:
        current_page -=1
        update_leaderboard()

# This function is used to move to the next page of the leaderboard. It increments the current_page by 1 and updates the leaderboard 
# display.
def go_right():
    global current_page, players_count
    if (current_page + 1) * 8 < players_count:
        current_page += 1
        update_leaderboard()


#Showing/hiding screen functions

# This function is used to show the add player screen. It hides all windows and shows the add player screen. It lifts the window to the 
# top and deiconifies it. The add player screen is then packed. This works similarly for the delete, search, and search result screens.
def show_add_player_screen():
    hide_all_windows()
    new_window_add.lift()
    new_window_add.deiconify()
    add_player_screen.pack()

def close_add_player_screen():
    new_window_add.withdraw()

def show_delete_player_screen():
    hide_all_windows()
    new_window_delete.lift()
    new_window_delete.deiconify()
    delete_player_screen.pack()

def close_delete_player_screen():
    new_window_delete.withdraw()

def show_search_player_screen():
    hide_all_windows()
    new_window_search.lift()
    new_window_search.deiconify()
    hide_all_search_screens()
    search_player_screen.pack()

def close_search_player_screen():
    new_window_search.withdraw()

# the search result = True screen works a bit differently. It first hides all search screens, then displays the search result screen 
# with the player's rank, name, and score. The search entry field is then cleared. It displays members from the search value (their 
# name) and returns their rank and score.
def show_search_True_screen(player):
    global current_page
    music.play()
    hide_all_search_screens()
    players = display(skipList, 0).split("\n")
    rank = "Not found"
    for p in players:
        if str(player[0]) in p:
            rank = p.split(",")[0].split(":")[1].strip()
            break
    search_result_text1.config(text=f"Player {player[1]} found! Rank: {rank}, Score: {player[0]}")
    search_result_True.pack()
    search_entry.delete(0, tk.END)


def show_search_False_screen():
    music.play()
    hide_all_search_screens()
    search_result_False.pack()
    search_entry.delete(0, tk.END)

def hide_all_search_screens():
    search_player_screen.pack_forget()
    search_result_True.pack_forget()
    search_result_False.pack_forget()

# This function is used to hide all windows. It hides the add, delete, and search windows.
def hide_all_windows():
    music.play()
    new_window_add.withdraw()
    new_window_delete.withdraw()
    new_window_search.withdraw()


# This function is used to generate the leaderboard text for a specific page or for all players. It first retrieves all players from 
# the skip list and sorts them by score in descending order. If the page is -1, it generates the leaderboard text for all players. 
# Otherwise, it generates the leaderboard text for the players on the specified page. The leaderboard text includes the rank, name, and 
# score of each player. The function returns the leaderboard text.
def display(skipList, page):
    current = skipList[1][2][0]  # Start from the first node
    players = []
    while current:
        players.append((current[0][1], current[0][0]))
        current = current[2][0]  # Move to the next node
    
    players = sorted(players, key=lambda player: player[1], reverse=True)  # Sort the players by score in descending order

    leaderboard_text = ""
    if page == -1:  # Special value to return all players
        for count, player in enumerate(players, start=1):    # Display the players in the leaderboard
            leaderboard_text += f"Rank: {count}, Player: {player[0]}, Score: {player[1]}\n\n"
    else:
        for count, player in enumerate(players[page*8:(page+1)*8], start=page*8+1):    # Display the players in the leaderboard
            leaderboard_text += f"Rank: {count}, Player: {player[0]}, Score: {player[1]}\n\n"

    return leaderboard_text

# This function is used to update the leaderboard display. It retrieves the leaderboard text for the current page and updates the 
# leaderboard display with the text using the custom font.
def update_leaderboard():
    leaderboard_display.config(text=display(skipList, current_page), font= custom_font)

# creating/initialising the skip list
skipList = createSkipList()

# Create main window
root = tk.Tk()
root.title("Leaderboard")

root.geometry("1000x650")
root.resizable(False, False)

# Load images
background_img = ImageTk.PhotoImage(Image.open("background.jpg"))
add_button_img = ImageTk.PhotoImage(Image.open("ADD.png").resize((150, 52)))
delete_button_img = ImageTk.PhotoImage(Image.open("DELETE.png").resize((150, 52)))
search_button_img = ImageTk.PhotoImage(Image.open("SEARCH.png").resize((150, 52)))
arrow_left_img = ImageTk.PhotoImage(Image.open("left shift.png"))
arrow_right_img = ImageTk.PhotoImage(Image.open("right shift.png"))
# menu_screen_img = ImageTk.PhotoImage(Image.open("menu screen.jpeg"))

# Load the font file
font_path = "PressStart2P.ttf"  
custom_font = Font(family="Press Start 2P", size=12)


# Create canvas for background
canvas = tk.Canvas(root, width=1000, height=650)
canvas.pack()
canvas.create_image(500, 325, image=background_img)  # Center the background image


# Create leaderboard display
leaderboard_display = tk.Label(root, bg='#FEA348')
leaderboard_display.place(x=500, y=325, anchor='center')


#Creating seperate screens for add, search, delete

new_window_add = tk.Toplevel(root)
new_window_add.title("Add Player")
new_window_add.protocol("WM_DELETE_WINDOW", close_add_player_screen)
add_player_screen = tk.Frame(new_window_add, bg = "#6B88FE")

new_window_delete = tk.Toplevel(root)
new_window_delete.title("Delete Player")
new_window_delete.protocol("WM_DELETE_WINDOW", close_delete_player_screen)
delete_player_screen = tk.Frame(new_window_delete, bg = "#6B88FE")

new_window_search = tk.Toplevel(root)
new_window_search.title("Search Player")
new_window_search.protocol("WM_DELETE_WINDOW", close_search_player_screen)
search_player_screen = tk.Frame(new_window_search, bg = "#6B88FE")
search_result_True = tk.Frame(new_window_search, bg = '#6B88FE')
search_result_False = tk.Frame(new_window_search, bg = "#6B88FE")

# Create buttons
add_button = tk.Button(root, image=add_button_img, font=custom_font, bg = '#6B88FE', command=show_add_player_screen)
add_button.place(x=250, y=550, anchor='center')

delete_button = tk.Button(root, image=delete_button_img, font=custom_font, bg = '#6B88FE', command=show_delete_player_screen)
delete_button.place(x=500, y=550, anchor='center')

search_button = tk.Button(root, image=search_button_img, font=custom_font, bg = '#6B88FE', command=show_search_player_screen)
search_button.place(x=750, y=550, anchor='center')

#Create screens:
#Add player screen
add_player_frame = tk.Frame(add_player_screen, bg= "#6B88FE")
add_player_frame.pack(fill= 'both', padx= 10, pady = 15)

add_player_name = tk.Label(add_player_frame, text='Name:', font=custom_font, bg = '#6B88FE')
add_player_name.pack(side='left', padx=10, pady=5)

name_entry = tk.Entry(add_player_frame) #enter players name to add
name_entry.pack(side='left', padx=10, pady=5)

add_player_score = tk.Label(add_player_frame, text='Score:',font=custom_font, bg = '#6B88FE')
add_player_score.pack(side='left', padx=10, pady=5)

score_entry = tk.Entry(add_player_frame) #enter players score to add
score_entry.pack(side='left', padx=10, pady=5)

final_add_button = tk.Button(add_player_screen, text='Add Player', font=custom_font, bg = '#6B88FE', command=add_player)
final_add_button.pack(padx=5 , pady=5)

#Delete player screen
delete_player_frame = tk.Frame(delete_player_screen, bg= "#6B88FE")
delete_player_frame.pack(fill='both', padx=10, pady=5)

delete_player_name = tk.Label(delete_player_frame, text='Name:', font=custom_font, bg = '#6B88FE')
delete_player_name.pack(side='left', padx=10, pady=5)

delete_entry = tk.Entry(delete_player_frame) #enter players name to delete 
delete_entry.pack(side='left', padx=10, pady=5)

final_delete_button = tk.Button(delete_player_screen, text='Delete Player', font=custom_font, bg = '#6B88FE', command=delete_player)
final_delete_button.pack( padx=5 , pady=5)

#Search player screen
search_player_frame = tk.Frame(search_player_screen, bg= "#6B88FE")
search_player_frame.pack(fill='both', padx=10, pady=5)

search_player_name = tk.Label(search_player_frame, text='Name:', font=custom_font, bg = '#6B88FE')
search_player_name.pack(side='left', padx=10, pady=5)

search_entry = tk.Entry(search_player_frame) #enter players name to search
search_entry.pack(side='left', padx=10, pady=5)

final_search_button = tk.Button(search_player_screen, text='Search Player', font=custom_font, bg = '#6B88FE', command=search_player)
final_search_button.pack( padx=5 , pady=5)


#Search result screen - True (found)
search_result_True1 = tk.Frame(search_result_True, bg = "#6B88FE")
search_result_True1.pack(fill='both', padx=10, pady=5)


search_result_text1 = tk.Label(search_result_True1, text='Player found.', font=custom_font, bg = '#6B88FE')
search_result_text1.pack(padx=10 , pady=5)

search_result_button = tk.Button(search_result_True1, text='OK', font=custom_font, bg = '#6B88FE', command=close_search_player_screen)
search_result_button.pack(side='left', padx=5 , pady=5)


#Search result screen - False (not found)
search_result_False1 = tk.Frame(search_result_False, bg = "#6B88FE")
search_result_False1.pack(fill='both', padx=10, pady=5)

search_result_text2 = tk.Label(search_result_False1, text='Player not found.', font=custom_font, bg = '#6B88FE')
search_result_text2.pack(padx=10 , pady=5)

search_result_button = tk.Button(search_result_False1, text='OK', font=custom_font, bg = '#6B88FE', command=close_search_player_screen)
search_result_button.pack(side='left', padx=5 , pady=5)


# Create arrow buttons
left_button = tk.Button(root, image=arrow_left_img, command=go_left, bg = '#6B88FE')
left_button.place(x=100, y=325, anchor='center')

right_button = tk.Button(root, image=arrow_right_img, command=go_right, bg = '#6B88FE')
right_button.place(x=900, y=325, anchor='center')


update_leaderboard()
new_window_add.withdraw()
new_window_delete.withdraw()
new_window_search.withdraw()
root.mainloop()


