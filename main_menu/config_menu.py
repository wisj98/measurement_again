import customtkinter as ctk
from tkinter import filedialog, ttk
import pickle

with open("config.pickle","rb") as fr:
    config = pickle.load(fr)

def config_start():
    window = ctk.CTk()
    window.geometry("600x400")
    window.title("환경 설정")

    root_button = ctk.CTkButton(master=window, text="메인 경로 설정", command=root)
    root_button.pack(pady=20, padx=20)

    user_button = ctk.CTkButton(master=window, text="작업자 설정", command=user_)
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

def user_():
    def user__(witch):
      user_window = ctk.CTk()
      user_window.geometry("300x450")
      user_window.title("작업자 관리")
  
      user_list = sorted(config["작업자"][witch])
      selected_now = None
  
      label = ctk.CTkLabel(master=user_window, text="작업자 목록")
      label.pack(pady=10, padx=20)
  
      # Treeview 생성
      tree = ttk.Treeview(user_window, columns=("Name"), show="headings")
      tree.heading("Name", text="작업자 이름")
      tree.pack(pady=10, padx=20, fill="both", expand=True)
  
      # 작업자 목록을 Treeview에 추가
      for user in user_list:
          tree.insert("", "end", values=(user,))
  
      def on_tree_select(event):
          """Treeview에서 항목을 선택했을 때 실행되는 함수"""
          nonlocal selected_now
          selected_item = tree.selection()
          if selected_item:
              selected_now = tree.item(selected_item[0], "values")[0]
              label_now.configure(text=f"선택된 작업자: {selected_now}")
  
      tree.bind("<<TreeviewSelect>>", on_tree_select)
  
      def add_user(witch):
          new_user_window = ctk.CTk()
          new_user_window.geometry("400x200")
          new_user_window.title("작업자 추가")
  
          def new_user():
              new_name = entry.get().strip()
              if new_name:
                  config["작업자"][witch].append(new_name)
                  with open("config.pickle", "wb") as f:
                      pickle.dump(config, f)
                  new_user_window.destroy()
                  update_treeview()
  
          label = ctk.CTkLabel(master=new_user_window, text="추가할 작업자의 이름을 입력하세요.")
          label.pack(pady=10)
  
          entry = ctk.CTkEntry(master=new_user_window)
          entry.pack(pady=10, padx=20, fill="x", expand=True)
  
          add_button = ctk.CTkButton(master=new_user_window, text="추가", command=new_user)
          add_button.pack(pady=10)
  
          new_user_window.mainloop()
  
      def delete_user():
          """선택된 작업자를 삭제"""
          nonlocal selected_now
          if selected_now and selected_now in config["작업자"][witch]:
              config["작업자"][witch].remove(selected_now)
              with open("config.pickle", "wb") as f:
                  pickle.dump(config, f)
              selected_now = None
              update_treeview()
              label_now.configure(text="선택된 작업자: 없음")
          else:
              print("삭제할 유저를 선택하세요.")
  
      def update_treeview():
          """Treeview 내용을 업데이트하는 함수"""
          tree.delete(*tree.get_children())  # 기존 목록 삭제
          for user in sorted(config["작업자"][witch]):
              tree.insert("", "end", values=(user,))
  
      # 현재 선택된 작업자 표시 라벨
      label_now = ctk.CTkLabel(master=user_window, text="선택된 작업자: 없음")
      label_now.pack(pady=5)
  
      # 추가 버튼
      add_button = ctk.CTkButton(master=user_window, text="작업자 추가", command=lambda: add_user(witch))
      add_button.pack(pady=5)
  
      # 삭제 버튼
      delete_button = ctk.CTkButton(master=user_window, text="작업자 삭제", command=delete_user)
      delete_button.pack(pady=5)
  
      user_window.mainloop()

    window = ctk.CTk()
    window.geometry("570x350")
    window.title("수정할 작업자 리스트 선택")

    roles = list(config["작업자"].keys())

    frame = ctk.CTkFrame(window, width=450, height=300)
    frame.grid(row=0,column=0, padx=20, pady=30)

    label_1 = ctk.CTkButton(frame, width = 100, height = 20, text = roles[0], font=("Helvetica", 20, "bold"), command = lambda: user__(roles[0]))
    label_1.grid(row=0,column=0,padx=5, pady=5)

    label_2 = ctk.CTkButton(frame, width = 100, height = 20, text = roles[1], font=("Helvetica", 20, "bold"), command = lambda: user__(roles[1]))
    label_2.grid(row=0,column=1,padx=5, pady=5)

    label_3 = ctk.CTkButton(frame, width = 100, height = 20, text = roles[2], font=("Helvetica", 20, "bold"), command = lambda: user__(roles[2]))
    label_3.grid(row=0,column=2,padx=5, pady=5)

    label_4 = ctk.CTkButton(frame, width = 100, height = 20, text = roles[3], font=("Helvetica", 20, "bold"), command = lambda: user__(roles[3]))
    label_4.grid(row=0,column=3,padx=5, pady=5)

    frame_1 = ctk.CTkScrollableFrame(frame, width = 100, height = 200)
    frame_1.grid(row=1,column=0,padx=5, pady=10)

    for user in config["작업자"][roles[0]]:
        ctk.CTkLabel(frame_1, text = user, font=("Helvetica", 15, "bold"), width=100, height=18).pack(padx=3, pady=3)

    frame_2 = ctk.CTkScrollableFrame(frame, width = 100, height = 200)
    frame_2.grid(row=1,column=1,padx=5, pady=10)

    for user in config["작업자"][roles[1]]:
        ctk.CTkLabel(frame_2, text = user, font=("Helvetica", 15, "bold"), width=100, height=18).pack(padx=3, pady=3)
    
    frame_3 = ctk.CTkScrollableFrame(frame, width = 100, height = 200)
    frame_3.grid(row=1,column=2,padx=5, pady=10)
    
    for user in config["작업자"][roles[2]]:
        ctk.CTkLabel(frame_3, text = user, font=("Helvetica", 15, "bold"), width=100, height=18).pack(padx=3, pady=3)

    frame_4 = ctk.CTkScrollableFrame(frame, width = 100, height = 200)
    frame_4.grid(row=1,column=3,padx=5, pady=10)

    for user in config["작업자"][roles[3]]:
        ctk.CTkLabel(frame_4, text = user, font=("Helvetica", 15, "bold"), width=100, height=18).pack(padx=3, pady=3)

    window.mainloop()

if __name__ == "__main__":
    config_start()