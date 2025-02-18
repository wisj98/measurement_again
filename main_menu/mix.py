import customtkinter as ctk
import pickle
import pandas as pd
import os
from datetime import datetime
import tkinter.ttk as ttk
from CTkMessagebox import CTkMessagebox
from main_menu.style import configure_treeview_style

with open("config.pickle", "rb") as fr:
    config = pickle.load(fr)

data_path = config["경로"] + "/data"
if not os.path.exists(data_path):
    os.makedirs(data_path)
today = datetime.today().strftime("%Y_%m_%d")
file_name = data_path + "/" + today + "_작업지시.csv"

def mix_start():
    if os.path.isfile(file_name):
        orders = pd.read_csv(file_name)
        orders_ = orders[orders["현재 단계"].str.startswith("2")]
    else:
        data = {
            "작업일": [],
            "지시자": [],
            "지시 시간": [],
            "작업물": [],
            "작업량": [],
            "배합 가마": [],
            "현재 단계": []
        }
        orders = pd.DataFrame(data)
        orders.to_csv(data_path + "/" + today + "_작업지시.csv", index=False)

    window = ctk.CTk()
    window.title("작업 지시")
    window.attributes('-fullscreen', True)

    up_frame = ctk.CTkFrame(master=window, height=40)
    up_frame.pack(side="top", fill="x")

    time_label = ctk.CTkLabel(window, font=("Arial", 30, "bold"))
    time_label.place(relx=1.0, x=-10, y=10, anchor="ne")

    def refresh_tree():
        if os.path.isfile(file_name):
            orders = pd.read_csv(file_name)
        orders_ = orders[orders["현재 단계"].str.startswith("2")]
        tree.delete(*tree.get_children())

        for col in orders_.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        orders_sorted = orders_.sort_values(by="현재 단계")
        
        # "현재 단계"의 첫 글자로 그룹화
        grouped = orders_sorted.groupby(orders_sorted["현재 단계"].str[0])

        for stage, group in grouped:
            for _, row in group.iterrows():
                tree.insert("", "end", values=list(row))
            tree.insert("", "end", values=["" for _ in range(len(orders_sorted.columns))])

        tree.pack(fill="both", expand=True, padx=10, pady=10)
        window.after(20000, refresh_tree)

    def update_time():
        now = datetime.now()
        formatted_time = now.strftime("현재 시각: %Y/%m/%d - %H:%M:%S")
        time_label.configure(text=formatted_time)
        window.after(1000, update_time)

    update_time()
    configure_treeview_style(window)
    tree = ttk.Treeview(window, columns=list(orders_.columns), show="headings")

    refresh_tree()

    def select():
        global orders_

        selected_items = tree.selection()
        if not selected_items:
            CTkMessagebox(title="알림", message="배합할 주문을 선택해주세요.", icon="cancel")
            return

        if CTkMessagebox(title="시작 확인", message="선택한 주문을 작업하시겠습니까?", icon="question").get():
            selected_rows = [] 

            for item in selected_items:
                item_values = tree.item(item, 'values')
                for _, row in orders.iterrows():
                    row_values = list(row)
                    if len(item_values) == len(row_values):
                        match = all(str(item_values[i]) == str(row_values[i]) for i in range(len(item_values)))  
                        if match:
                            selected_rows.append(row_values) 
                            break
            update = orders[orders.apply(lambda row: list(row) in selected_rows, axis=1)].index

            orders.to_csv(data_path + "/" + today + "_작업지시.csv", index=False)
            print(selected_rows)
            measurement_window(selected_rows[0])

    def save_data():
        window.destroy()

    # 버튼 프레임 생성
    button_frame = ctk.CTkFrame(window)
    button_frame.pack(pady=10)

    select_button = ctk.CTkButton(button_frame, text="작업 시작", font=("Helvetica", 40, "bold"), command=select, height=100, width= 300)
    select_button.pack(side="left", padx=10)

    save_button = ctk.CTkButton(button_frame, text="종료하기", font=("Helvetica", 40, "bold"), command=save_data, height=100, width= 300)
    save_button.pack(side="left", padx=10)

    window.mainloop()

def measurement_window(data):
    data = data[:-1]
    window = ctk.CTk()
    window.title("측량")
    window.attributes('-fullscreen', True)

    up_frame = ctk.CTkFrame(master=window, height=40)
    up_frame.pack(side="top", fill="x")

    time_label = ctk.CTkLabel(window, font=("Arial", 30, "bold"))
    time_label.place(relx=1.0, x=-10, y=10, anchor="ne")

    info_label = ctk.CTkLabel(window, font=("Arial", 30, "bold"), text=f"지시자: {data[1]} | 지시 시간: {data[2]} | 제품 명: {data[3]} | 제조량: {data[4]}kg")
    info_label.place(relx=0.0, x=10, y=10, anchor="nw")

    frame_container = ctk.CTkFrame(master=window)
    frame_container.pack(side="top", fill="both", expand=True)

    left_frame = ctk.CTkFrame(master=frame_container, width=100)
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_container = ctk.CTkFrame(master=frame_container)
    right_container.grid(row=0, column=1, sticky="nsew")

    frame_container.grid_columnconfigure(0, weight=0) 
    frame_container.grid_columnconfigure(1, weight=1)
    frame_container.grid_rowconfigure(0, weight=1)

    def update_time():
        now = datetime.now()
        formatted_time = now.strftime("현재 시각: %Y/%m/%d - %H:%M:%S")
        time_label.configure(text=formatted_time)
        window.after(1000, update_time)

    with open(f"{config["경로"]}/recipe.pickle", "rb") as fr:
        recipe = pickle.load(fr)[data[3]]['배합법']
    
    recipe = [[x,False] for x in recipe]
    
    def next(n):
        def counter(now, order, t=None):
            if t is None:  # 첫 실행 시
                minutes, seconds = map(int, order[1:-1].split(":"))
                t = minutes * 60 + seconds  # 초 단위로 변환
            
            if t > 0:
                now.configure(text=f"{n+1} 단계\n\n{t//60}:{t%60} 대기", command=None)
                window.after(1000, lambda: counter(now, order, t - 1))  # 1초 감소 후 재실행
            else:
                next(n)  # 시간이 0이 되면 다음 단계 실행

        recipes_dict[n][0].configure(fg_color="green")
        recipes_dict[n][1].configure(fg_color="green")
        n += 1
        
        if n < len(recipe):
            order = recipe[n][0]
            if order.startswith("(") and order.endswith(")"):  # 타이머 조건 확인
                counter(now, order)
            else:
                now.configure(text=f"{n+1} 단계\n\n{order}", command=lambda: next(n))
        else:
            now.configure(text="배합이 완료되었습니다.\n좌측의 배합 완료 버튼을 눌러주세요.")

    now = ctk.CTkButton(master=right_container, text=f"1 단계\n\n{recipe[0][0]}", font=("Helvetica", 100, "bold"), height = 1000, width = 1300, command=lambda: next(0))
    now.grid(row=0,column=0, padx=50, pady=20)

    recipes = ctk.CTkScrollableFrame(master=right_container, height =1000, width=350)
    recipes.grid(row=0,column=1)

    recipes_dict = {}
    for row, i in enumerate(recipe):
        # 한 줄당 하나의 Frame 생성
        row_frame = ctk.CTkFrame(recipes, fg_color="black")  # 검은색 배경으로 경계선 역할
        row_frame.pack(fill="x", padx=5, pady=5)  # 프레임 간 여백 추가

        inner_frame = ctk.CTkFrame(row_frame, fg_color="white")  # 내부 프레임 (실제 라벨 배치)
        inner_frame.pack(fill="both", padx=2, pady=2)  # 테두리를 두껍게 보이게 하기 위한 여백 추가

        recipes_dict[row] = [ctk.CTkLabel(inner_frame, text=f"{row+1} 단계\n{i[0] if i[0][0] != "(" else i[0][1:-1] + "대기"}", font=("Helvetica", 40, "bold"), width = 300, justify="left", anchor="w"), inner_frame]
        recipes_dict[row][0].pack(padx=10, pady=20)

    
    def save(data):
        orders = pd.read_csv(file_name)
        user = user_combo.get()
        orders.loc[
            (orders["지시자"] == data[1]) & 
            (orders["지시 시간"] == data[2]) & 
            (orders["작업물"] == data[3]) & 
            (orders["작업량(kg)"] == data[4]), 
            "현재 단계"
        ] = f"4: 배합 완료({user})"
        print(orders)
        orders.to_csv(file_name, index=False)

        window.destroy()

    def cancel(data):
        orders = pd.read_csv(file_name)

        orders.to_csv(file_name, index=False)

        window.destroy()

    user_combo = ctk.CTkComboBox(left_frame, values=config["작업자"]["배합자"], font=("Helvetica", 20, "bold"), height = 50)
    user_combo.grid(row=1, column=0, sticky="s", pady=10, padx = 10)

    done_button = ctk.CTkButton(left_frame, text="측정\n완료", font=("Helvetica", 40, "bold"), command=lambda: save(data), height = 450)
    done_button.grid(row=2, column=0, sticky="s", pady=10, padx = 10)

    cancel_button = ctk.CTkButton(left_frame, text="측정\n취소", font=("Helvetica", 40, "bold"), command=lambda: cancel(data), height = 450)
    cancel_button.grid(row=3, column=0, sticky="s", pady=10, padx = 10)
    update_time()
    window.mainloop()

if __name__ == "__main__":
    measurement_window(['2024-01-03', '김철수', '14:00', '마', 10, 'a', '0: 작업 전'])
    # measurement_start()