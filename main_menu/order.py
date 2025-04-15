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
        orders = pd.DataFrame(data)
        orders.to_csv(file_name, index=False)
    #---------------------------------------------------------------------------------------------------------
    orders = pd.read_csv(file_name)
    window = ctk.CTk()
    window.title("작업 지시")
    window.attributes('-fullscreen', True)

    up_frame = ctk.CTkFrame(master=window, height=40)
    up_frame.pack(side="top", fill="x")

    title_label = ctk.CTkLabel(window, font=("pretendard medium", 14, "bold"), text = "작업지시")
    title_label.place(relx=0.0, x=10, y=10, anchor="nw")

    time_label = ctk.CTkLabel(window, font=("pretendard medium", 14, "bold"))
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
    column_widths = [178, 178, 178, 300, 178, 178, 178, 178, 178, 178]

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

    def refresh_window(orders = False):
        if not orders:
            orders = pd.read_csv(file_name)
        for widget in inner_frame.winfo_children():
            widget.destroy()
        for i in range(len(orders)):
            order_frame = ctk.CTkFrame(master=inner_frame, height=45)
            order_frame.pack(side="top", fill="x")

            for idx, title in enumerate(orders.columns):
                label = ctk.CTkLabel(
                    master=order_frame,
                    text=orders.iloc[idx][title],
                    font=("pretendard medium", 12, "bold"),
                    width=column_widths[idx],
                    height=40,
                    anchor="center",  # 가운데 정렬
                    fg_color="#52ADD4",  # 이전에 조정한 컬러
                    text_color="black"
                )
                label.grid(row=0, column=idx, sticky="nsew", padx=1)
        
        window.after(20000, refresh_window)

    refresh_window()

    def add_order():
        add_window = ctk.CTk()
        add_window.title("작업 지시 추가")
        add_window.geometry("850x550")  # 창 크기 3배로 조정

        workers = config["작업자"]["지시자"]
        gamas = config["작업자"]["가마"]

        with open(f"{config['경로']}/recipe.pickle", "rb") as fr:
            recipes = pickle.load(fr).keys()
        ctk.CTkLabel(add_window, text="작업자:", font=("Helvetica", 40, "bold")).grid(row=0, column=0, padx=30, pady=(100,10), sticky="e")
        worker_combobox = ctk.CTkComboBox(add_window, font=("Helvetica", 40, "bold"), width=500, values=workers)
        worker_combobox.grid(row=0, column=1, padx=30, pady=(100,10))

        ctk.CTkLabel(add_window, text="작업물:", font=("Helvetica", 40, "bold")).grid(row=1, column=0, padx=30, pady=10, sticky="e")

        options = list(recipes)  # 원하는 옵션 리스트
        product_combobox = ctk.CTkComboBox(add_window, values=options, font=("Helvetica", 40, "bold"), width=500, dropdown_font=("Helvetica", 25, "bold"))
        product_combobox.grid(row=1, column=1, padx=30, pady=10)

        ctk.CTkLabel(add_window, text="작업량(kg):", font=("Helvetica", 40, "bold")).grid(row=2, column=0, padx=30, pady=10, sticky="e")
        amount_entry = ctk.CTkEntry(add_window, font=("Helvetica", 40, "bold"), width=500)
        amount_entry.grid(row=2, column=1, padx=30, pady=10)

        ctk.CTkLabel(add_window, text="배합 가마:", font=("Helvetica", 40, "bold")).grid(row=3, column=0, padx=30, pady=10, sticky="e")
        gama_combobox = ctk.CTkComboBox(add_window, font=("Helvetica", 40, "bold"), width=500, values=gamas)
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
                "작업물": product,
                "작업량(kg)": amount,
                "배합 가마": gama,
                "현재 단계": "0: 작업 전"
            }
            orders = pd.concat([orders, pd.DataFrame(new_order, index=[0])], ignore_index=True)
            orders.to_csv(file_name, index=False)
            refresh_window()
            add_window.destroy()

        submit_button = ctk.CTkButton(add_window, text="추가", font=("Helvetica", 50, "bold"), command=submit_order, width = 300, height = 75)
        submit_button.grid(row=4, column=0, columnspan=2, pady=30)

        add_window.mainloop()


    def delete_order():
        # 선택된 항목 가져오기
        orders = pd.read_csv(file_name)
        selected_items = tree.selection()
        if not selected_items:
            CTkMessagebox(title="알림", message="삭제할 항목을 선택해주세요.", icon="cancel")
            return

        # 삭제하기 전에 확인 메시지 표시
        if CTkMessagebox(title="삭제 확인", message="선택한 항목을 삭제하시겠습니까?", icon="question").get():
            orders = pd.read_csv(file_name)

            indices_to_drop = []
            for item in selected_items:
                item_values = tree.item(item, 'values')
                
                for index, row in orders.iterrows():
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
                    
            orders.drop(indices_to_drop, inplace=True)

            orders = orders.reset_index(drop=True)
            orders.to_csv(file_name, index=False)
            refresh_window()

    def save_data():
        window.destroy()

    # 버튼 프레임 생성
    button_frame = ctk.CTkFrame(window)
    button_frame.pack(pady=10)

    # 버튼 생성 및 배치
    add_button = ctk.CTkButton(button_frame, text="작업 지시", font=("Helvetica", 40, "bold"), command=add_order, height=100, width= 300)
    add_button.pack(side="left", padx=10)

    delete_button = ctk.CTkButton(button_frame, text="작업 삭제", font=("Helvetica", 40, "bold"), command=delete_order, height=100, width= 300)
    delete_button.pack(side="left", padx=10)

    save_button = ctk.CTkButton(button_frame, text="종료하기", font=("Helvetica", 40, "bold"), command=save_data, height=100, width= 300)
    save_button.pack(side="left", padx=10)

    window.mainloop()


if __name__ == "__main__":
    order_start()