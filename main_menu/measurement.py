import customtkinter as ctk
import pickle
import pandas as pd
import os
from datetime import datetime
import tkinter.ttk as ttk
from CTkMessagebox import CTkMessagebox
from main_menu.style import configure_treeview_style
from main_menu.measuring import measuring

with open("config.pickle", "rb") as fr:
    config = pickle.load(fr)

data_path = config["경로"] + "/data"
if not os.path.exists(data_path):
    os.makedirs(data_path)
today = datetime.today().strftime("%Y_%m_%d")
file_name = data_path + "/" + today + "_작업지시.csv"

def measurement_start():
    if os.path.isfile(file_name):
        orders = pd.read_csv(file_name)
        orders_ = orders[orders["현재 단계"] == "0: 작업 전"]
    else:
        data = {
            "작업일": [],
            "지시자": [],
            "지시 시간": [],
            "작업물": [],
            "작업량(kg)": [],
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
        orders_ = orders[orders["현재 단계"] == "0: 작업 전"]
        tree.delete(*tree.get_children())

        for col in orders_.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        orders_sorted = orders_.sort_values(by="현재 단계")
        grouped = orders_sorted.groupby("현재 단계")

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
            CTkMessagebox(title="알림", message="측정할 주문을 선택해주세요.", icon="cancel")
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

    right_frame = ctk.CTkScrollableFrame(master=frame_container)
    right_frame.grid(row=0, column=1, sticky="nsew")

    frame_container.grid_columnconfigure(0, weight=0) 
    frame_container.grid_columnconfigure(1, weight=1)
    frame_container.grid_rowconfigure(0, weight=1)

    def update_time():
        now = datetime.now()
        formatted_time = now.strftime("현재 시각: %Y/%m/%d - %H:%M:%S")
        time_label.configure(text=formatted_time)
        for i in now_labels.keys():
            now_labels[i][0].configure(text =f"현재: {now_labels[i][1]}kg")
        window.after(1000, update_time)

    with open(f"{config["경로"]}/recipe.pickle", "rb") as fr:
        recipe = pickle.load(fr)[data[3]]['배합비']
    whole = 0
    for ingredient in recipe:
        whole += ingredient[1]
    for i in range(len(recipe)):
        recipe[i][1] = recipe[i][1]/whole*data[4]
        recipe[i][1], recipe[i][2] = round(recipe[i][1] - recipe[i][1]*recipe[i][2]/100,3), round(recipe[i][1] + recipe[i][1]*recipe[i][2]/100,3)

    now_labels = {}

    def measurement(data):
        target, min, max = data[0], data[1], data[2]
        measurement_popup = ctk.CTkToplevel(window)
        measurement_popup.geometry("800x500")
        measurement_popup.wm_attributes("-topmost", 1)
        measurement_popup.title(f"{target} 측량 중...")
        measurement_popup.focus_force()
        measurement_popup.lift()

        popup_container_1 = ctk.CTkLabel(master=measurement_popup, height=35, text=f"{target} 측량", font=("Arial", 30, "bold"))
        popup_container_1.grid(row=0,column=0,sticky="new", pady=20)

        popup_container_2 = ctk.CTkFrame(master=measurement_popup)
        popup_container_2.grid(row=1, column=0,sticky="nsew", pady=2, padx=2)

        popup_container_2_highest = ctk.CTkLabel(master=popup_container_2, text = f"하한\n{min}kg", font=("Arial", 30, "bold"), width = 100, height = 100)
        popup_container_2_lowest = ctk.CTkLabel(master=popup_container_2, text = f"상한\n{max}kg", font=("Arial", 30, "bold"), width = 100, height = 100)
        popup_container_2_perfect = ctk.CTkLabel(master=popup_container_2, text = f"적정\n{round((min + max)/2, 3)}kg", font=("Arial", 30, "bold"), width = 100, height = 100)

        popup_container_2_highest.grid(row=0, column=0, sticky="nsew", pady=10, padx =10)
        popup_container_2_lowest.grid(row=0, column=1, sticky="nsew", pady=10, padx =10)
        popup_container_2_perfect.grid(row=0, column=2, sticky="nsew", pady=10, padx =10)

        popup_container_2.columnconfigure(0, weight=1)
        popup_container_2.columnconfigure(1, weight=1)
        popup_container_2.columnconfigure(2, weight=1)

        popup_container_3 = ctk.CTkFrame(master=measurement_popup)
        popup_container_3.grid(row=2, column = 0, sticky="nsew", pady=10, padx =10)
        count = 0
        def update_value():
            nonlocal now_labels, count
            _ = round(measuring(),3)
            if _ != 0 or _ >= 100 or (count >= 3 and _ == 0): 
                now_labels[target][1] = _
                count = 0
            else: count += 1
            if target != 0:
                if now_labels[target][1] < min or now_labels[target][1] > max:
                    popup_container_3_now.configure(fg_color="yellow", text_color="black")
                    now_labels[target][2].configure(fg_color = "lightyellow")
                else:
                    popup_container_3_now.configure(fg_color="green", text_color="black")
                    now_labels[target][2].configure(fg_color = "lightgreen")
            popup_container_3_now.configure(text=f"{round(now_labels[target][1],3)}kg")
            popup_container_3_now.after(500, update_value)

        popup_container_3_now = ctk.CTkLabel(master=popup_container_3, text=f"{round(now_labels[target][1],3)}kg", font=("Arial", 100, "bold"))
        popup_container_3_now.grid(row=0, column = 0, sticky="nsew", pady=10, padx =10)

        def update_value_():
            measurement_popup.destroy()

        popup_container_3_done = ctk.CTkButton(master=popup_container_3, text="측정 종료", font=("Arial", 30, "bold"), command = lambda: update_value_())
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

    for row, ingredient in enumerate(recipe):
        ingredient_name = ingredient[0]  # 재료 이름
        min_value = ingredient[1]  # 최소값
        max_value = ingredient[2]  # 최대값

        # 한 줄당 하나의 Frame 생성
        row_frame = ctk.CTkFrame(right_frame, fg_color="black")  # 검은색 배경으로 경계선 역할
        row_frame.pack(fill="x", padx=5, pady=5)  # 프레임 간 여백 추가

        inner_frame = ctk.CTkFrame(row_frame, fg_color="white")  # 내부 프레임 (실제 라벨 배치)
        inner_frame.pack(fill="both", padx=2, pady=2)  # 테두리를 두껍게 보이게 하기 위한 여백 추가

        ctk.CTkLabel(inner_frame, text=f"재료명: {ingredient_name}", font=("Helvetica", 40, "bold"), width = 500, justify="left", anchor="w").pack(side="left", padx=10, pady=20)
        ctk.CTkLabel(inner_frame, text=f"최소: {min_value}kg", font=("Helvetica", 40, "bold"),text_color = "blue", width = 300, justify="left", anchor="w").pack(side="left", padx=10, pady=20)
        ctk.CTkLabel(inner_frame, text=f"최대: {max_value}kg", font=("Helvetica", 40, "bold"),text_color = "red", width = 300, justify="left", anchor="w").pack(side="left", padx=10, pady=20)
        now_labels[ingredient_name] = [ctk.CTkLabel(inner_frame, text=f"현재: 0kg", font=("Helvetica", 40, "bold"), width = 300, justify="left", anchor="w"), 0, inner_frame]
        now_labels[ingredient_name][0].pack(side="left", padx=10, pady=20)
        ctk.CTkButton(inner_frame, text="측정 시작", font=("Helvetica", 40, "bold"), width = 300,height=90, command = lambda data = [ingredient_name, min_value, max_value]: measurement(data)).pack(side="right", padx=1, pady=1)
    
    def save(data):
        user = user_combo.get()
        save_name = data_path + "/" + today + "_측정완료.csv"
        orders = pd.read_csv(file_name)

        orders.loc[
            (orders["지시자"] == data[1]) & 
            (orders["지시 시간"] == data[2]) & 
            (orders["작업물"] == data[3]) & 
            (orders["작업량(kg)"] == data[4]), 
            "현재 단계"
        ] = f"2: 측량 완료({user})"
        orders.to_csv(file_name, index=False)
        if os.path.isfile(save_name):
            saving = pd.read_csv(save_name)
            data.append(user) #작업자 넣을 곳
            data.append("/".join([f"{x}:{now_labels[x][1]}kg" for x in now_labels.keys()]))
            data.append(sum([now_labels[x][1] for x in now_labels.keys()]))
            print(saving)
            print(data)
            saving.loc[len(saving)] = data
            saving.to_csv(save_name, index = False)

            ingredients = pd.read_csv(config["경로"] + "/ingredients.csv")
            ingredients["유통기한"] = pd.to_datetime(ingredients["유통기한"])
            for x in list(now_labels.keys()):
                if x in list(ingredients["원료명"]):
                    print(x)
                    idx = ingredients.loc[ingredients["원료명"] == x, "유통기한"].idxmin()
                    ingredients.at[idx, "현재량(kg)"] = ingredients.at[idx, "현재량(kg)"] - now_labels[x][1]
                    print(ingredients.at[idx, "현재량(kg)"])
            ingredients.to_csv(config["경로"] + "/ingredients.csv", index=False)

        else:
            saving = pd.DataFrame({
        "작업일": [data[0]],
        "지시자": [data[1]],
        "지시 시간": [data[2]],
        "작업물": [data[3]],
        "작업량(kg)": [data[4]],
        "배합 가마": [data[5]],
        "측량자": [user], # 작업자 넣을 곳
        "측량 결과":["/".join([f"{x}:{now_labels[x][1]}kg" for x in now_labels.keys()])],
        "측량 총량":[sum([now_labels[x][1] for x in now_labels.keys()])]
        })
            saving.to_csv(save_name, index = False)

        window.destroy()

    def cancel():
        orders = pd.read_csv(file_name)
        orders.to_csv(file_name, index=False)

        window.destroy()
    user_combo = ctk.CTkComboBox(left_frame, values=config["작업자"]["측량자"], font=("Helvetica", 20, "bold"), height = 50)
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