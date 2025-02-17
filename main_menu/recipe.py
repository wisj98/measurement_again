import customtkinter as ctk
import pickle
from tkinter import ttk
from main_menu.style import configure_treeview_style_for_recipe

# 설정 파일 로드
with open("config.pickle", "rb") as fr:
    config = pickle.load(fr)

file_path = f"{config['경로']}/recipe.pickle"
with open(file_path, "rb") as fr:
    recipes = pickle.load(fr)

def recipe_manage():
    recipe_window = ctk.CTk()
    recipe_window.geometry("600x900+0+0")
    recipe_window.title("레시피 관리")
    configure_treeview_style_for_recipe(recipe_window)

    recipe_list = sorted(recipes.keys())
    selected_now = None

    label = ctk.CTkLabel(master=recipe_window, text="레시피 목록", font=("Arial", 24, "bold"))
    label.pack(pady=(50, 10), padx=40)

    # Treeview 설정
    tree_frame = ctk.CTkFrame(master=recipe_window)
    tree_frame.pack(pady=(0, 10), padx=40, fill="both", expand=True)

    columns = ("레시피 이름",)
    tree = ttk.Treeview(tree_frame, columns=columns, show="tree")
    tree.column("#0", width=400, minwidth=400, stretch=True)

    # 트리뷰 항목 추가
    for recipe in recipe_list:
        tree.insert("", "end", iid=recipe, text=recipe)

    tree.pack(fill="both", expand=True)

    # 선택된 레시피 라벨
    label_now = ctk.CTkLabel(master=recipe_window, text="선택된 레시피: 없음", font=("Arial", 18))
    label_now.pack(pady=10)

    # 레시피 선택 이벤트
    def on_tree_select(event):
        nonlocal selected_now
        selected_item = tree.selection()
        if selected_item:
            selected_now = tree.item(selected_item[0])["text"]
            label_now.configure(text=f"선택된 레시피: {selected_now}")

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def fixing_recipe():
        if not selected_now:
            return
        fix_recipe_window = ctk.CTk()
        fix_recipe_window.geometry("1200x500")
        fix_recipe_window.title("레시피 수정")

        fixing_recipe = recipes[selected_now]["배합비"]

        def fix_recipe():
            try:
                new = entry.get().split("=")
                recipes[new[0]]["배합비"] = [[x.split("/")[0], float(x.split("/")[1]), float(x.split("/")[2])] for x in new[1].split("+")]
                recipes[new[0]]["배합법"] = entry_.get().split(",")
                with open(file_path, "wb") as fw:
                    pickle.dump(recipes, fw)
                tree.delete(*tree.get_children())  # 트리뷰 초기화
                for recipe in sorted(recipes.keys()):
                    tree.insert("", "end", iid=recipe, text=recipe)  # 트리뷰 다시 추가
                fix_recipe_window.destroy()
            except:
                warning_window = ctk.CTk()
                warning_window.geometry("300x100")
                warning_window.title("경고")

                warning_label = ctk.CTkLabel(master=warning_window, text="배합비 양식에 맞춰서 작성해 주세요.")
                warning_label.pack(pady=10, padx=20)

                def close_warning_window():
                    warning_window.destroy()

                close_button = ctk.CTkButton(master=warning_window, text="닫기", command=close_warning_window)
                close_button.pack(pady=10, padx=20)

                warning_window.mainloop()

        label = ctk.CTkLabel(master=fix_recipe_window, text="배합비를 입력해주세요. \n예시)용액_1=우유/10/1+식초/5/1+간장/3/1", font=("Arial", 24, "bold"))
        label.pack(pady=(20, 0), padx=20)

        entry = ctk.CTkEntry(master=fix_recipe_window, height=50, font=("Arial", 24, "bold"))
        entry.pack(pady=0, padx=20, fill="x", expand=True)
        entry.insert(0, f"{selected_now}={" + ".join([f"{x[0]}/{x[1]}/{x[2]}" for x in fixing_recipe])}")

        label_ = ctk.CTkLabel(master=fix_recipe_window, text="배합법을 입력해주세요. \n예시)우유 붓기,식초 붓기,섞기,간장 붓기", font=("Arial", 24, "bold"))
        label_.pack(pady=(0, 0), padx=20)

        entry_ = ctk.CTkEntry(master=fix_recipe_window, height=50, font=("Arial", 24, "bold"))
        entry_.pack(pady=0, padx=20, fill="x", expand=True)
        entry_.insert(0, f"{",".join(recipes[selected_now]["배합법"])}")

        add_button = ctk.CTkButton(master=fix_recipe_window, text="수정", command=fix_recipe, font=("Arial", 24, "bold"), height=50, width=200)
        add_button.pack(pady=10, padx=20)

        fix_recipe_window.mainloop()

    def delete_recipe():
        nonlocal selected_now
        if selected_now and selected_now in recipes:
            del recipes[selected_now]
            with open(file_path, "wb") as fw:
                pickle.dump(recipes, fw)
            tree.delete(*tree.get_children())  # 트리뷰 초기화
            for recipe in sorted(recipes.keys()):
                tree.insert("", "end", iid=recipe, text=recipe)  # 트리뷰 다시 추가
            selected_now = None
            label_now.configure(text="선택된 레시피: 없음")

    # 버튼 추가
    button_frame = ctk.CTkFrame(master=recipe_window)
    button_frame.pack(pady=10)

    fix_button = ctk.CTkButton(master=button_frame, text="레시피 수정", command=fixing_recipe, font=("Helvetica", 20, "bold"), width=100, height=30)
    fix_button.grid(row=0, column=0, padx=10)

    delete_button = ctk.CTkButton(master=button_frame, text="레시피 삭제", command=delete_recipe, font=("Helvetica", 20, "bold"), width=100, height=30)
    delete_button.grid(row=0, column=1, padx=10)

    recipe_window.mainloop()

if __name__ == "__main__":
    recipe_manage()
