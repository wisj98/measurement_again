import customtkinter as ctk
from tkinter import filedialog
import pickle

with open("config.pickle","rb") as fr:
    config = pickle.load(fr)

def config_start():
    window = ctk.CTk()
    window.geometry("600x400")
    window.title("환경 설정")

    root_button = ctk.CTkButton(master=window, text="메인 경로 설정", command=root)
    root_button.pack(pady=20, padx=20)

    user_button = ctk.CTkButton(master=window, text="작업자 설정", command=user)
    user_button.pack(pady=20, padx=20)

    right_button = ctk.CTkButton(master=window, text="권한 설정", command=right)
    right_button.pack(pady=20, padx=20)

    window.mainloop()

def root():
    root_ = ctk.CTk()
    root_.geometry("700x150")
    root_.title("메인 경로 설정")

    path_label = ctk.CTkLabel(root_, text=f"현재 경로: {config["경로"]}", wraplength=350, anchor="w")
    path_label.pack(pady=20, padx=10)

    def set_new_path():
        new_path = filedialog.askdirectory(title="새로운 경로 선택")
        if new_path:
            config["경로"] = new_path
            path_label.configure(text=f"현재 경로: {config["경로"]}")
            with open("config.pickle","wb") as f:
                pickle.dump(config, f)
    
    set_path_button = ctk.CTkButton(root_, text="새로운 경로 지정", command=set_new_path)
    set_path_button.pack(pady=10)

    root_.mainloop()

def right():
    right_ = ctk.CTk()
    right_.geometry("200x300")
    right_.title("권한 설정")

    checkbox_vars = {}

    def create_checkboxes():
        for i, (key, value) in enumerate(config["권한"].items()):
            checkbox_vars[key] = ctk.BooleanVar(value=value)
            checkbox = ctk.CTkCheckBox(
                right_, text=key, variable=checkbox_vars[key]
            )
            checkbox.pack(pady=5, padx=10, anchor="w")

    def save_config():
        for key, var in checkbox_vars.items():
            config["권한"][key] = var.get()
        with open("config.pickle","wb") as f:
                pickle.dump(config, f)

    create_checkboxes()

    save_button = ctk.CTkButton(right_, text="저장하기", command=save_config)
    save_button.pack(pady=20)

    right_.mainloop()

def user():
    user_window = ctk.CTk()
    user_window.geometry("300x450")
    user_window.title("작업자 관리")
    
    user_list = sorted(config["작업자"])

    selected_now = None

    label = ctk.CTkLabel(master=user_window, text="작업자 목록")
    label.pack(pady=10, padx=20)

    text_box = ctk.CTkTextbox(master=user_window, wrap="word")
    text_box.pack(pady=20, padx=20, fill="both", expand=True)

    def on_text_box_click(event):
        nonlocal selected_now
        text_box.tag_add("sel", "current linestart", "current lineend")
        text_box.tag_add("selected", "current linestart", "current lineend")  # 선택된 행에 "selected" 태그 추가

        # 선택된 부분 출력
        selected_text = text_box.get("sel.first", "sel.last")
        label_now.configure(text=f"선택된 작업자: {selected_text}")
        selected_now = selected_text

    text_box.bind("<Button-1>", on_text_box_click)
    text_box.bind("<Double-Button-1>", on_text_box_click)

    # user_list의 요소들을 텍스트 박스에 추가
    for user in user_list:
        text_box.insert("end", user + "\n")
        
    def add_user():
        new_user_window = ctk.CTk()
        new_user_window.geometry("600x150")
        new_user_window.title("작업자 추가")

        def new_user():
            config["작업자"].append(entry.get())
            with open("config.pickle","wb") as f:
                pickle.dump(config, f)
            new_user_window.destroy()
            text_box.delete("1.0", "end")  # 텍스트 박스 내용 지우기
            user_list = sorted(config["작업자"])  # 레시피 목록 업데이트
            for user in user_list:
                text_box.insert("end", user + "\n")

        label = ctk.CTkLabel(master=new_user_window, text="""추가할 작업자의 이름(코드)을 입력해주세요.""")
        label.pack(pady=10, padx=20)

        # 글자를 입력할 수 있는 박스 생성
        entry = ctk.CTkEntry(master=new_user_window)
        entry.pack(pady=10, padx=20, fill="x", expand=True)

        # "추가" 버튼 생성
        add_button = ctk.CTkButton(master=new_user_window, text="추가", command = new_user)
        add_button.pack(pady=10, padx=20)

        new_user_window.mainloop()

    def delete_user():
        try:
            selected_user = selected_now # 선택된 레시피 이름 가져오기
            if selected_user in config["작업자"]:
                config["작업자"].remove(selected_user)
                with open("config.pickle","wb") as f:
                    pickle.dump(config, f)
                text_box.delete("1.0", "end")  # 텍스트 박스 내용 지우기
                user_list = sorted(config["작업자"])  # 레시피 목록 업데이트
                for user in user_list:
                    text_box.insert("end", user + "\n")
            else:
                print("삭제할 유저를 선택하세요.")
        except:
            print("선택한 작업자가 존재하지 않습니다.")

    # 현재 라벨
    label_now = ctk.CTkLabel(master = user_window, text="선택된 작업자:")
    label_now.pack(pady=5, padx=20)

    add_button = ctk.CTkButton(master=user_window, text="작업자 추가", command = add_user)
    add_button.pack(pady=5, padx=20)

    delete_button = ctk.CTkButton(master=user_window, text="작업자 삭제", command=delete_user)
    delete_button.pack(pady=5, padx=20)

    user_window.mainloop()

if __name__ == "__main__":
    config_start()