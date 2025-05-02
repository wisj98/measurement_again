import customtkinter as ctk
import pickle
import pandas as pd
import os
from datetime import datetime
import tkinter.ttk as ttk
from CTkMessagebox import CTkMessagebox

def order_start():
    #---------------------------------------------------------------------------------------------------------
    with open("config.pickle", "rb") as fr:
        config = pickle.load(fr)

    data_path = config["경로"] + "/data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    today = datetime.today().strftime("%Y_%m_%d")
    file_name = data_path + "/" + today + "_작업지시.csv"
    if os.path.isfile(file_name):
        orders = pd.read_csv(file_name)
        orders = orders.sort_values(by="현재 단계").reset_index(drop=True)
        print(file_name)
    else:
        # test
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
    #---------------------------------------------------------------------------------------------------------
    window = ctk.CTk()
    window.title("작업 지시")
    window.attributes('-fullscreen', True)

    up_frame = ctk.CTkFrame(master=window, height=40, fg_color="#333333", corner_radius=0)
    up_frame.pack(side="top", fill="x",pady=[0,5])

    title_label = ctk.CTkLabel(
        window,
        font=("pretendard medium", 14, "bold"),
        text="작업 지시",
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
    #---------------------------------------------------------------------------------------------------------
    columns_frame = ctk.CTkFrame(master=window, height=40)
    columns_frame.pack(side="top", fill="x")

    column_titles = [
        "작업일", "지시자", "지시 시간", "제품명", "작업량(Kg)",
        "배합가마", "현재단계", "내역", "확정", "삭제"
    ]

    # column 수에 맞게 weight 지정 (동일한 비율로 배분)
    column_widths = [175, 175, 175, 300, 175, 175, 175, 175, 175, 175]

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
    #---------------------------------------------------------------------------------------------------------
    inner_frame = ctk.CTkScrollableFrame(master=window, height=900)
    inner_frame.pack(side="top", fill="x")

    def check(orders, idx):
        with open(f"{config["경로"]}/recipe.pickle", "rb") as fr: pass
        print(orders.iloc[idx])

    def save(orders, idx):
        orders.loc[idx, "현재 단계"] = "1:작업 전"
        orders.to_csv(file_name, index=False)
        refresh_window(orders)

    def delete(orders, idx):
        orders = orders.drop(index=idx).reset_index(drop=True)
        orders.to_csv(file_name, index=False)
        refresh_window(orders)

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
                    text = "저장",font=("pretendard medium", 12, "bold"),
                    width=column_widths[idx+2],
                    height=40,
                    anchor="center", 
                    fg_color="#BBBBBB",
                    text_color="black",
                    command=lambda i=i, orders=orders: save(orders, i), corner_radius=0
                    )
            save_button.grid(row=0, column=idx+2, sticky="nsew", padx=1)

            delete_button = ctk.CTkButton(master=order_frame,
                    text = "삭제",font=("pretendard medium", 12, "bold"),
                    width=column_widths[idx+3],
                    height=40,
                    anchor="center", 
                    fg_color="#BBBBBB",
                    text_color="black",
                    command=lambda i=i, orders=orders: delete(orders, i), corner_radius=0)
            delete_button.grid(row=0, column=idx+3, sticky="nsew", padx=1)
        if refresh:
            window.after(30000, lambda refresh=refresh: refresh_window(refresh==True))

    refresh_window(refresh=True)
#---------------------------------------------------------------------------------------------------------

    def add_order():
        add_window = ctk.CTk()
        add_window.title("작업 지시 추가")
        add_window.geometry("775x400")  # 창 크기 3배로 조정

        workers = config["작업자"]["지시자"]
        gamas = config["작업자"]["가마"]

        with open(f"{config['경로']}/recipe.pickle", "rb") as fr:
            recipes = pickle.load(fr).keys()
        ctk.CTkLabel(add_window, text="지시자:", font=("Helvetica", 30, "bold")).grid(row=0, column=0, padx=30, pady=(50,10), sticky="e")
        worker_combobox = ctk.CTkComboBox(add_window, font=("Helvetica", 30, "bold"), width=500, values=workers)
        worker_combobox.grid(row=0, column=1, padx=30, pady=(50,10))

        ctk.CTkLabel(add_window, text="제품명:", font=("Helvetica", 30, "bold")).grid(row=1, column=0, padx=30, pady=10, sticky="e")

        options = list(recipes)  # 원하는 옵션 리스트
        product_combobox = ctk.CTkComboBox(add_window, values=options, font=("Helvetica", 30, "bold"), width=500, dropdown_font=("Helvetica", 25, "bold"))
        product_combobox.grid(row=1, column=1, padx=30, pady=10)

        ctk.CTkLabel(add_window, text="작업량(kg):", font=("Helvetica", 30, "bold")).grid(row=2, column=0, padx=30, pady=10, sticky="e")
        amount_entry = ctk.CTkEntry(add_window, font=("Helvetica", 30, "bold"), width=500)
        amount_entry.grid(row=2, column=1, padx=30, pady=10)

        ctk.CTkLabel(add_window, text="배합가마:", font=("Helvetica", 30, "bold")).grid(row=3, column=0, padx=30, pady=10, sticky="e")
        gama_combobox = ctk.CTkComboBox(add_window, font=("Helvetica", 30, "bold"), width=500, values=gamas)
        gama_combobox.grid(row=3, column=1, padx=30, pady=10)

        def submit_order():
            orders = pd.read_csv(file_name)

            worker = worker_combobox.get()
            product = product_combobox.get()
            amount = amount_entry.get()
            gama = gama_combobox.get()

            if not worker or not product or not amount:
                CTkMessagebox(title="오류", message="모든 필드를 채워주세요.", icon="cancel")
                add_window.destroy()
            try:
                amount = int(amount)
            except ValueError:
                CTkMessagebox(title="오류", message="작업량은 숫자로 입력해야 합니다.", icon="cancel")
                add_window.destroy()
                return

            new_order = {
                "작업일": datetime.today().strftime("%Y-%m-%d"),
                "지시자": worker,
                "지시 시간": datetime.now().strftime("%H:%M"),
                "제품명": product,
                "작업량(kg)": amount,
                "배합 가마": gama,
                "현재 단계": "0: 확정 전"
            }
            orders = pd.concat([orders, pd.DataFrame(new_order, index=[0])], ignore_index=True)
            orders.to_csv(file_name, index=False)
            refresh_window()
            add_window.destroy()

        submit_button = ctk.CTkButton(add_window, text="작업 추가", font=("Helvetica", 40, "bold"), command=submit_order, width = 750, height = 75)
        submit_button.grid(row=4, column=0, columnspan=2, pady=30)

        add_window.mainloop()

    def save_data():
        window.destroy()

    # 버튼 프레임 생성
    button_frame = ctk.CTkFrame(window)
    button_frame.pack(pady=10)

    # 버튼 생성 및 배치
    add_button = ctk.CTkButton(button_frame, text="작업 지시", font=("Helvetica", 40, "bold"), command=add_order, height=100, width= 300)
    add_button.pack(side="left", padx=10)

    save_button = ctk.CTkButton(button_frame, text="종료하기", font=("Helvetica", 40, "bold"), command=save_data, height=100, width= 300)
    save_button.pack(side="left", padx=10)

    window.mainloop()


if __name__ == "__main__":
    order_start()