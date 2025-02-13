import customtkinter as ctk
import pickle

with open("config.pickle","rb") as fr:
    config = pickle.load(fr)

file_path = f"{config["경로"]}/recipe.pickle"
with open(file_path, "rb") as fr:
    recipes = pickle.load(fr)

def recipe_manage():
    recipe_window = ctk.CTk()
    recipe_window.geometry("300x450")
    recipe_window.title("레시피 관리")

    # with open(file_path,"rb") as fr:
    #     recipes = pickle.load(fr)
    
    recipe_list = sorted(recipes.keys())

    selected_now = None

    label = ctk.CTkLabel(master=recipe_window, text="레시피 목록")
    label.pack(pady=10, padx=20)

    text_box = ctk.CTkTextbox(master=recipe_window, wrap="word")
    text_box.pack(pady=20, padx=20, fill="both", expand=True)

    def on_text_box_click(event):
        nonlocal selected_now
        text_box.tag_add("sel", "current linestart", "current lineend")
        text_box.tag_add("selected", "current linestart", "current lineend")

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
        fix_recipe_window = ctk.CTk()
        fix_recipe_window.geometry("600x250")
        fix_recipe_window.title("레시피 수정")
        fixing_recipe = recipes[selected_now]["배합비"]
        def fix_recipe():
            try:
                new = entry.get().split("=")
                recipes[new[0]]["배합비"] = [[x.split("/")[0],float(x.split("/")[1]),float(x.split("/")[2])] for x in new[1].split("+")]
                recipes[new[0]]["배합법"] = entry_.get().split(",")
                with open("recipe.pickle", "wb") as fw: 
                        pickle.dump(recipes, fw)
                text_box.delete("1.0", "end")
                recipe_list = sorted(recipes.keys())
                for recipe in recipe_list:
                    text_box.insert("end", recipe + "\n")
                fix_recipe_window.destroy()
            except:
                warning_window = ctk.CTk()
                warning_window.geometry("300x100")
                warning_window.title("경고")

                # "레시피 양식에 맞춰서 작성해 주세요." 레이블 생성
                warning_label = ctk.CTkLabel(master=warning_window, text="배합비 양식에 맞춰서 작성해 주세요.")
                warning_label.pack(pady=10, padx=20)

                # "닫기" 버튼 생성 및 command 설정
                def close_warning_window():
                    warning_window.destroy()

                close_button = ctk.CTkButton(master=warning_window, text="닫기", command=close_warning_window)
                close_button.pack(pady=10, padx=20)

                warning_window.mainloop()
        # "example" 레이블 생성
        label = ctk.CTkLabel(master=fix_recipe_window, text="""배합비를 입력해주세요. \n예시)용액_1=우유/10/1+식초/5/1+간장/3/1""")
        label.pack(pady=5, padx=20)

        # 글자를 입력할 수 있는 박스 생성
        entry = ctk.CTkEntry(master=fix_recipe_window)
        entry.pack(pady=0, padx=20, fill="x", expand=True)
        entry.insert(0,f"{selected_now}={"+".join([f"{x[0]}/{x[1]}/{x[2]}" for x in fixing_recipe])}")

        label_ = ctk.CTkLabel(master=fix_recipe_window, text="""배합법을 입력해주세요. \n예시)우유 붓기,식초 붓기,섞기,간장 붓기""")
        label_.pack(pady=5, padx=20)

        entry_ = ctk.CTkEntry(master=fix_recipe_window)
        entry_.pack(pady=0, padx=20, fill="x", expand=True)
        entry_.insert(0,f"{",".join(recipes[selected_now]["배합법"])}")
        # "추가" 버튼 생성
        add_button = ctk.CTkButton(master=fix_recipe_window, text="수정", command = fix_recipe)
        add_button.pack(pady=10, padx=20)

        fix_recipe_window.mainloop()
        
    def add_recipe():
        new_recipe_window = ctk.CTk()
        new_recipe_window.geometry("600x250")
        new_recipe_window.title("레시피 추가")

        def new_recipe():
            try:
                new = entry.get().split("=")
                recipes[new[0]]["배합비"] = [[x.split("/")[0],float(x.split("/")[1]),float(x.split("/")[2])] for x in new[1].split("+")]
                recipes[new[0]]["배합법"] = entry_.get().split(",")
                with open("recipe.pickle", "wb") as fw: 
                        pickle.dump(recipes, fw)
                text_box.delete("1.0", "end")
                recipe_list = sorted(recipes.keys())
                for recipe in recipe_list:
                    text_box.insert("end", recipe + "\n")
                new_recipe_window.destroy()
            except:
                warning_window = ctk.CTk()
                warning_window.geometry("300x100")
                warning_window.title("경고")

                # "레시피 양식에 맞춰서 작성해 주세요." 레이블 생성
                warning_label = ctk.CTkLabel(master=warning_window, text="배합비 양식에 맞춰서 작성해 주세요.")
                warning_label.pack(pady=10, padx=20)

                # "닫기" 버튼 생성 및 command 설정
                def close_warning_window():
                    warning_window.destroy()

                close_button = ctk.CTkButton(master=warning_window, text="닫기", command=close_warning_window)
                close_button.pack(pady=10, padx=20)

                warning_window.mainloop()
        # "example" 레이블 생성
        label = ctk.CTkLabel(master=new_recipe_window, text="""배합비를 입력해주세요. \n예시)용액_1=우유/10/1+식초/5/1+간장/3/1""")
        label.pack(pady=5, padx=20)

        # 글자를 입력할 수 있는 박스 생성
        entry = ctk.CTkEntry(master=new_recipe_window)
        entry.pack(pady=0, padx=20, fill="x", expand=True)

        label_ = ctk.CTkLabel(master=new_recipe_window, text="""배합법을 입력해주세요. \n예시)우유 붓기,식초 붓기,섞기,간장 붓기""")
        label_.pack(pady=5, padx=20)

        entry_ = ctk.CTkEntry(master=new_recipe_window)
        entry_.pack(pady=0, padx=20, fill="x", expand=True)

        # "추가" 버튼 생성
        add_button = ctk.CTkButton(master=new_recipe_window, text="추가", command = new_recipe)
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
    label_now = ctk.CTkLabel(master = recipe_window, text="선택된 레시피:")
    label_now.pack(pady=5, padx=20)

    # 버튼 생성
    modify_button = ctk.CTkButton(master=recipe_window, text="레시피 수정", command = fixing_recipe)
    modify_button.pack(pady=5, padx=20)

    add_button = ctk.CTkButton(master=recipe_window, text="레시피 추가", command = add_recipe)
    add_button.pack(pady=5, padx=20)

    delete_button = ctk.CTkButton(master=recipe_window, text="레시피 삭제", command=delete_recipe)
    delete_button.pack(pady=5, padx=20)

    recipe_window.mainloop()

if __name__ == "__main__":
    recipe_manage()