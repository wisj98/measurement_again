import pickle
import customtkinter as ctk

with open("config.pickle","rb") as fr:
    config = pickle.load(fr)

def check_right(where):
    if config["권한"][where] == True: return True
    else: return False

def check_mainroot(): 
    return config["결과 저장 경로"]