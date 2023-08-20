import tkinter as tk
from frontend import frame_displayer_class



class main_tkinter_app:
    def __init__(self,front_end_frames_class):
        self.window = tk.Tk()
        self.frame_class= front_end_frames_class(self.window)
        



    def run(self):

        self.frame_class.display()
        
        self.window.mainloop()


if __name__ == "__main__":
    # main_run = main_tkinter_app(frame_displayer_class)
    # main_run.run()
    pass
 
