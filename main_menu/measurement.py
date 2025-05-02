import customtkinter as ctk
import pickle
import pandas as pd
import os
from datetime import datetime
import tkinter.ttk as ttk
from CTkMessagebox import CTkMessagebox
# from main_menu.style import configure_treeview_style
# from main_menu.measuring import measuring

def measurement_start():
#-------------------------------------------------------------------------
    with open("config.pickle", "rb") as fr:
        config = pickle.load(fr)

    data_path = config["경로"] + "/data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    today = datetime.today().strftime("%Y_%m_%d")
    file_name = data_path + "/" + today + "_작업지시.csv"

    if os.path.isfile(file_name):
        orders = pd.read_csv(file_name)
        orders_ = orders[orders["현재 단계"] == "1:작업 전"]
    else:
        data = {
            "작업일": [],
            "지시자": [],
            "지시 시간": [],
            "제품명": [],
            "작업량(kg)": [],
            "배합 가마": [],
            "현재 단계": []
        }
        orders = pd.DataFrame(data)[["작업일", "지시자", "지시 시간", "제품명", "작업량(kg)", "배합 가마", "현재 단계"]]
        orders.to_csv(file_name, index=False)
#-------------------------------------------------------------------------
    window = ctk.CTk()
    window.title("작업 지시")
    window.attributes('-fullscreen', True)

    up_frame = ctk.CTkFrame(master=window, height=40, fg_color="#333333", corner_radius=0)
    up_frame.pack(side="top", fill="x",pady=[0,5])

    title_label = ctk.CTkLabel(
        window,
        font=("pretendard medium", 14, "bold"),
        text="칭량 작업",
        text_color="#ffffff",       # 흰 글자
        bg_color="#333333"          # 배경 회색
    )
    title_label.place(relx=0.0, x=10, y=10, anchor="nw")

    time_label = ctk.CTkLabel(
        window,
        font=("pretendard medium", 14, "bold"),
        text_color="#ffffff",       # 흰 글자
        bg_color="#333333"          # 배경 회색
    )
    time_label.place(relx=1.0, x=-10, y=10, anchor="ne")

    def update_time():
        now = datetime.now()
        formatted_time = now.strftime("현재 시각: %Y/%m/%d - %H:%M:%S")
        time_label.configure(text=formatted_time)
        window.after(1000, update_time)

    update_time()
#-------------------------------------------------------------------------
    columns_frame = ctk.CTkFrame(master=window, height=40)
    columns_frame.pack(side="top", fill="x")

    column_titles = [
        "작업일", "지시자", "지시 시간", "제품명", "작업량(Kg)",
        "배합가마", "현재단계", "내역", "작업 시작"
    ]

    # column 수에 맞게 weight 지정 (동일한 비율로 배분)
    column_widths = [197, 197, 197, 300, 197, 197, 197, 197, 197]

    for idx, title in enumerate(column_titles):
        label = ctk.CTkLabel(
            master=columns_frame,
            text=title,
            font=("pretendard medium", 14, "bold"),
            width=column_widths[idx],
            height=40,
            anchor="center",  # 가운데 정렬
            fg_color="#52ADD4",  # 이전에 조정한 컬러
            text_color="black"
        )
        if idx == 0: label.grid(row=0, column=idx, sticky="nsew", padx=[7,1])
        else: label.grid(row=0, column=idx, sticky="nsew", padx=1)
#-------------------------------------------------------------------------
    inner_frame = ctk.CTkScrollableFrame(master=window, height=900)
    inner_frame.pack(side="top", fill="x")

    def check(orders, idx):
        print(orders.iloc[idx])

    def refresh_window(orders = False, refresh = False):
        if type(orders) != pd.DataFrame: orders = pd.read_csv(file_name)
        orders = orders.sort_values(by="현재 단계").reset_index(drop=True)
        for widget in inner_frame.winfo_children():
            widget.destroy()
        for i in range(len(orders)):
            order_frame = ctk.CTkFrame(master=inner_frame, height=45)
            order_frame.pack(side="top", fill="x", pady=1)

            for idx, title in enumerate(orders.columns):
                label = ctk.CTkLabel(
                    master=order_frame,
                    text=orders.iloc[i][title],
                    font=("pretendard medium", 12, "bold"),
                    width=column_widths[idx],
                    height=40,
                    anchor="center", 
                    fg_color="#BBBBBB",
                    text_color="black", corner_radius=0
                )
                label.grid(row=0, column=idx, sticky="nsew", padx=1)
            check_button = ctk.CTkButton(master=order_frame,
                    text = "확인",font=("pretendard medium", 12, "bold"),
                    width=column_widths[idx+1],
                    height=40,
                    anchor="center", 
                    fg_color="#BBBBBB",
                    text_color="black",
                    command=lambda i=i, orders=orders: check(orders, i), corner_radius=0
                    )
            check_button.grid(row=0, column=idx+1, sticky="nsew", padx=1)

            save_button = ctk.CTkButton(master=order_frame,
                    text = "작업 시작",font=("pretendard medium", 12, "bold"),
                    width=column_widths[idx+2],
                    height=40,
                    anchor="center", 
                    fg_color="#BBBBBB",
                    text_color="black",
                    command=lambda i=i, orders=orders: work(orders.iloc[i]), corner_radius=0
                    )
            save_button.grid(row=0, column=idx+2, sticky="nsew", padx=1)

        if refresh:
            window.after(30000, lambda refresh=refresh: refresh_window(refresh==True))

    refresh_window(refresh=True)
#------------------------------------------------------------------------------------------------
    def save_data():
        window.destroy()

    # 버튼 프레임 생성
    button_frame = ctk.CTkFrame(window)
    button_frame.pack(pady=10)

    save_button = ctk.CTkButton(button_frame, text="종료하기", font=("pretendard medium", 40, "bold"), command=save_data, height=100, width= 300)
    save_button.pack(side="left", padx=1)

    window.mainloop()
#------------------------------------------------------------------------------------------------
def work(order):
    with open("config.pickle", "rb") as fr:
        config = pickle.load(fr)

    window = ctk.CTk()
    window.title("작업 지시")
    window.attributes('-fullscreen', True)

    up_frame = ctk.CTkFrame(master=window, height=40, fg_color="#333333", corner_radius=0)
    up_frame.pack(side="top", fill="x",pady=[0,5])

    title_label = ctk.CTkLabel(
        window,
        font=("pretendard medium", 14, "bold"),
        text="칭량 작업",
        text_color="#ffffff",       # 흰 글자
        bg_color="#333333"          # 배경 회색
    )
    title_label.place(relx=0.0, x=10, y=10, anchor="nw")

    time_label = ctk.CTkLabel(
        window,
        font=("pretendard medium", 14, "bold"),
        text_color="#ffffff",       # 흰 글자
        bg_color="#333333"          # 배경 회색
    )
    time_label.place(relx=1.0, x=-10, y=10, anchor="ne")

    def update_time():
        now = datetime.now()
        formatted_time = now.strftime("현재 시각: %Y/%m/%d - %H:%M:%S")
        time_label.configure(text=formatted_time)
        window.after(1000, update_time)

    update_time()
#------------------------------------------------------------------------------------------------
    info_frame = ctk.CTkFrame(window, height = 400, fg_color="#BBBBBB", corner_radius=0, width=1500)
    info_frame.pack(side="top",pady=[0,5], fill=None)

    width = [300,300,300,500,300]
    headers = ["작업일", "지시자", "지시 시간", "제품명", "작업량(kg)"]
    for i, text in enumerate(headers):
        label = ctk.CTkLabel(info_frame, text=text, font=("pretendard medium", 20, "bold"), fg_color="#AAAAAA", text_color="black", corner_radius=0, width=width[i], height=75)
        label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

    data = [order["작업일"], order['지시자'], order["지시 시간"], order["제품명"], order["작업량(kg)"]]
    for i, text in enumerate(data):
        label = ctk.CTkLabel(info_frame, text=text, font=("pretendard medium", 18, "bold"), fg_color="#AAAAAA", text_color="black", corner_radius=0, width=width[i], height=75)
        label.grid(row=1, column=i, sticky="nsew", padx=1, pady=1)

    with open(f"{config["경로"]}/recipe.pickle", "rb") as fr:
        recipe = pickle.load(fr)[order["제품명"]]['배합비']

    columns_frame = ctk.CTkFrame(master=window, height=40)
    columns_frame.pack(side="top", fill="x")
    column_titles = [
        "원료명", "기준량(g)", "칭량값(g)", "칭량"
    ]
    column_widths = [900,250,250,500]
    for idx, title in enumerate(column_titles):
        label = ctk.CTkLabel(
            master=columns_frame,
            text=title,
            font=("pretendard medium", 14, "bold"),
            width=column_widths[idx],
            height=80,
            anchor="center",  # 가운데 정렬
            fg_color="#52ADD4",  # 이전에 조정한 컬러
            text_color="black"
        )
        if idx == 0: label.grid(row=0, column=idx, sticky="nsew", padx=[7,1])
        else: label.grid(row=0, column=idx, sticky="nsew", padx=1)
    for ingredient in recipe:
        print(ingredient)
    for i in range(len(recipe)):
        recipe[i][1] = recipe[i][1]/100*order["작업량(kg)"]
        recipe[i][2] = round(recipe[i][1]*recipe[i][2]/100,3)
#------------------------------------------------------------------------------------------------
    now_labels = {}

    def measurement(data):
        target, standard, error = data[0], data[1], data[2]
        popup_window = ctk.CTkToplevel(window)
        popup_window.geometry("800x500")
        popup_window.wm_attributes("-topmost", 1)
        popup_window.title(f"{target} 칭량 중...")
        popup_window.focus_force()
        popup_window.lift()

        top_frame = ctk.CTkLabel(master=popup_window, height=50, text=f"{target} 측량", font=("Arial", 30, "bold"))
        top_frame.grid(row=0,column=0,sticky="new")

        middle_frame = ctk.CTkLabel(master=popup_window,height=50, text=f"기준량: {standard} g", font=("Arial", 30, "bold"))
        middle_frame.grid(row=1,column=0,sticky="new")

        bottom_frame = ctk.CTkFrame(master=popup_window, height=100)
        bottom_frame.grid(row=2, column = 0, sticky="nsew")
        count = 0
        def update_value():
            nonlocal now_labels, count
            _ = round(measuring(),3)
            if _ != 0 or _ >= 100 or (count >= 3 and _ == 0): 
                now_labels[target][1] = _
                count = 0
            else: count += 1
            if target != 0:
                if now_labels[target][1] < standard-error or now_labels[target][1] > standard+error:
                    popup_container_3_now.configure(fg_color="yellow", text_color="black")
                    now_labels[target][2].configure(fg_color = "lightyellow")
                else:
                    popup_container_3_now.configure(fg_color="green", text_color="black")
                    now_labels[target][2].configure(fg_color = "lightgreen")
            popup_container_3_now.configure(text=f"{round(now_labels[target][1],3)}kg")
            popup_container_3_now.after(500, update_value)

        popup_container_3_now = ctk.CTkLabel(master=bottom_frame, text=f"{round(now_labels[target][1],3)}kg", font=("Arial", 50, "bold"))
        popup_container_3_now.grid(row=0, column = 0, sticky="nsew")

        def update_value_():
            popup_window.destroy()

        popup_container_3_done = ctk.CTkButton(master=bottom_frame, text="측정 종료", font=("Arial", 30, "bold"), command = lambda: update_value_())
        popup_container_3_done.grid(row=0, column=1, sticky="nsew", pady=10, padx =10)

        update_value()
        popup_window.mainloop()
#------------------------------------------------------------------------------------------------
    ingredients_frame = ctk.CTkScrollableFrame(master=window, height=650, fg_color="#BBBBBB")
    ingredients_frame.pack(side="top",pady=[0,5], fill="x")
    column_widths = [900,250,250,250,250]
    for row, ingredient in enumerate(recipe):
        ingredient_name = ingredient[0]  # 재료 이름
        standard_value = ingredient[1]
        error_value = ingredient[2]

        ingredient_frame = ctk.CTkFrame(master=ingredients_frame, height=50)
        ingredient_frame.pack(side="top",pady=[0,5], fill="x")

        ctk.CTkLabel(ingredient_frame, text=f"{ingredient_name}", font=("pretendard medium", 12, "bold"), width = 900, height=50, justify="left", anchor="w", fg_color="#AAAAAA",corner_radius=0).pack(side="left", padx=1, pady=[0,1])
        ctk.CTkLabel(ingredient_frame, text=f"{standard_value}", font=("pretendard medium", 12, "bold"), width = 250, height=50, justify="left", fg_color="#AAAAAA",corner_radius=0).pack(side="left", padx=1, pady=[0,1])
        now_labels[ingredient_name] = [ctk.CTkLabel(ingredient_frame, text=f"0", font=("pretendard medium", 12, "bold"), width = 250, height=50, justify="left", fg_color="#AAAAAA",corner_radius=0), 0, ingredient_frame]
        now_labels[ingredient_name][0].pack(side="left", padx=1, pady=[0,1])
        ctk.CTkButton(ingredient_frame, text="칭량 시작", font=("pretendard medium", 12, "bold"), width = 250,height=50, command = lambda data = [ingredient_name, standard_value, error_value]: measurement(data), fg_color="#AAAAAA",corner_radius=0).pack(side="left", padx=1, pady=[0,1])
        if ingredient_name[-1] == "*":
            ctk.CTkButton(ingredient_frame, text="칭량 완료", font=("pretendard medium", 12, "bold"), width = 250,height=50, command = lambda data=ingredient[0]: now_labels[data], fg_color="#AAAAAA",corner_radius=0).pack(side="left", padx=1, pady=[0,1])
        else:
            now_labels.append(ctk.CTkLabel(ingredient_frame, text="칭량 완료", font=("pretendard medium", 12, "bold"), width = 250,height=50, fg_color="#AAAAAA",corner_radius=0))
            now_labels[-1].pack(side="left", padx=1, pady=[0,1])
#------------------------------------------------------------------------------------------------
#save, cancel 함수
#------------------------------------------------------------------------------------------------
    buttons_frame = ctk.CTkFrame(master=window, height=100)
    buttons_frame.pack(side="top",pady=[5,5], fill="x")
    worker = ctk.CTkComboBox(master=buttons_frame, height=100, width=450, font=("pretendard medium", 20, "bold"))
    worker.pack(side="left",padx=15,fill="x")
    save_button = ctk.CTkButton(master=buttons_frame, height=100, width=450, text="전체 칭량 완료", font=("pretendard medium", 20, "bold"), command=lambda :save(order))
    save_button.pack(side="left",padx=15,fill="x")
    cancel_button = ctk.CTkButton(master=buttons_frame, height=100, width=450, text="칭량 취소", font=("pretendard medium", 20, "bold"), command=window.destroy)
    cancel_button.pack(side="left",padx=15,fill="x")
    history_button = ctk.CTkButton(master=buttons_frame, height=100, width=450, text="칭량작업 기록서", font=("pretendard medium", 20, "bold"), command=lambda:history(order, now_labels))
    history_button.pack(side="left",padx=15,fill="x")

    window.mainloop()


if __name__ == "__main__":
    # measurement_window(['2024-01-03', '김철수', '14:00', '마', 10, 'a', '0: 작업 전'])
    measurement_start()