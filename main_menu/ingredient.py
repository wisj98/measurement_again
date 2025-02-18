import customtkinter as ctk
import pickle
import pandas as pd
import os
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from tkinter import ttk
import numpy as np
from main_menu.style import configure_treeview_style

with open("config.pickle", "rb") as fr:
    config = pickle.load(fr)

data_path = config["경로"]

if not os.path.exists(data_path):
    os.makedirs(data_path)

file_name = data_path + "/ingredients.csv"

if os.path.isfile(file_name):
    ingredients = pd.read_csv(file_name)
else:
    data = {
        "원료 코드": [],
        "원료명": [],
        "Lot no.": [],
        "거래처명": [],
        "유통기한": [],
        "입고량(kg)": [],
        "현재량(kg)": [],
    }
    ingredients = pd.DataFrame(data)

    # ingredients = pd.DataFrame({
    #     "원료 코드":[],
    #     "원료명":[] ,
    #     "Lot no.":[] ,
    #     "거래처명":[] ,
    #     "유통기한":[] ,
    #     "입고량(L)":[] ,
    #     "현재량(L)":[] ,
    # })
    ingredients.to_csv(file_name, index=False)

def ingredient_manage():
    ingredients = pd.read_csv(file_name)
    invalid_rows = ingredients[ingredients["현재량(kg)"] <= 0]

    for index, row in invalid_rows.iterrows():
        ingredient_name = row["원료명"]
        amount = row["현재량(kg)"]

        target_row = ingredients[(ingredients["원료명"] == ingredient_name) & (ingredients["현재량(kg)"] > 0)].sort_values("유통기한").head(1)

        if not target_row.empty:
            target_index = target_row.index[0]
            ingredients.at[target_index, "현재량(kg)"] += amount

        ingredients.drop(index, inplace=True)

    window = ctk.CTk()
    window.title("재고 관리")
    window.attributes('-fullscreen', True)

    # 시간 표시 레이블 생성
    up_frame = ctk.CTkFrame(master=window, height=40)
    up_frame.pack(side="top", fill="x")

    time_label = ctk.CTkLabel(window, font=("Arial", 25))
    time_label.place(relx=1.0, x=-10, y=10, anchor="ne")

    def update_time():
        now = datetime.now()
        formatted_time = now.strftime("현재 시각: %Y/%m/%d - %H:%M:%S")
        time_label.configure(text=formatted_time)
        window.after(1000, update_time)  # 1초마다 업데이트

    configure_treeview_style(window)
    update_time()

    # Treeview 위젯 생성
    tree = ttk.Treeview(window, columns=list(ingredients.columns), show="headings")

    def refresh_tree():
        ingredients = pd.read_csv(file_name)
        tree.delete(*tree.get_children())

        for col in ingredients.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        ingredients_sorted = ingredients.sort_values(by="원료명")

        grouped = ingredients_sorted.groupby("원료명")

        for stage, group in grouped:
            for _, row in group.iterrows():
                tree.insert("", "end", values=list(row))
            tree.insert("", "end", values=["" for _ in range(len(ingredients.columns))])

        tree.pack(fill="both", expand=True, padx=10, pady=10)

    refresh_tree()

    def add_order():
        add_window = ctk.CTk()
        add_window.title("입고")
        add_window.geometry("850x650+0+0")  # 창 크기 조정 (add_order()와 동일)

        # 레이블 및 입력 필드 폰트, 크기 조정
        ctk.CTkLabel(add_window, text="원료 코드:", font=("Helvetica", 40, "bold")).grid(row=0, column=0, padx=30, pady=(100,10), sticky="e")
        code_entry = ctk.CTkEntry(add_window, font=("Helvetica", 40, "bold"), width=500)
        code_entry.grid(row=0, column=1, padx=30, pady=(100,10))

        ctk.CTkLabel(add_window, text="원료명:", font=("Helvetica", 40, "bold")).grid(row=1, column=0, padx=30, pady=10, sticky="e")
        name_entry = ctk.CTkEntry(add_window, font=("Helvetica", 40, "bold"), width=500)
        name_entry.grid(row=1, column=1, padx=30, pady=10)

        ctk.CTkLabel(add_window, text="Lot No:", font=("Helvetica", 40, "bold")).grid(row=2, column=0, padx=30, pady=10, sticky="e")
        lot_entry = ctk.CTkEntry(add_window, font=("Helvetica", 40, "bold"), width=500)
        lot_entry.grid(row=2, column=1, padx=30, pady=10)

        ctk.CTkLabel(add_window, text="거래처명:", font=("Helvetica", 40, "bold")).grid(row=3, column=0, padx=30, pady=10, sticky="e")
        company_entry = ctk.CTkEntry(add_window, font=("Helvetica", 40, "bold"), width=500)
        company_entry.grid(row=3, column=1, padx=30, pady=10)

        ctk.CTkLabel(add_window, text="유통기한:", font=("Helvetica", 40, "bold")).grid(row=4, column=0, padx=30, pady=10, sticky="e")
        until_entry = ctk.CTkEntry(add_window, font=("Helvetica", 40, "bold"), width=500, placeholder_text="ex) 1998-10-22")
        until_entry.grid(row=4, column=1, padx=30, pady=10)

        ctk.CTkLabel(add_window, text="입고량(kg):", font=("Helvetica", 40, "bold")).grid(row=5, column=0, padx=30, pady=10, sticky="e")
        L_entry = ctk.CTkEntry(add_window, font=("Helvetica", 40, "bold"), width=500)
        L_entry.grid(row=5, column=1, padx=30, pady=10)

        def submit_order():
            global ingredients

            code = code_entry.get()
            name = name_entry.get()
            lot = lot_entry.get()
            company = company_entry.get()
            until = until_entry.get()
            L = L_entry.get()

            if not all([code, name, lot, company, until, L]): #더 간결하게 수정
                CTkMessagebox(title="오류", message="모든 필드를 채워주세요.", icon="cancel")
                return #함수 종료
            try:
                L = int(L)
            except ValueError:
                CTkMessagebox(title="오류", message="입고량은 숫자로 입력해야 합니다.", icon="cancel")
                return #함수 종료

            new_ingredient = {
                "원료 코드": code,
                "원료명": name,
                "Lot no.": lot,
                "거래처명": company,
                "유통기한": until,
                "입고량(kg)": L,
                "현재량(kg)": L
            }
            ingredients = pd.concat([ingredients, pd.DataFrame(new_ingredient, index=[0])], ignore_index=True)
            ingredients.to_csv(file_name, index=False)
            refresh_tree()
            add_window.destroy()

        submit_button = ctk.CTkButton(add_window, text="추가", font=("Helvetica", 50, "bold"), command=submit_order, width=300, height=75) # 버튼 크기, 폰트 조정
        submit_button.grid(row=6, column=0, columnspan=2, pady=30)  # pady 값 조정

        add_window.mainloop()
    def delete_order():
        selected_items = tree.selection()
        if not selected_items:
            CTkMessagebox(title="알림", message="삭제할 항목을 선택해주세요.", icon="cancel")
            return

        # 삭제하기 전에 확인 메시지 표시
        if CTkMessagebox(title="삭제 확인", message="선택한 항목을 삭제하시겠습니까?", icon="question").get():
            global ingredients
            indices_to_drop = []
            for item in selected_items:
                item_values = tree.item(item, 'values')
                
                # DataFrame에서 삭제할 데이터의 인덱스를 찾기
                for index, row in ingredients.iterrows():
                    row_values = list(row)
                    if len(item_values) == len(row_values):
                        match = True
                    for i in range(len(item_values)):
                        if str(item_values[i]) != str(row_values[i]):
                            match = False
                            break
                    if match:
                        indices_to_drop.append(index)
                        break
                    
            # DataFrame에서 행 삭제
            ingredients.drop(indices_to_drop, inplace=True)
            ingredients = ingredients.reset_index(drop=True)
            ingredients.to_csv(file_name, index=False)
            refresh_tree()

    def save_data():
        window.destroy()

    # 버튼 프레임 생성
    button_frame = ctk.CTkFrame(window)
    button_frame.pack(pady=10)

    # 버튼 생성 및 배치
    add_button = ctk.CTkButton(button_frame, text="신규 입고", command=add_order, height=100, width= 300, font=("Helvetica", 40, "bold"))
    add_button.pack(side="left", padx=10)

    delete_button = ctk.CTkButton(button_frame, text="재고 삭제", command=delete_order, height=100, width= 300, font=("Helvetica", 40, "bold"))
    delete_button.pack(side="left", padx=10)

    save_button = ctk.CTkButton(button_frame, text="종료", command=save_data, height=100, width= 300, font=("Helvetica", 40, "bold"))
    save_button.pack(side="left", padx=10)

    window.mainloop()


if __name__ == "__main__":
    ingredient_manage()