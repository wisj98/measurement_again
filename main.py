import customtkinter as ctk

from main_menu.order import order_start
try: 
    from main_menu.measurement import measurement_start
    check_measure = True
except:
    check_measure = False
from main_menu.mix import mix_start
from main_menu.recipe import recipe_manage
from main_menu.ingredient import ingredient_manage
from main_menu.config_menu import config_start
from main_menu.check import check_right, check_web
import os
import sys
from PIL import Image

BASE_DIR = os.path.dirname(sys.executable)

def login():
    username = username_entry.get()
    password = password_entry.get()
    token = check_web(username, password)
    if token == True:
        result_label.configure(text="로그인 성공!")
        app.destroy()
        main_menu()
    else:
        popup = ctk.CTk()
        popup.title("로그인 실패")
        popup.geometry("600x300")
        
        label = ctk.CTkLabel(popup, text=f"로그인 실패!\n\n\n{token}", font=("Arial", 20, "bold"))
        label.pack(expand=True, padx=20, pady=20)
        
        button = ctk.CTkButton(popup, text="확인", command=popup.destroy)
        button.pack(pady=10)

        popup.mainloop()

def main_menu():
    mainmenu = ctk.CTk()
    mainmenu.title("메인 메뉴")
    mainmenu.attributes('-fullscreen', True)

    bg_image = ctk.CTkImage(dark_image=Image.open("factory.jpg"), size=(mainmenu.winfo_screenwidth(), mainmenu.winfo_screenheight()))

    # 배경 레이블 생성 (이미지를 Label 위에 띄우기)
    bg_label = ctk.CTkLabel(mainmenu, image=bg_image, text="")
    bg_label.place(relwidth=1, relheight=1)

    # 버튼 생성
    order_button = ctk.CTkButton(master=mainmenu, text="작업 지시", command=lambda: order_start() if check_right("order") else no_right("order"), font=("Helvetica", 40, "bold"), width=500, height=100)  # 폰트 크기, width, height 5배 조정
    order_button.pack(pady=(100,10), padx=40)  # pady, padx 2배 조정

    measure_button = ctk.CTkButton(master=mainmenu, text="측량 시작", command=lambda: measurement_start() if check_right("measurement") else no_right("measurement"), font=("Helvetica", 40, "bold"), width=500, height=100)
    measure_button.pack(pady=10, padx=40)

    mix_button = ctk.CTkButton(master=mainmenu, text="배합 시작", command=lambda: mix_start() if check_right("mix") else no_right("mix"), font=("Helvetica", 40, "bold"), width=500, height=100)
    mix_button.pack(pady=10, padx=40)

    recipe_button = ctk.CTkButton(master=mainmenu, text="BOM 관리", command=lambda: recipe_manage() if check_right("recipe") else no_right("recipe"), font=("Helvetica", 40, "bold"), width=500, height=100)
    recipe_button.pack(pady=10, padx=40)

    ingredient_button = ctk.CTkButton(master=mainmenu, text="원료 입고 관리", command=lambda: ingredient_manage() if check_right("ingredient") else no_right("ingredient"), font=("Helvetica", 40, "bold"), width=500, height=100)
    ingredient_button.pack(pady=10, padx=40)

    config_button = ctk.CTkButton(master=mainmenu, text="환경 설정", command=admin_login, font=("Helvetica", 40, "bold"), width=500, height=100)
    config_button.pack(pady=10, padx=40)

    exit_button = ctk.CTkButton(master=mainmenu, text="프로그램 종료", command=mainmenu.destroy, font=("Helvetica", 40, "bold"), width=500, height=100)
    exit_button.pack(pady=10, padx=40)

    mainmenu.mainloop()

def admin_login():
    admin_login_window = ctk.CTk()
    admin_login_window.title("비밀번호 입력")
    admin_login_window.geometry("300x200")
        
    admin_title_label = ctk.CTkLabel(admin_login_window, text="비밀번호 필요", font=("Arial", 16))
    admin_title_label.pack(pady=10)
        
    admin_password_label = ctk.CTkLabel(admin_login_window, text="비밀번호:")
    admin_password_label.pack(pady=5)
    admin_password_entry = ctk.CTkEntry(admin_login_window, show="*")
    admin_password_entry.pack(pady=5)

    def admin_login_action():
        if admin_password_entry.get() == "1": 
            admin_login_window.destroy()
            config_start()
        else: 
            no_right("config")

    admin_login_button = ctk.CTkButton(admin_login_window, text="확인", command=admin_login_action)
    admin_login_button.pack(pady=10)
        
    admin_login_window.mainloop()

def no_right(what):
    root = ctk.CTk()
    root.title("권한 없음")
    root.geometry("300x150")
    
    message = ctk.CTkLabel(root, text=f"{what}에 대한 권한이 없습니다.", font=("Arial", 14))
    message.pack(pady=20)
    
    close_button = ctk.CTkButton(root, text="확인", command=root.destroy)
    close_button.pack(pady=10)
    
    root.mainloop()

# ctk 테마 설정 (옵션)
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")

# 앱 생성
app = ctk.CTk()
app.geometry("1725x900+0+0")  # 창 크기를 1.5배로 변경
app.title("로그인")

# 중앙 정렬을 위한 그리드 설정
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)
app.grid_rowconfigure(4, weight=1)

# 제목 레이블
_ = "생산 관리 시스템"
if check_measure == False:
    _ = "생산 관리 시스템\n(저울이 연결되지 않은 상태입니다.)"
title_label = ctk.CTkLabel(master=app, text=_, font=("Helvetica", 80, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(150, 0), sticky="n")  # 중앙 배치

# 아이디 레이블 및 입력 필드
username_label = ctk.CTkLabel(master=app, text="아이디:", font=("Helvetica", 40, "bold"))
username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")  # 오른쪽 정렬
username_entry = ctk.CTkEntry(master=app, placeholder_text="아이디를 입력하세요", width=800, font=("Helvetica", 40, "bold"))
username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")  # 왼쪽 정렬

# 비밀번호 레이블 및 입력 필드
password_label = ctk.CTkLabel(master=app, text="비밀번호:", font=("Helvetica", 40, "bold"))
password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
password_entry = ctk.CTkEntry(master=app, placeholder_text="비밀번호를 입력하세요", show="*", width=800, font=("Helvetica", 40, "bold"))
password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# 버튼 프레임
button_frame = ctk.CTkFrame(master=app, fg_color="#F0F0F0")
button_frame.grid(row=3, column=0, columnspan=2, pady=60, sticky="n")

# 로그인 및 종료 버튼
login_button = ctk.CTkButton(master=button_frame, text="로그인",command=login ,width=500, height=150, font=("Helvetica", 60, "bold"))
login_button.pack(side="left", padx=40)
exit_button = ctk.CTkButton(master=button_frame, text="종료", command=app.quit, width=500, height=150, font=("Helvetica", 60, "bold"))
exit_button.pack(side="left", padx=40)

# 결과 레이블
result_label = ctk.CTkLabel(master=app, text="", font=("Helvetica", 40))
result_label.grid(row=4, column=0, columnspan=2, pady=40, sticky="n")

# 앱 실행
app.mainloop()
