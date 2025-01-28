import customtkinter
import pickle
import time
try:
    import measuring
except:
    # 경고 팝업 창 생성
    # warning_popup = customtkinter.CTk()
    # warning_popup.geometry("400x150")
    # warning_popup.title("경고")

    # # 경고 메시지 레이블
    # warning_label = customtkinter.CTkLabel(warning_popup, text="저울에 연결이 되지 않았습니다.\n확인 후 프로그램을 다시 실행해주세요.", font=("Arial", 16))
    # warning_label.pack(pady=20, padx=20)

    # # 확인 버튼
    # def close_popup():
    #     warning_popup.destroy()
    #     exit()

    # confirm_button = customtkinter.CTkButton(warning_popup, text="확인", command=close_popup)
    # confirm_button.pack(pady=10)

    # warning_popup.mainloop()
    pass

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "test" and password == "1234":
        result_label.configure(text="로그인 성공!")
        app.destroy()
        open_new_window()
    else:
        result_label.configure(text="로그인 실패!")

def open_new_window():
    new_window = customtkinter.CTk()
    new_window.geometry("600x400")
    new_window.title("메인 메뉴")

    # 버튼 생성
    start_button = customtkinter.CTkButton(master=new_window, text="측정 시작", command=start_measurement)
    start_button.pack(pady=20, padx=20)

    recipe_button = customtkinter.CTkButton(master=new_window, text="레시피 관리", command=manage_recipe)
    recipe_button.pack(pady=20, padx=20)

    config_button = customtkinter.CTkButton(master=new_window, text="환경 설정", command=manage_config)
    config_button.pack(pady=20, padx=20)

    exit_button = customtkinter.CTkButton(master=new_window, text="프로그램 종료", command=new_window.destroy)
    exit_button.pack(pady=20, padx=20)

    new_window.mainloop()

def manage_config():
    _login_window = customtkinter.CTk()
    _login_window.title("관리자 로그인")
    _login_window.geometry("300x200")

    _username_label = customtkinter.CTkLabel(master=_login_window, text="사용자 이름:")
    _username_label.pack(pady=10, padx=10)
    _username_entry = customtkinter.CTkEntry(master=_login_window, placeholder_text="사용자 이름을 입력하세요")
    _username_entry.pack(pady=10, padx=10)

    _password_label = customtkinter.CTkLabel(master=_login_window, text="비밀번호:")
    _password_label.pack(pady=10, padx=10)
    _password_entry = customtkinter.CTkEntry(master=_login_window, placeholder_text="비밀번호를 입력하세요", show="*")
    _password_entry.pack(pady=10, padx=10)

    def _login():
        _username = username_entry.get()
        _password = password_entry.get()

        if _username == "test" and _password == "1234":
            _login_window.destroy()

            config_window = customtkinter.CTkToplevel()
            config_window.geometry("600x400")
            config_window.title("환경설정")
            config_window.focus_force()
            config_window.grab_set()

            change_root = customtkinter.CTkButton(master = config_window, text="결과 저장 경로 변경")
            change_root.pack(padx = 20, pady = 20)

            worker_list = customtkinter.CTkButton(master = config_window, text="작업자 설정")
            worker_list.pack(padx = 20, pady = 20)

            right_config = customtkinter.CTkButton(master = config_window, text="권한 설정")
            right_config.pack(padx = 20, pady = 20)
        else:
            _result_label.configure(text="로그인 실패")

    _login_button = customtkinter.CTkButton(master=_login_window, text="로그인", command=_login)
    _login_button.pack(pady=10, padx=10)

    _result_label = customtkinter.CTkLabel(master=_login_window, text="")
    _result_label.pack(pady=10, padx=10)


def start_measurement():
    measurement_window = customtkinter.CTkToplevel()
    measurement_window.after(0, lambda: measurement_window.state('zoomed'))
    measurement_window.title("측정")
    measurement_window.focus_force()
    measurement_window.grab_set()

    # 컨테이너 프레임 생성
    container_first = customtkinter.CTkFrame(measurement_window, height=80)
    container_first.pack(pady=10, padx=20, fill="x")  # 가로로 꽉 채우기

    # 사용업체명 레이블
    company_label = customtkinter.CTkLabel(container_first, text="사용업체명: ABC 회사", font=("Arial", 24))
    company_label.pack(side="left", padx=10)  # 왼쪽 정렬

    # 시간 표시 레이블
    time_label = customtkinter.CTkLabel(container_first, text="", font=("Arial", 24), fg_color="black")
    time_label.pack(side="right", padx=10)

    container = customtkinter.CTkFrame(measurement_window, height=500)
    container.pack(pady=10, padx=20, fill="x")

    # 2:3 비율로 나눌 컨테이너 생성
    left_container = customtkinter.CTkFrame(container, height=500)
    right_container = customtkinter.CTkScrollableFrame(container, height=500)

    # grid 레이아웃으로 배치 (가중치 2:3)
    left_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    right_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    container.grid_columnconfigure(0, weight=1)  # 왼쪽 컨테이너 가중치 2
    container.grid_columnconfigure(1, weight=4)  # 오른쪽 컨테이너 가중치 3
    right_container.grid_columnconfigure(0, weight=1)

    # 왼쪽

    left_1_container = customtkinter.CTkFrame(left_container, height = 100)
    left_2_container = customtkinter.CTkFrame(left_container, height = 80)
    left_3_container = customtkinter.CTkFrame(left_container, height = 80)
    left_4_container = customtkinter.CTkFrame(left_container, height = 80)
    left_5_container = customtkinter.CTkFrame(left_container, height = 80)
    left_6_container = customtkinter.CTkFrame(left_container, height = 80)

    left_1_container.grid(row = 0, column = 0, sticky = "nsew", padx=10, pady=10)
    left_2_container.grid(row = 1, column = 0, sticky = "nsew", padx=10, pady=10)
    left_3_container.grid(row = 2, column = 0, sticky = "nsew", padx=10, pady=10)
    left_4_container.grid(row = 3, column = 0, sticky = "nsew", padx=10, pady=10)
    left_5_container.grid(row = 4, column = 0, sticky = "nsew", padx=10, pady=10)
    left_6_container.grid(row = 5, column = 0, sticky = "nsew", padx=10, pady=10)

    left_container.grid_columnconfigure(0, weight=1)

    left_1_left_container = customtkinter.CTkFrame(left_1_container, height = 80)
    left_1_left_container.grid(row = 0, column = 0, sticky = "nsew", padx=2, pady=2)
    left_2_left_container = customtkinter.CTkFrame(left_2_container, height = 60).grid(row = 0, column = 0, sticky = "nsew", padx=2, pady=2)
    left_3_left_container = customtkinter.CTkFrame(left_3_container, height = 60).grid(row = 0, column = 0, sticky = "nsew", padx=2, pady=2)
    left_4_left_container = customtkinter.CTkFrame(left_4_container, height = 60).grid(row = 0, column = 0, sticky = "nsew", padx=2, pady=2)
    left_5_left_container = customtkinter.CTkFrame(left_5_container, height = 60).grid(row = 0, column = 0, sticky = "nsew", padx=2, pady=2)

    left_1_right_container = customtkinter.CTkFrame(left_1_container, height = 80)
    left_1_right_container.grid(row = 0, column = 1, sticky = "nse", padx=2, pady=2)
    left_2_right_container = customtkinter.CTkFrame(left_2_container, height = 60).grid(row = 0, column = 1, sticky = "nsew", padx=2, pady=2)
    left_3_right_container = customtkinter.CTkFrame(left_3_container, height = 60).grid(row = 0, column = 1, sticky = "nsew", padx=2, pady=2)
    left_4_right_container = customtkinter.CTkFrame(left_4_container, height = 60).grid(row = 0, column = 1, sticky = "nsew", padx=2, pady=2)
    left_5_right_container = customtkinter.CTkFrame(left_5_container, height = 60).grid(row = 0, column = 1, sticky = "nsew", padx=2, pady=2)

    left_1_container.grid_columnconfigure(0, weight = 1)
    left_1_container.grid_columnconfigure(1, weight = 3)
    left_2_container.grid_columnconfigure(0, weight = 1)
    left_2_container.grid_columnconfigure(1, weight = 1)
    left_3_container.grid_columnconfigure(0, weight = 1)
    left_3_container.grid_columnconfigure(1, weight = 1)
    left_4_container.grid_columnconfigure(0, weight = 1)
    left_4_container.grid_columnconfigure(1, weight = 1)
    left_5_container.grid_columnconfigure(0, weight = 1)
    left_5_container.grid_columnconfigure(1, weight = 1)

    #레시피 불러오기
    with open("recipe.pickle","rb") as fr:
        recipes = pickle.load(fr)
    recipe_keys = sorted(recipes.keys())
    chosen = recipe_keys[0]

    #초기화 버튼
    def reset():
        measurement_window.destroy()
        start_measurement()

    reset_button = customtkinter.CTkButton(master=left_1_left_container, text="초기화", font=("Arial", 30, "bold"), fg_color="white", text_color="black", command=reset)
    left_1_left_container.grid_rowconfigure(0, weight=1)  # 행 가중치 설정
    left_1_left_container.grid_columnconfigure(0, weight=1)  # 열 가중치 설정
    reset_button.grid(row=0, column=0, sticky = "nsew")

    #레시피 선택
    def new_recipe(choice):
        # right_container 내부의 모든 위젯 삭제
        for widget in right_container.winfo_children():
            widget.destroy()

        values = []
        labels = []

        def update_labels(labels, values):
            standard = sorted(values, key = lambda x: len(x))[-1][0] / sorted(values, key = lambda x: len(x))[-1][1]
            for i in range(len(values)):
                target = standard * values[i][1]
                labels[i][0].configure(text=f"목표\n {round(target - (target * values[i][2] / 100), 3)}kg ~ {round(target + (target * values[i][2] / 100), 3)}kg")
                labels[i][1].configure(text=f"현재\n {round(values[i][0],3)}kg")
                if abs(values[i][0] - target) > (target * values[i][1] / 100) and values[i][0] != 0:
                    labels[i][2].configure(fg_color = "red")
                else:
                    if values[i][0] != 0:
                        labels[i][2].configure(fg_color = "green")
                if len(values[i]) == 5:
                    labels[i][2].configure(text = f"(기준)\n{recipes[choice][i][0]}")
                else:
                    labels[i][2].configure(text = f"{recipes[choice][i][0]}")
<<<<<<< HEAD
            right_container.after(1000, update_labels, labels, values)
        right_container.after(1000, update_labels, labels, values)
=======
            time.sleep(0.5)
            right_container.after(250, update_labels, labels, values)
        right_container.after(500, update_labels, labels, values)
>>>>>>> 4fec827373332eecc9d5528b548fa977c0b8a316
        def measurement(num):
            measurement_popup = customtkinter.CTkToplevel(measurement_window)
            measurement_popup.geometry("800x500")
            measurement_popup.wm_attributes("-topmost", 1)
            measurement_popup.title(f"{values[num][3]} 측량 중...")
            measurement_popup.focus_force()
            measurement_popup.lift()

            popup_container_1 = customtkinter.CTkLabel(master=measurement_popup, height=35, text=f"{values[num][3]} 측량", font=("Arial", 30, "bold"))
            popup_container_1.grid(row=0,column=0,sticky="new", pady=20)

            popup_container_2 = customtkinter.CTkFrame(master=measurement_popup)
            popup_container_2.grid(row=1, column=0,sticky="nsew", pady=2, padx=2)
            
            standard = sorted(values, key = lambda x: len(x))[-1][0] / sorted(values, key = lambda x: len(x))[-1][1]
            target = standard * values[num][1]
<<<<<<< HEAD
            popup_container_2_highest = customtkinter.CTkLabel(master=popup_container_2, text = f"하한\n{round(target - target * values[num][2] / 100,3)}kg", font=("Arial", 30, "bold"), width = 100, height = 100)
            popup_container_2_lowest = customtkinter.CTkLabel(master=popup_container_2, text = f"상한\n{round(target + target * values[num][2] / 100,3)}kg", font=("Arial", 30, "bold"), width = 100, height = 100)
            popup_container_2_perfect = customtkinter.CTkLabel(master=popup_container_2, text = f"적정\n{round(target,3)}kg", font=("Arial", 30, "bold"), width = 100, height = 100)
=======
            popup_container_2_highest = customtkinter.CTkLabel(master=popup_container_2, text = f"하한\n{round(target - target * values[num][2] / 100,2)}g", font=("Arial", 30, "bold"), width = 100, height = 100)
            popup_container_2_lowest = customtkinter.CTkLabel(master=popup_container_2, text = f"상한\n{round(target + target * values[num][2] / 100,2)}g", font=("Arial", 30, "bold"), width = 100, height = 100)
            popup_container_2_perfect = customtkinter.CTkLabel(master=popup_container_2, text = f"적정\n{round(target, 2)}g", font=("Arial", 30, "bold"), width = 100, height = 100)
>>>>>>> 4fec827373332eecc9d5528b548fa977c0b8a316

            popup_container_2_highest.grid(row=0, column=0, sticky="nsew", pady=10, padx =10)
            popup_container_2_lowest.grid(row=0, column=1, sticky="nsew", pady=10, padx =10)
            popup_container_2_perfect.grid(row=0, column=2, sticky="nsew", pady=10, padx =10)

            popup_container_2.columnconfigure(0, weight=1)
            popup_container_2.columnconfigure(1, weight=1)
            popup_container_2.columnconfigure(2, weight=1)

            popup_container_3 = customtkinter.CTkFrame(master=measurement_popup)
            popup_container_3.grid(row=2, column = 0, sticky="nsew", pady=10, padx =10)
<<<<<<< HEAD
            now, count = 0, 0
            # start = values[num][0]
            # others = sum([x[0] for x in values]) - start
            def update_value():
                nonlocal now, count
                _ = measuring.measuring()
                if _ != 0 or _ >= 100 or (count >= 3 and _ == 0): 
                    now = _
                    count = 0
                else: count += 1
                if target != 0:
                    if abs(now - target) > (target * values[num][2] / 100):
                        popup_container_3_now.configure(fg_color="yellow", text_color="black")
                    else:
                        diff = abs(now - target)  # target과의 차이 계산
                        g = int(255 - diff / target * 255)  # target에서 멀수록 g 값 감소
                        g = max(0, min(255, g))  # g 값을 0 ~ 255 사이로 제한
                        color = "#%02x%02x%02x" % (0, g, 0)  # RGB 색상 코드 생성
                        popup_container_3_now.configure(fg_color=color, text_color="black")
                popup_container_3_now.configure(text=f"{round(now,3)}kg")
=======
            now = 0
            start = values[num][0]
            others = sum([x[0] for x in values]) - start
            def update_value():
                def hsv_to_rgb(h, s, v):
                    return colorsys.hsv_to_rgb(h / 360, s, v)
                nonlocal start, now, others
                now = start + 1 #설정 필요
                # if target != 0:
                #     if abs(now - target) > (target * values[num][1] / 100):
                #         diff = abs(now - target * values[num][1] / 100)
                #         h = 60  # 노란색의 H 값 (HSV 색상 모델)
                #         s = 1.0  # 채도 최대
                #         v = 1 - (diff / (target * values[num][1] / 100))  # 명도 조절 (0 ~ 1)
                #         r, g, b = hsv_to_rgb(h, s, v)  # HSV를 RGB로 변환
                #         color = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
                #         popup_container_3_now.configure(fg_color=color)
                #     else:
                #         diff = abs(now - target * values[num][1] / 100)
                #         h = 120  # 초록색의 H 값 (HSV 색상 모델)
                #         s = 1.0  # 채도 최대
                #         v = 1 - (diff / (target * values[num][1] ))  # 명도 조절 (0 ~ 1)
                #         r, g, b = hsv_to_rgb(h, s, v)  # HSV를 RGB로 변환
                #         color = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
                #         popup_container_3_now.configure(fg_color=color)
                popup_container_3_now.configure(text=f"{now}g")
>>>>>>> 4fec827373332eecc9d5528b548fa977c0b8a316
                popup_container_3_now.after(500, update_value)

            popup_container_3_now = customtkinter.CTkLabel(master=popup_container_3, text=f"{round(now,3)}kg", font=("Arial", 100, "bold"))
            popup_container_3_now.grid(row=0, column = 0, sticky="nsew", pady=10, padx =10)

            def update_value_(num):
                if sum([x[0] for x in values]) == 0: values[num].append("기준!")
                values[num][0] = now
                measurement_popup.destroy()
                
            popup_container_3_done = customtkinter.CTkButton(master=popup_container_3, text="측정 종료", font=("Arial", 30, "bold"), command = lambda: update_value_(num))
            popup_container_3_done.grid(row=0, column=1, sticky="nsew", pady=10, padx =10)

            popup_container_3.columnconfigure(0,weight=10)
            popup_container_3.columnconfigure(1,weight=1)
            popup_container_3.rowconfigure(0,weight=1)

            measurement_popup.columnconfigure(0, weight = 1)
            measurement_popup.rowconfigure(0, weight = 1)
            measurement_popup.rowconfigure(1, weight = 1)
            measurement_popup.rowconfigure(2, weight = 5)
            update_value()
            measurement_popup.mainloop()

        for i in range(len(recipes[choice])):
            values.append([0, recipes[choice][i][1], recipes[choice][i][2], recipes[choice][i][0]])
            container_ = customtkinter.CTkFrame(master=right_container, height=75)
            container_.grid(row=i,column=0, sticky = "nsew", padx=3,pady=2)

            name = customtkinter.CTkLabel(master=container_,height=75,width=150, text=recipes[choice][i][0], font=("Arial", 20, "bold"))
            name.grid(row=0,column=0,sticky="nsew",padx=10)
            percentage_1 = customtkinter.CTkLabel(master=container_, height=75, width=100, text=f"/ 주재료비 {recipes[choice][i][1]} ", font=("Arial", 20, "bold"),anchor="e")
            percentage_2 = customtkinter.CTkLabel(master=container_, height=75, width=50, text=f"± {recipes[choice][i][2]}%", font=("Arial", 15),anchor="w")
            percentage_1.grid(row=0,column=1,sticky="nse",padx=0)
            percentage_2.grid(row=0,column=2,sticky="nse",padx=0)

            target = customtkinter.CTkLabel(master=container_,height=75, width=175, text=f"0kg", font=("Arial", 20, "bold"))
            now = customtkinter.CTkLabel(master=container_,height=75, width=50, text=f"0kg", font=("Arial", 15, "bold"))
            target.grid(row=0,column=3,sticky="nsw",padx=20)
            now.grid(row=0,column=4,sticky="nsw",padx=0)
            labels.append([target, now, name])

            measure = customtkinter.CTkButton(master=container_,height=50,width=50, text="측정 시작", font=("Arial", 30, "bold"), command=lambda num=i: measurement(num))
            measure.grid(row=0, column=5, sticky="e", padx=5, pady=5)
            container_.columnconfigure(0, weight=2)
            container_.columnconfigure(1, weight=2)
            container_.columnconfigure(2, weight=2)
            container_.columnconfigure(3, weight=2)
            container_.columnconfigure(4, weight=1)
            container_.columnconfigure(5, weight=2)


    choose_recipe = customtkinter.CTkComboBox(master=left_1_right_container,values=recipe_keys, command=new_recipe)
    choose_recipe_label = customtkinter.CTkLabel(master=left_1_right_container, text="레시피 선택", font=("Arial", 20, "bold"))
    # left_1_right_container.grid_rowconfigure(0, weight=1)  # 행 가중치 설정
    left_1_right_container.grid_columnconfigure(0, weight=1)
    left_1_right_container.grid_columnconfigure(1, weight=5)  # 열 가중치 설정
    choose_recipe.grid(row=0, column=1, sticky = "nsew", pady = 10, padx = 20)
    choose_recipe_label.grid(row=0, column=0, sticky = "nsew")
    
    # 실시간
    def update_live():
        # 시간
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        time_label.configure(text=current_time)

        measurement_window.after(1000, update_live)

    update_live()

    measurement_window.mainloop()

def manage_recipe():

    recipe_window = customtkinter.CTk()
    recipe_window.geometry("300x450")
    recipe_window.title("레시피 관리")

    with open("recipe.pickle","rb") as fr:
        recipes = pickle.load(fr)
    
    recipe_list = sorted(recipes.keys())

    selected_now = None

    label = customtkinter.CTkLabel(master=recipe_window, text="레시피 목록")
    label.pack(pady=10, padx=20)

    text_box = customtkinter.CTkTextbox(master=recipe_window, wrap="word")
    text_box.pack(pady=20, padx=20, fill="both", expand=True)

    def on_text_box_click(event):
        nonlocal selected_now
        text_box.tag_add("sel", "current linestart", "current lineend")
        text_box.tag_add("selected", "current linestart", "current lineend")  # 선택된 행에 "selected" 태그 추가

        # 선택된 부분 출력
        selected_text = text_box.get("sel.first", "sel.last")
        label_now.configure(text=f"선택된 레시피: {selected_text}")
        selected_now = selected_text

    text_box.bind("<Button-1>", on_text_box_click)
    text_box.bind("<Double-Button-1>", on_text_box_click)

    # recipe_list의 요소들을 텍스트 박스에 추가
    for recipe in recipe_list:
        text_box.insert("end", recipe + "\n")
    def fixing_recipe():
        fix_recipe_window = customtkinter.CTk()
        fix_recipe_window.geometry("600x150")
        fix_recipe_window.title("레시피 수정")
        fixing_recipe = recipes[selected_now]
        def fix_recipe():
            try:
                new = entry.get().split("=")
                recipes[new[0]] = [[x.split("/")[0],float(x.split("/")[1]),float(x.split("/")[2])] for x in new[1].split("+")]
                with open("recipe.pickle", "wb") as fw: 
                        pickle.dump(recipes, fw)
                text_box.delete("1.0", "end")
                recipe_list = sorted(recipes.keys())
                for recipe in recipe_list:
                    text_box.insert("end", recipe + "\n")
                fix_recipe_window.destroy()
            except:
                warning_window = customtkinter.CTk()
                warning_window.geometry("300x100")
                warning_window.title("경고")

                # "레시피 양식에 맞춰서 작성해 주세요." 레이블 생성
                warning_label = customtkinter.CTkLabel(master=warning_window, text="레시피 양식에 맞춰서 작성해 주세요.")
                warning_label.pack(pady=10, padx=20)

                # "닫기" 버튼 생성 및 command 설정
                def close_warning_window():
                    warning_window.destroy()

                close_button = customtkinter.CTkButton(master=warning_window, text="닫기", command=close_warning_window)
                close_button.pack(pady=10, padx=20)

                warning_window.mainloop()
        # "example" 레이블 생성
        label = customtkinter.CTkLabel(master=fix_recipe_window, text="""레시피를 입력해주세요. \n예시)용액_1=우유/10/1+식초/5/1+간장/3/1""")
        label.pack(pady=10, padx=20)

        # 글자를 입력할 수 있는 박스 생성
        entry = customtkinter.CTkEntry(master=fix_recipe_window)
        entry.pack(pady=10, padx=20, fill="x", expand=True)
        entry.insert(0,f"{selected_now}={"+".join([f"{x[0]}/{x[1]}/{x[2]}" for x in fixing_recipe])}")
        # "추가" 버튼 생성
        add_button = customtkinter.CTkButton(master=fix_recipe_window, text="수정", command = fix_recipe)
        add_button.pack(pady=10, padx=20)

        fix_recipe_window.mainloop()
        
    def add_recipe():
        new_recipe_window = customtkinter.CTk()
        new_recipe_window.geometry("600x150")
        new_recipe_window.title("레시피 추가")

        def new_recipe():
            try:
                new = entry.get().split("=")
                recipes[new[0]] = [[x.split("/")[0],float(x.split("/")[1]),float(x.split("/")[2])] for x in new[1].split("+")]
                with open("recipe.pickle", "wb") as fw: 
                        pickle.dump(recipes, fw)
                text_box.delete("1.0", "end")
                recipe_list = sorted(recipes.keys())
                for recipe in recipe_list:
                    text_box.insert("end", recipe + "\n")
                new_recipe_window.destroy()
            except:
                warning_window = customtkinter.CTk()
                warning_window.geometry("300x100")
                warning_window.title("경고")

                # "레시피 양식에 맞춰서 작성해 주세요." 레이블 생성
                warning_label = customtkinter.CTkLabel(master=warning_window, text="레시피 양식에 맞춰서 작성해 주세요.")
                warning_label.pack(pady=10, padx=20)

                # "닫기" 버튼 생성 및 command 설정
                def close_warning_window():
                    warning_window.destroy()

                close_button = customtkinter.CTkButton(master=warning_window, text="닫기", command=close_warning_window)
                close_button.pack(pady=10, padx=20)

                warning_window.mainloop()
        # "example" 레이블 생성
        label = customtkinter.CTkLabel(master=new_recipe_window, text="""레시피를 입력해주세요. \n예시)용액_1=우유/10/1+식초/5/1+간장/3/1""")
        label.pack(pady=10, padx=20)

        # 글자를 입력할 수 있는 박스 생성
        entry = customtkinter.CTkEntry(master=new_recipe_window)
        entry.pack(pady=10, padx=20, fill="x", expand=True)

        # "추가" 버튼 생성
        add_button = customtkinter.CTkButton(master=new_recipe_window, text="추가", command = new_recipe)
        add_button.pack(pady=10, padx=20)

        new_recipe_window.mainloop()

    def delete_recipe():
        try:
            selected_recipe = selected_now # 선택된 레시피 이름 가져오기
            if selected_recipe in recipes.keys():
                del recipes[selected_recipe]  # 딕셔너리에서 레시피 삭제
                with open("recipe.pickle", "wb") as fw:  # 딕셔너리를 pickle 파일로 저장
                    pickle.dump(recipes, fw)
                text_box.delete("1.0", "end")  # 텍스트 박스 내용 지우기
                recipe_list = sorted(recipes.keys())  # 레시피 목록 업데이트
                for recipe in recipe_list:
                    text_box.insert("end", recipe + "\n")  # 업데이트된 목록 표시
            else:
                print("삭제할 레시피를 선택하세요.")
        except KeyError:
            print("선택한 레시피가 존재하지 않습니다.")

    # 현재 라벨
    label_now = customtkinter.CTkLabel(master = recipe_window, text="선택된 레시피:")
    label_now.pack(pady=5, padx=20)

    # 버튼 생성
    modify_button = customtkinter.CTkButton(master=recipe_window, text="레시피 수정", command = fixing_recipe)
    modify_button.pack(pady=5, padx=20)

    add_button = customtkinter.CTkButton(master=recipe_window, text="레시피 추가", command = add_recipe)
    add_button.pack(pady=5, padx=20)

    delete_button = customtkinter.CTkButton(master=recipe_window, text="레시피 삭제", command=delete_recipe)
    delete_button.pack(pady=5, padx=20)

    recipe_window.mainloop()

# customtkinter 테마 설정 (옵션)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# 앱 생성 및 설정
app = customtkinter.CTk()
app.geometry("600x400")
app.title("로그인")

# 사용자 이름 레이블 및 입력 필드
username_label = customtkinter.CTkLabel(master=app, text="사용자 이름:")
username_label.pack(pady=10, padx=10)
username_entry = customtkinter.CTkEntry(master=app, placeholder_text="사용자 이름을 입력하세요")
username_entry.pack(pady=10, padx=10)

# 비밀번호 레이블 및 입력 필드
password_label = customtkinter.CTkLabel(master=app, text="비밀번호:")
password_label.pack(pady=10, padx=10)
password_entry = customtkinter.CTkEntry(master=app, placeholder_text="비밀번호를 입력하세요", show="*")
password_entry.pack(pady=10, padx=10)

# 로그인 버튼
login_button = customtkinter.CTkButton(master=app, text="로그인", command=login)
login_button.pack(pady=10, padx=10)

# 결과 레이블
result_label = customtkinter.CTkLabel(master=app, text="")
result_label.pack(pady=10, padx=10)

app.mainloop()