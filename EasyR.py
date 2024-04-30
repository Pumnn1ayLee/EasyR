import os
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
#全局变量，用户信息
user_info = {}

#全局变量，档案信息
mode_window = None
profile_window = None
entry_window = None
profiles = []

# 获取当前用户的个人文件夹路径
user_folder = os.path.expanduser("~")

# 创建一个名为 "UserData" 的文件夹，用于保存用户数据文件
data_folder = os.path.join(user_folder, "UserData")
os.makedirs(data_folder, exist_ok=True)

# 定义 JSON 文件路径
user_info_file = os.path.join(data_folder, "user_info.json")

# 定义用户档案信息文件路径
profile_file = os.path.join(data_folder,"profiles.json")

#全局变量,当前用户登录用户名
current_username = None

def register():
    username = username_entry.get()
    password = password_entry.get()

    if username.strip() == "" or password.strip() == "":
        messagebox.showerror("错误", "用户名和密码不能为空")
    else:
        # 读取已有用户信息
        user_info = read_user_info()

        if username in user_info:
            messagebox.showerror("错误", "用户名已存在")
        else:
            # 添加新用户信息
            user_info[username] = password
            # 保存用户信息到文件
            save_user_info(user_info)
            messagebox.showinfo("成功", "注册成功")

def login():

    global current_username

    username = username_entry.get()
    password = password_entry.get()

    if username.strip() == "" or password.strip() == "":
        messagebox.showerror("错误", "用户名和密码不能为空")
    else:
        #读取用户已有信息
        user_info = read_user_info()
        if username not in user_info or user_info[username] != password:
            messagebox.showerror("错误", "用户名或密码错误")
        else:
            current_username = username
            messagebox.showinfo("成功", "登录成功")
            # 关闭之前的窗口
            root.destroy()
            # 创建新的窗口
            show_modes_window()


def read_user_info():
    try:
        with open(user_info_file,"r") as file:
            user_info = json.load(file)
    except FileNotFoundError:
        user_info = {}
    return user_info

def save_user_info(user_info):
    with open(user_info_file,"w") as file:
        json.dump(user_info,file)

def read_profiles():
    try:
        with open(profile_file, "r") as file:
            profiles = json.load(file)
    except FileNotFoundError:
        profiles = []
    return profiles

def save_profiles(profiles):
    with open(profile_file, "w") as file:
        json.dump(profiles, file)

def open_profile_mode(username):
    global current_username

    # 读取用户档案信息
    profiles = read_profiles()

    # 查找当前用户的档案信息
    user_profile = None
    for profile in profiles:
        if profile["username"] == current_username:
            user_profile = profile
            break

    if user_profile:
        print(f"用户 {current_username} 的档案信息：{user_profile}")
    else:
        print(f"用户 {current_username} 没有档案信息")

################################################################################
def create_new_entry(entry_data):
    entries = {"model": entry_data["model"],
                    "name":  [],
                    "spec":  [],
                    "dos":   [],
                    "unit":  [],
                    "numbers": [],
                    "usage": []
                    }
    entries["name"].append(entry_data["name"])
    entries["spec"].append(entry_data["spec"])
    entries["dos"].append(entry_data["dos"])
    entries["unit"].append(entry_data["unit"])
    entries["numbers"].append(entry_data["numbers"])
    entries["usage"].append(entry_data["usage"])

    return entries
################################################################################


def save_entry_data(username, entry_data):
    # 读取用户档案信息
    profiles = read_profiles()

    # 查找当前用户的档案信息
    user_profile = None
    for profile in profiles:
        if profile["username"] == username:
            user_profile = profile
            break

    if user_profile:
        exist_model = False #用于判断是否存在相同的model
        # 将新的录入数据添加到用户的档案信息中
        for entry in user_profile["entries"]:
            #如果有相同的model则写入其中
            if entry["model"] == entry_data["model"]:
                entry["name"].append(entry_data["name"])
                entry["spec"].append(entry_data["spec"])
                entry["dos"].append(entry_data["dos"])
                entry["unit"].append(entry_data["unit"])
                entry["numbers"].append(entry_data["numbers"])
                entry["usage"].append(entry_data["usage"])
                exist_model = True
                break
        if exist_model == False:
            entry = create_new_entry(entry_data)
            user_profile["entries"].append(entry)
    else:
        # 如果当前用户没有档案信息，则创建一个新的档案信息
        entries = create_new_entry(entry_data)

        user_profile = {"username": username, "entries": [entries]}
        profiles.append(user_profile)

    # 保存更新后的用户档案信息
    save_profiles(profiles)
    print(f"用户 {username} 的录入数据已保存")

def show_modes_window():

    global mode_window

    global profile_window

    global entry_window

    # 关闭之前的窗口
    if profile_window:
        profile_window.destroy()

    if entry_window:
        entry_window.destroy()

    mode_window = tk.Tk()

    mode_window.title("模式选择")

    # 设置窗口大小
    mode_window.geometry("400x300")

    # 获取窗口大小
    window_width = mode_window.winfo_reqwidth()
    window_height = mode_window.winfo_reqheight()

    # 获取屏幕宽高
    screen_width = mode_window.winfo_screenwidth()
    screen_height = mode_window.winfo_screenheight()

    # 计算窗口居中的位置
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)

    # 设置窗口居中显示
    mode_window.geometry(f"+{x}+{y}")

    # 创建"录入模式"和"档案模式"按钮
    entry_mode_button = tk.Button(mode_window, text="录入模式", font=("Helvetica", 20),command=open_entry_mode)
    entry_mode_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    template_mode_button = tk.Button(mode_window, text="档案模式", font=("Helvetica", 20),command=open_profile_mode)
    template_mode_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    mode_window.mainloop()

# 档案模式按钮核心功能
def open_profile_mode():

    profiles = read_profiles()

    global mode_window

    mode_window.destroy()

    #  创建新窗口
    profile_window = tk.Tk()

    profile_window.geometry("600x600")

    profile_window.title("档案")

    # 创建滚动条
    scrollbar = tk.Scrollbar(profile_window)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    # 创建列表框
    listbox = tk.Listbox(profile_window, yscrollcommand=scrollbar.set, width=25, height=20)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    # 设置滚动条与文本框的关联
    scrollbar.config(command=listbox.yview)

    # 清空列表框内容
    listbox.delete(0, tk.END)

    # 在列表框中添加当前用户的所有 "model" 值
    for profile in profiles:
        if profile["username"] == current_username:
            for entry in profile["entries"]:
                listbox.insert(tk.END, entry["model"])

    # 创建Treeview表格
    tree = ttk.Treeview(profile_window, columns=("草药名称", "规格", "用量", "单位", "次数","用法"),show="headings")
    tree.heading("草药名称", text="草药名称")
    tree.heading("规格", text="规格")
    tree.heading("用量", text="用量")
    tree.heading("单位", text="单位")
    tree.heading("次数", text="次数")
    tree.heading("用法",text="用法")
    tree.column("草药名称", width=40)
    tree.column("规格", width=40)
    tree.column("用量", width=40)
    tree.column("单位", width=40)
    tree.column("次数", width=40)
    tree.column("用法",width=40)
    tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#############################################################################################################
    def delete_selected_content():
        treeview_selected_item = tree.focus() #获取Treeview选中项
        treeview_selected_index = 0 # 记录treeview中第几位
        listbox_selected_index = listbox.curselection() # 记录listbox中第几位
        children_item = tree.get_children() #获取treeview中所有的数据
        
        #查看第几位
        for i in range(len(children_item)):
            if children_item[i] == treeview_selected_item:
                treeview_selected_index = i
                break
        # 删除profiles中的数据
        if listbox_selected_index:
            model = listbox.get(listbox_selected_index)
# -------------->  如果没有选择treeview则删除listbox中选中的数据
            if treeview_selected_item == '':
                for profile in profiles:
                    if profile["username"] != current_username:
                        continue
                    for i in range(len(profile["entries"])):
                        if profile["entries"][i]["model"] != model:
                            continue
                        profile["entries"].pop(i)
                        save_profiles(profiles)
                        listbox.delete(listbox_selected_index)
                        update_table("f")
                        break
                    return
                 
            # 遍历档案,找到与选中的model值匹配的并删除
            for profile in profiles:
                if profile["username"] != current_username:
                    continue
                for entry in profile["entries"]:
                    if entry["model"] == model:
                        entry["name"].pop(treeview_selected_index)
                        entry["spec"].pop(treeview_selected_index)
                        entry["dos"].pop(treeview_selected_index)
                        entry["unit"].pop(treeview_selected_index)
                        entry["numbers"].pop(treeview_selected_index)
                        entry["usage"].pop(treeview_selected_index)
                        save_profiles(profiles)
                        # 删除treeview中的选中项
                        tree.delete(treeview_selected_item)
                        break
                break 

#############################################################################################################


    # 事件处理函数
    def update_table(event):
        # 清空 Treeview 表格
        tree.delete(*tree.get_children())

        # 获取选中项的索引
        selected_index = listbox.curselection()
        if selected_index:
            model = listbox.get(selected_index)  # 获取选中的 "model" 值
            tree.delete(*tree.get_children())  # 清空表格内容
            # 遍历档案，找到与选中的 "model" 值匹配的录入数据，并插入表格
            for profile in profiles:
                if profile["username"] != current_username:  # 确保仅查找当前用户的档案信息
                    continue
                for entry in profile["entries"]:
                    if entry["model"] != model:
                        continue
                    for i in range(len(entry['name'])):
                        temp = []
                        temp.append(entry['name'][i])
                        temp.append(entry['spec'][i])
                        temp.append(entry['dos'][i])
                        temp.append(entry['unit'][i])
                        temp.append(entry['numbers'][i])
                        temp.append(entry['usage'][i])
                        tree.insert("", tk.END, values=temp)  # 插入对应 model 的录入数据
                        
                    break
                break
                            # 仅插入除 "model" 之外的其他字段
                            #values = [entry[key] for key in entry if key != "model"]
                            #print("type:",type(values))
                            #print(values)
                            #tree.insert("", tk.END, values=values)  # 插入对应 model 的录入数据
    # 绑定事件处理函数
    listbox.bind("<<ListboxSelect>>", update_table)

    # 创建返回按钮
    return_button = tk.Button(profile_window, text="返回", command=lambda: back_to_modes_window(profile_window))
    return_button.pack()
    
    # 创建删除按钮
    delete_button = tk.Button(profile_window, text="删除", command=delete_selected_content)
    delete_button.pack()

    profile_window.mainloop()

def open_entry_mode():
    global mode_window

    global profiles

    profiles = read_profiles()
    # 关闭之前的窗口
    if mode_window:
        mode_window.destroy()
    # 创建新窗口
    entry_window = tk.Tk()
    entry_window.title("录入模式")
    entry_window.geometry("450x350")

    # 创建标签和输入框
    model_label = tk.Label(entry_window, text="模板：")
    model_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    model_entry = tk.Entry(entry_window)
    model_entry.grid(row=0, column=1, padx=10, pady=10)

    name_label = tk.Label(entry_window, text="草药名称：")
    name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    name_entry = tk.Entry(entry_window)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    spec_label = tk.Label(entry_window, text="规格：")
    spec_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    spec_entry = tk.Entry(entry_window)
    spec_entry.grid(row=2, column=1, padx=10, pady=10)

    dos_label = tk.Label(entry_window, text="用量：")
    dos_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    dos_entry = tk.Entry(entry_window)
    dos_entry.grid(row=3, column=1, padx=10, pady=10)

    unit_label = tk.Label(entry_window, text="单位：")
    unit_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    unit_entry = tk.Entry(entry_window)
    unit_entry.grid(row=4, column=1, padx=10, pady=10)

    numbers_label = tk.Label(entry_window, text="次数：")
    numbers_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
    numbers_entry = tk.Entry(entry_window)
    numbers_entry.grid(row=5, column=1, padx=10, pady=10)

    usage_label = tk.Label(entry_window, text="用法：")
    usage_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")
    usage_entry = tk.Entry(entry_window)
    usage_entry.grid(row=6, column=1, padx=10, pady=10)

    def submit_entry():
        # 获取用户输入的信息
        entry_data = {
        "model":model_entry.get(),
        "name": name_entry.get(),
        "spec": spec_entry.get(),
        "dos": dos_entry.get(),
        "unit" : unit_entry.get(),
        "numbers": numbers_entry.get(),
        "usage": usage_entry.get(),
        }

        # 将信息录入到档案中
        save_entry_data(current_username, entry_data)
        print("用户信息已经保存")

        # 清空输入框
        name_entry.delete(0, tk.END)
        spec_entry.delete(0, tk.END)
        dos_entry.delete(0, tk.END)
        unit_entry.delete(0, tk.END)
        numbers_entry.delete(0, tk.END)
        usage_entry.delete(0,tk.END)

    # 创建提交按钮
    submit_button = tk.Button(entry_window, text="提交", command=submit_entry)
    submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    # 创建返回按钮
    return_button = tk.Button(entry_window, text="返回", command=lambda: back_to_modes_window(entry_window))
    return_button.grid(row=7, column=3, columnspan=2)

    entry_window.mainloop()

# 返回到模式选择窗口
def back_to_modes_window(window_to_close):
    global mode_window
    # 关闭当前窗口
    window_to_close.destroy()
    # 重新显示模式选择窗口
    show_modes_window()


# 创建登录窗口
root = tk.Tk()
root.title("登录")

# 设置窗口大小
root.geometry("400x300")

# 获取窗口大小
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()

# 获取屏幕宽高
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口居中的位置
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)

# 设置窗口居中显示
root.geometry(f"+{x}+{y}")

# 创建用户名和密码输入框
username_label = tk.Label(root, text="用户名：", font=("Helvetica", 14))
username_label.place(relx=0.4, rely=0.4, anchor=tk.E)

username_entry = tk.Entry(root)
username_entry.place(relx=0.4, rely=0.4, anchor=tk.W)

password_label = tk.Label(root, text="密码：", font=("Helvetica", 14))
password_label.place(relx=0.35, rely=0.5, anchor=tk.E)

password_entry = tk.Entry(root, show="*")
password_entry.place(relx=0.4, rely=0.5, anchor=tk.W)

# 创建登录和注册按钮
login_button = tk.Button(root, text="登录", command=login, font=("Helvetica", 14))
login_button.place(relx=0.3, rely=0.65, anchor=tk.CENTER)

register_button = tk.Button(root, text="注册", command=register, font=("Helvetica", 14))
register_button.place(relx=0.7, rely=0.65, anchor=tk.CENTER)

# 设置网格的列权重，使得列可以随窗口大小变化而调整
root.columnconfigure(0, weight=1)

# 运行登录窗口的主循环
root.mainloop()
