import customtkinter as ctk

from main_menu.order import order_start
from main_menu.measurement import measurement_start
from main_menu.mix import mix_start
from main_menu.recipe import recipe_manage
from main_menu.ingredient import ingredient_manage
from main_menu.config_menu import config_start
from main_menu.check import check_right

def login():
    username = username_entry.get()
    password = password_entry.get()

    if 1:
        result_label.configure(text="로그인 성공!")
        app.destroy()
        main_menu()
    else:
        result_label.configure(text="로그인 실패!")

def main_menu():
    mainmenu = ctk.CTk()
    mainmenu.geometry("600x500+0+0")
    mainmenu.title("메인 메뉴")
    mainmenu.attributes('-fullscreen', True)

    # 버튼 생성
    order_button = ctk.CTkButton(master=mainmenu, text="작업 지시", command=lambda: order_start() if check_right("order") else no_right("order"), font=("Helvetica", 40, "bold"), width=500, height=100)  # 폰트 크기, width, height 5배 조정
    order_button.pack(pady=20, padx=40)  # pady, padx 2배 조정

    measure_button = ctk.CTkButton(master=mainmenu, text="측량 시작", command=lambda: measurement_start() if check_right("measurement") else no_right("measurement"), font=("Helvetica", 40, "bold"), width=500, height=100)
    measure_button.pack(pady=20, padx=40)

    mix_button = ctk.CTkButton(master=mainmenu, text="배합 시작", command=lambda: mix_start() if check_right("mix") else no_right("mix"), font=("Helvetica", 40, "bold"), width=500, height=100)
    mix_button.pack(pady=20, padx=40)

    recipe_button = ctk.CTkButton(master=mainmenu, text="BOM 관리", command=lambda: recipe_manage() if check_right("recipe") else no_right("recipe"), font=("Helvetica", 40, "bold"), width=500, height=100)
    recipe_button.pack(pady=20, padx=40)

    ingredient_button = ctk.CTkButton(master=mainmenu, text="원료 입고 관리", command=lambda: ingredient_manage() if check_right("ingredient") else no_right("ingredient"), font=("Helvetica", 40, "bold"), width=500, height=100)
    ingredient_button.pack(pady=20, padx=40)

    config_button = ctk.CTkButton(master=mainmenu, text="환경 설정", command=admin_login, font=("Helvetica", 40, "bold"), width=500, height=100)
    config_button.pack(pady=20, padx=40)

    exit_button = ctk.CTkButton(master=mainmenu, text="프로그램 종료", command=mainmenu.destroy, font=("Helvetica", 40, "bold"), width=500, height=100)
    exit_button.pack(pady=20, padx=40)

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

# 앱 생성 및 설정
app = ctk.CTk()
app.geometry("1150x600+0+0")  # 2배 크기로 변경
app.title("로그인")

# 제목 레이블 추가
title_label = ctk.CTkLabel(master=app, text="생산 관리 시스템", font=("Helvetica", 80, "bold"))  # 폰트 크기 2배로 변경
title_label.grid(row=0, column=0, columnspan=2, padx=40, pady=(40, 0))  # padx, pady 2배로 변경

# 레이블 및 입력 필드 배치
username_label = ctk.CTkLabel(master=app, text="아이디:", font=("Helvetica", 40, "bold"))  # 폰트 크기 2배로 변경
username_label.grid(row=1, column=0, padx=40, pady=40, sticky="w")  # padx, pady 2배로 변경
username_entry = ctk.CTkEntry(master=app, placeholder_text="아이디를 입력하세요", width=800, font=("Helvetica", 40, "bold"))  # width 2배로 변경, 폰트 크기 2배로 변경
username_entry.grid(row=1, column=1, padx=40, pady=40, sticky="w")  # padx, pady 2배로 변경

password_label = ctk.CTkLabel(master=app, text="비밀번호:", font=("Helvetica", 40, "bold"))  # 폰트 크기 2배로 변경
password_label.grid(row=2, column=0, padx=40, pady=40, sticky="w")  # padx, pady 2배로 변경
password_entry = ctk.CTkEntry(master=app, placeholder_text="비밀번호를 입력하세요", show="*", width=800, font=("Helvetica", 40, "bold"))  # width 2배로 변경, 폰트 크기 2배로 변경
password_entry.grid(row=2, column=1, padx=40, pady=40, sticky="w")  # padx, pady 2배로 변경

# 프레임 생성
button_frame = ctk.CTkFrame(master=app)
button_frame.grid(row=3, column=0, columnspan=2, padx=40, pady=(40, 80), sticky="ew")  # padx, pady 2배로 변경, pady 하단 여백 추가

# 버튼 배치
login_button = ctk.CTkButton(master=button_frame, text="로그인", command=login, width=500, height = 150, font=("Helvetica", 60, "bold"))  # width 2배로 변경, 폰트 크기 2배로 변경
login_button.pack(side="left", padx=(0, 20))  # padx 2배로 변경
exit_button = ctk.CTkButton(master=button_frame, text="종료", command=app.quit, width=500, height = 150, font=("Helvetica", 60, "bold"))  # width 2배로 변경, 폰트 크기 2배로 변경, 종료 기능 추가
exit_button.pack(side="left", padx=(20, 0))  # padx 2배로 변경

# 결과 레이블
result_label = ctk.CTkLabel(master=app, text="", font=("Helvetica", 40))  # 폰트 크기 2배로 변경
result_label.grid(row=4, column=0, columnspan=2, padx=40, pady=40, sticky="w")  # padx, pady 2배로 변경

app.grid_columnconfigure(0, weight=1)  # 첫 번째 열 (레이블)의 비율 조정
app.grid_columnconfigure(1, weight=1)  # 두 번째 열 (입력 필드)의 비율 조정

app.mainloop()