import data
import tkinter
from quiz_brain import *


BACKGROUND_COLOR = "#375362"
CANVAS_COLOR = "white"

CONFIRM_IMAGE_PATH = "./images/true.png"
DECLINE_IMAGE_PATH = "./images/false.png"

PROGRAM_NAME = "QuizApp"

REGULAR_FONT = {"name": "Arial", "size": 20, "type": "italic", "color": "black"}
SCORE_FONT = {"name": "Arial", "size": 14, "type": "normal", "color": "white"}

CANVAS_PADDING = 20
BUTTON_PADDING = 20
TEXT_PADDING = 15
WINDOW_PADDING = 20

CANVAS_SIZE = {"width": 300, "height": 250}

NEW_SESSION_MESSAGE = NO_QUESTION_RESPOND + "\nDo You want to launch a new session?"


class QuizInterface:
    
    def __init__(self, quiz_brain: QuizBrain):
        self.brain = quiz_brain
        
        self.window = tkinter.Tk()
        self.window.title(PROGRAM_NAME)
        self.window.config(bg=BACKGROUND_COLOR, padx=WINDOW_PADDING, pady=WINDOW_PADDING)
        
        self.canvas = tkinter.Canvas()
        self.canvas.config(width=CANVAS_SIZE["width"], height=CANVAS_SIZE["height"], bg="white")
        self.question_field = self.canvas.create_text(
            CANVAS_SIZE["width"]/2, 
            CANVAS_SIZE["height"]/2, 
            width=CANVAS_SIZE["width"]-2*WINDOW_PADDING, 
            text=self.brain.get_question(), 
            font=(REGULAR_FONT["name"], REGULAR_FONT["size"], REGULAR_FONT["type"]), 
            fill=REGULAR_FONT["color"]
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=CANVAS_PADDING)
        
        self.confirm_image = tkinter.PhotoImage(file=CONFIRM_IMAGE_PATH)
        self.decline_image = tkinter.PhotoImage(file=DECLINE_IMAGE_PATH)
        
        self.confirm_button = tkinter.Button(
            image=self.confirm_image, 
            highlightthickness=0, 
            borderwidth=0, 
            bg=BACKGROUND_COLOR, 
            command=lambda: self.check_answer("True")
        )
        self.confirm_button.grid(row=2, column=1, padx=BUTTON_PADDING)
        
        self.decline_button = tkinter.Button(
            image=self.decline_image, 
            highlightthickness=0, 
            borderwidth=0, 
            bg=BACKGROUND_COLOR, 
            command=lambda: self.check_answer("False")
        )
        self.decline_button.grid(row=2, column=0, padx=BUTTON_PADDING)
        
        self.score_label = tkinter.Label(
            text=f"Score: {self.brain.user_score}/{self.brain.total_score}", 
            font=(SCORE_FONT["name"], SCORE_FONT["size"], SCORE_FONT["type"]), 
            fg=SCORE_FONT["color"], 
            bg=BACKGROUND_COLOR
        )
        self.score_label.grid(row=0, column=1, sticky=tkinter.E)
        
        self.heighest_score_label = tkinter.Label(
            text=f"Highest score: {self.brain.highest_score}",
            font=(SCORE_FONT["name"], SCORE_FONT["size"], SCORE_FONT["type"]), 
            fg=SCORE_FONT["color"], 
            bg=BACKGROUND_COLOR
        )
        self.heighest_score_label.grid(row=0, column=0, sticky=tkinter.W)
        
        self.window.mainloop()


    def check_answer(self, user_answer):
        self.brain.check_answer(user_answer)
        self.set_question_text()
            

    def set_question_text(self):
        question = self.brain.get_question()
        
        self.update_score()
        
        if question != NO_QUESTION_RESPOND:
            self.canvas.itemconfigure(self.question_field, text=question)
        else:
            respond = tkinter.messagebox.askyesno(title="The Final", message=NEW_SESSION_MESSAGE)
            if respond == True:
                self.brain.reset()
                self.set_question_text()
                self.update_score(is_new_session=True)
            else:
                self.brain.save_progress()
                self.window.destroy()

        
    def update_score(self, is_new_session=False):
        if is_new_session == True:
            self.heighest_score_label.config(text=f"Highest score: {self.brain.highest_score}")
        
        self.score_label.config(text=f"Score: {self.brain.user_score}/{self.brain.total_score}")