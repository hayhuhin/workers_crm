import tkinter as tk
from tkinter import ttk
from settings import BG_COLOR,WIDTH,HEIGHT,LAYOUT_COLOR

class frame_displayer_class:
    def __init__(self,window):
        self.window = window 
        self.window.geometry((str(WIDTH)+'x'+str(HEIGHT))) 
        self.window.config(bg=BG_COLOR)


    def left_pane(self):
        pane_frame = ttk.Frame(self.window,width=250,height=1000)

        pane_frame.pack(anchor='w')

        dashboard_button = ttk.Button(master=pane_frame,text='Dashboard')
        dashboard_button.pack(anchor="center",padx=20,pady=20)

        dashboard_button_2 = ttk.Button(master=pane_frame,text='Users')
        dashboard_button_2.pack(padx=20,pady=20)

        dashboard_button_3 = ttk.Button(master=pane_frame,text='Teams')
        dashboard_button_3.pack(padx=20,pady=20)



    def income_window(self):
        frame = tk.Frame(master=self.window,bg='red',width=400,height=400).place(x=300,y=300)


    


    # def displaying_frames(self):

        # self.window.columnconfigure(0, weight=0, minsize=12)
        # self.window.rowconfigure(0, weight=0, minsize=12)

        # frame_1 = tk.Frame(master=self.window,bg='white',width=12,height=12,relief=tk.RAISED,
        #     borderwidth=1,)
        # frame_1.grid(row=0,column=0,padx=1, pady=1)

        # frame_1_1 = tk.Frame(master=self.window,bg='green',width=12,height=20,relief=tk.RAISED,
        #     borderwidth=1,)
        # frame_1_1.place(x=15,y=15)

        # frame_1_3 = tk.Frame(master=self.window,bg='red',width=12,height=12,relief=tk.RAISED,
        #     borderwidth=1,)
        # frame_1_3.grid(row=0,column=0,padx=1, pady=1)



        # frame_2 = tk.Frame(master=self.window,bg='white',width=100,height=100,relief=tk.RAISED,
        #     borderwidth=1)
        # frame_2.grid(row=0,column=1)


    def frame_creator(self,window,width,height,position,bg_color):
        frame = tk.Frame(master=window,width=width,height=height,bg=bg_color)
        frame.place(x=position[0],y=position[1])




    def display(self):
        self.left_pane()
        # self.displaying_frames()
        # self.income_window()
        self.income_window()