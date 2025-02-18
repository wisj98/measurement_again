import pickle
import customtkinter as ctk
import pandas as pd
from datetime import datetime

with open("config.pickle","rb") as fr:
    config = pickle.load(fr)

def check_right(where):
    if config["권한"][where] == True: return True
    else: return False

def check_mainroot(): 
    return config["결과 저장 경로"]

def check_web(id, password):
    url = "https://raw.githubusercontent.com/wisj98/measurement_web/main/test.csv"
    df = pd.read_csv(url)
    df = df[(df["ID"] == id) & (df["password"] == password) & (df["program"] == "measurement")]
    if len(df) == 0:
        return "아이디나 비밀번호를 확인해주세요.\n아이디, 비밀번호 찾기 문의는 010-2113-2067로 부탁드립니다."
    if datetime.strptime(df.iloc[0]["until"], "%Y/%m/%d") >= datetime.today():
        return True
    else:
        return f"사용 기한이 {df.iloc[0]["until"]} 부로 만료되었습니다."