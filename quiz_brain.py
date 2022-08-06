from data import *
import html
import json
import random
import time


FILE_PATH = "./score.json"
NO_QUESTION_RESPOND = "There is no any new question."


class QuizBrain:

    def __init__(self):
        self.user_score = 0
        self.total_score = 0
        self.shown_questions = []

        #Get the highest user score (if the file exists, of course)
        try:
            progress_file = open(FILE_PATH, 'r')
            progress = json.load(progress_file)
            self.highest_score = int(progress["user's score"])
        except FileNotFoundError:
            self.highest_score = 0
        else:
            progress_file.close()
        
        
    def check_answer(self, user_answer):
        self.total_score += 1
        
        if user_answer == self.shown_questions[-1]["correct_answer"]:
            self.user_score += 1
            return True
        else:
            return False
     
     
    #Generates a new question from the existing set of questions
    def get_question(self):
        #Check if some qusetions are not covered yet
        if len(self.shown_questions) < PARAMETERS["amount"]:
            random.seed(time.localtime())
            self.new_question = random.choice(question_data)
            
            while True:
                if self.new_question in self.shown_questions:
                    random.seed(time.localtime())
                    self.new_question = random.choice(question_data)
                else:
                    self.shown_questions.append(self.new_question)
                    break
            
            #Create an html element from a text
            self.question_text = html.unescape(self.new_question["question"])
            self.question_answer = self.new_question["correct_answer"]
        else:
            return NO_QUESTION_RESPOND
        
        return self.question_text


    def reset(self):
        #Make sure we'll not loose any data
        self.save_progress()
        
        if self.user_score > self.highest_score:
            self.highest_score = self.user_score
        
        self.user_score = 0
        self.total_score = 0
        self.shown_questions.clear()
        
        update_data()
        
    
    def save_progress(self):
        #Prepare data before saving
        progress = {
            "user's score": self.user_score,
            "total score": self.total_score,
            }
        
        #Upload updated data into the file
        with open(FILE_PATH, 'w') as progress_file:
            json.dump(progress, progress_file, indent=4)