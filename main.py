# Программа TaskManager с использованием tkinker

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# Цветовые схемы

themes = {
    "light": {
        "bg": "#f4f4f9",
        "fg": "#333333",
        "highlight": "#ffffff",
        "accent": "#4CAF50",
        "button": "#e0e0e0",
        "text_bg": "#ffffff",
        "low_priority": "#d4edda",
        "medium_priority": "#fff3cd",
        "high_priority": "#f8d7da",
        "button_fg": "#333333",
        "header_bg": "#f4f4f9",  # Цвет фона для заголовков
        "header_fg": "#333333",  # Цвет текста для заголовков
    },
    "dark": {
        "bg": "#2c2c2c",
        "fg": "#000000",
        "highlight": "#3e3e3e",
        "accent": "#2196F3",
        "button": "#424242",
        "text_bg": "#d3d3d3",
        "low_priority": "#2e7d32",
        "medium_priority": "#f9a825",
        "high_priority": "#d32f2f",
        "button_fg": "#FFFFFF",
        "header_bg": "#2c2c2c",  # Цвет фона для заголовков
        "header_fg": "#ffffff",  # Цвет текста для заголовков
    },
}


# Применение цветовой темы

def apply_theme():
    global theme
    colors = themes[theme]

    # Настройка основного окна

    main_window.configure(bg=colors["bg"])

    # Настройка панелей

    for panel in [left_panel, center_panel, right_panel]:
        panel.configure(bg=colors["bg"])

    # Настройка стандартных виджетов

    for widget in main_window.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(bg=colors["button"], fg=colors["button_fg"])
        elif isinstance(widget, tk.Listbox):
            widget.configure(bg=colors["text_bg"], fg=colors["fg"])
        elif isinstance(widget, tk.Text):
            widget.configure(bg=colors["text_bg"], fg=colors["fg"], insertbackground=colors["fg"])
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=colors["text_bg"], fg=colors["fg"])

    # Настройка ttk-стилей

    style = ttk.Style()
    style.theme_use("clam")

    # Настройка стиля для ttk.Label

    style.configure(
        "TLabel",
        background=colors["header_bg"],
        foreground=colors["header_fg"],
        font=("Helvetica", 10)
    )

    # Настройка стиля для ttk.Button

    style.configure(
        "TButton",
        background=colors["button"],
        foreground=colors["button_fg"],
        font=("Helvetica", 10),
        borderwidth=0,
    )
    style.map(
        "TButton",
        background=[("active", colors["accent"]), ("pressed", colors["highlight"])],
    )

    # Настройка стиля для ttk.Combobox

    style.configure(
        "TCombobox",
        fieldbackground=colors["text_bg"],
        background=colors["highlight"],
        foreground=colors["fg"],
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", colors["text_bg"])],
        foreground=[("readonly", colors["fg"])],
    )

    # Настройка текста в полях

    task_name.configure(bg=colors["text_bg"], fg=colors["fg"])
    task_description.configure(bg=colors["text_bg"], fg=colors["fg"], insertbackground=colors["fg"])
    task_details.configure(bg=colors["text_bg"], fg=colors["fg"], insertbackground=colors["fg"])
    category_list.configure(bg=colors["text_bg"], fg=colors["fg"])
    task_list.configure(bg=colors["text_bg"], fg=colors["fg"])

    # Настройка


# Глобальные переменные

theme = "dark"
tasks = []
categories = {"Работа": [], "Учеба": [], "Личное": [], "Другое": []}  # Категории задач
current_category = "Всё"


# Функция для смены темы

def change_theme(selected_theme):
    global theme
    theme = selected_theme
    apply_theme()


# Функция для открытия файла

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            global tasks, categories
            tasks.clear()
            for category in categories:
                categories[category].clear()
            for row in reader:
                task = {
                    "name": row["name"],
                    "description": row["description"],
                    "priority": row["priority"],
                    "category": row["category"],
                }
                tasks.append(task)
                categories[task["category"]].append(task)
        refresh_task_list()
        refresh_categories()
        messagebox.showinfo("Успех", "Файл успешно загружен!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")


# Функция для сохранения файла

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
    )
    if not file_path:
        return
    try:
        with open(file_path, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=["name", "description", "priority", "category"]
            )
            writer.writeheader()
            for task in tasks:
                writer.writerow(task)
        messagebox.showinfo("Успех", "Файл успешно сохранен!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")


# Функции для работы с задачами

def add_task():
    name = task_name.get().strip()
    description = task_description.get("1.0", tk.END).strip()
    priority = task_priority.get()
    category = task_category.get()

    if not name or not priority or not category:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    task = {
        "name": name,
        "description": description,
        "priority": priority,
        "category": category,
    }
    tasks.append(task)
    categories[category].append(task)
    refresh_task_list()
    refresh_categories()
    clear_task_fields()


def delete_task():
    selected_index = task_list.curselection()
    if not selected_index:
        messagebox.showerror("Ошибка", "Выберите задачу для удаления!")
        return

    task = tasks.pop(selected_index[0])
    categories[task["category"]].remove(task)
    refresh_task_list()
    refresh_categories()


def refresh_categories():
    category_list.delete(0, tk.END)
    for category, task_list_in_category in categories.items():
        category_list.insert(tk.END, f"{category} ({len(task_list_in_category)})")
    # Добавляем категорию "Всё" в левое окно, чтобы отображались все задачи

    category_list.insert(tk.END, "Всё")


filtered_tasks = []  # Список задач для текущего фильтра


def refresh_task_list():
    global filtered_tasks
    task_list.delete(0, tk.END)  # Очистка списка задач

    # Определяем цвета для приоритетов

    priority_colors = {
        "Низкий": "lightgreen",
        "Средний": "khaki",
        "Высокий": "lightcoral",
    }

    filtered_tasks = tasks  # Показываем все задачи
    for i, task in enumerate(filtered_tasks, start=1):  # Нумерация задач
        task_text = f"{i}. {task['name']}"  # Полный текст строки
        task_list.insert(tk.END, task_text)  # Добавляем задачу в список

        # Определяем цвет для задачи на основе приоритета

        bg_color = priority_colors.get(task["priority"], "white")
        task_list.itemconfig(i - 1, {"bg": bg_color})  # Настраиваем цвет строки

    task_details.delete("1.0", tk.END)  # Очистка деталей задачи


def refresh_task_list_by_category(category):
    global filtered_tasks
    task_list.delete(0, tk.END)  # Очистка списка задач

    # Определяем цвета для приоритетов

    priority_colors = {
        "Низкий": "lightgreen",
        "Средний": "khaki",
        "Высокий": "lightcoral",
    }

    tasks_in_category = categories.get(category, [])  # Задачи в выбранной категории
    filtered_tasks = tasks_in_category  # Обновляем отфильтрованный список

    for i, task in enumerate(filtered_tasks, start=1):  # Нумерация задач
        task_text = f"{i}. {task['name']}"  # Полный текст строки
        task_list.insert(tk.END, task_text)  # Добавляем задачу в список

        # Определяем цвет для задачи на основе приоритета

        bg_color = priority_colors.get(task["priority"], "white")
        task_list.itemconfig(i - 1, {"bg": bg_color})  # Настраиваем цвет строки

    task_details.delete("1.0", tk.END)  # Очистка деталей задачи


def apply_text_color(index, priority, position):
    colors = {"Высокий": "red", "Средний": "orange", "Низкий": "green"}
    color = colors.get(priority, "black")
    task_list.itemconfig(index, {"fg": color})


def show_task_details(event):
    selected_index = task_list.curselection()
    if not selected_index:
        return

    task = filtered_tasks[selected_index[0]]  # Из отфильтрованного списка

    # Очистка деталей перед добавлением новой информации

    task_details.delete("1.0", tk.END)

    # Добавление строк с деталями задачи

    task_details.insert(tk.END, f"Название: {task['name']}\n")
    task_details.insert(tk.END, f"Описание: {task['description']}\n")

    # Добавляем строку "Приоритет" с соответствующим цветом

    task_details.insert(tk.END, "Приоритет: ", "bold")

    task_details.insert(
        tk.END, f"{task['priority']}\n", task["priority"]
    )  # Применяем тег по имени приоритета

    task_details.insert(tk.END, f"Категория: {task['category']}")

    # Настройка тегов для форматирования текста

    task_details.tag_config("bold", font=("Helvetica", 10, "bold"))
    task_details.tag_config("Высокий", foreground="red")
    task_details.tag_config("Средний", foreground="orange")
    task_details.tag_config("Низкий", foreground="green")


def category_selected(event):
    selected_index = category_list.curselection()
    if not selected_index:
        return  # Если ничего не выбрано, выходим из функции

    selected_category = category_list.get(selected_index[0]).split(" (")[
        0
    ]  # Убираем число задач из категории

    if selected_category == "Всё":
        refresh_task_list()  # Показываем все задачи
    else:
        refresh_task_list_by_category(
            selected_category
        )  # Показываем задачи только из выбранной категории


def clear_task_fields():
    task_name.delete(0, tk.END)
    task_description.delete("1.0", tk.END)
    task_priority.set("")
    task_category.set("")


# Глобальные переменные для сортировки

sort_direction = {
    "category": True,
    "priority": True,
}  # True - по возрастанию, False - по убыванию

# Функция сортировки


def sort_tasks(by):
    global sort_direction
    reverse = not sort_direction[by]  # Обратное направление сортировки
    sort_direction[by] = reverse

    if by == "category":
        tasks.sort(key=lambda x: x["category"], reverse=reverse)
    elif by == "priority":
        priority_order = {"Низкий": 1, "Средний": 2, "Высокий": 3}
        tasks.sort(key=lambda x: priority_order[x["priority"]], reverse=reverse)

    refresh_task_list()


# Создание основного окна

main_window = tk.Tk()
main_window.title('TaskManager "Malamute"')
main_window.geometry("1200x600")

# Панели

left_panel = tk.Frame(main_window, width=250)
left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

center_panel = tk.Frame(main_window)
center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

right_panel = tk.Frame(main_window, width=250)
right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Левый блок (категории)

ttk.Label(left_panel, text="Категории:", font=("Helvetica", 12, "bold")).pack(pady=10)
category_list = tk.Listbox(left_panel, height=15)
category_list.pack(fill=tk.BOTH, expand=True)
category_list.bind("<<ListboxSelect>>", category_selected)
refresh_categories()

# Центральный блок (список задач)

ttk.Label(center_panel, text="Список задач:", font=("Helvetica", 12, "bold")).grid(
    row=0, column=0, columnspan=2, pady=10, sticky="n"
)

task_list = tk.Listbox(center_panel, height=15)
task_list.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
task_list.bind("<<ListboxSelect>>", show_task_details)

# Название задачи и поле ввода

ttk.Label(center_panel, text="Название задачи:", anchor="w").grid(
    row=2, column=0, padx=(10, 5), pady=5, sticky="w"
)
task_name = tk.Entry(center_panel, width=50)
task_name.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="w")

# Описание задачи и поле ввода

ttk.Label(center_panel, text="Описание задачи:", anchor="w").grid(
    row=3, column=0, padx=(10, 5), pady=5, sticky="w"
)
task_description = tk.Text(center_panel, height=4, width=50)
task_description.grid(row=3, column=1, padx=(5, 10), pady=5, sticky="w")

# Приоритет

ttk.Label(center_panel, text="Приоритет:", anchor="w").grid(
    row=4, column=0, padx=(10, 5), pady=5, sticky="w"
)
task_priority = ttk.Combobox(
    center_panel, values=["Низкий", "Средний", "Высокий"], width=48
)
task_priority.grid(row=4, column=1, padx=(5, 10), pady=5, sticky="w")

# Категория

ttk.Label(center_panel, text="Категория:", anchor="w").grid(
    row=5, column=0, padx=(10, 5), pady=5, sticky="w"
)
task_category = ttk.Combobox(center_panel, values=list(categories.keys()), width=48)
task_category.grid(row=5, column=1, padx=(5, 10), pady=5, sticky="w")

# Настройка колонок

center_panel.grid_columnconfigure(0, weight=0)
center_panel.grid_columnconfigure(1, weight=0)

# Кнопки: "Добавить задачу" и "Удалить задачу"

ttk.Button(center_panel, text="Добавить задачу", command=add_task, width=25).grid(
    row=6, column=0, padx=5, pady=5, sticky="w"
)
ttk.Button(center_panel, text="Удалить задачу", command=delete_task, width=25).grid(
    row=6, column=1, padx=5, pady=5, sticky="w"
)

# Кнопки: "Сортировать по категории" и "Сортировать по приоритету"

ttk.Button(
    center_panel,
    text="Сортировать по категории",
    command=lambda: sort_tasks("category"),
    width=25,
).grid(row=7, column=0, padx=5, pady=5, sticky="w")
ttk.Button(
    center_panel,
    text="Сортировать по приоритету",
    command=lambda: sort_tasks("priority"),
    width=25,
).grid(row=7, column=1, padx=5, pady=5, sticky="w")


# Настройка правого блока (right_panel) с использованием grid

right_panel.grid_columnconfigure(0, weight=1)

# Заголовок "Детали задачи"

ttk.Label(right_panel, text="Детали задачи:", font=("Helvetica", 12, "bold")).grid(
    row=0, column=0, padx=10, pady=10, sticky="n"
)

# Поле для отображения деталей задачи

task_details = tk.Text(right_panel, height=15)
task_details.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

# Настройка строк для растягивания по вертикали

right_panel.grid_rowconfigure(1, weight=1)  # Растягиваем поле ввода


# Верхнее меню

menu_bar = tk.Menu(main_window)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=main_window.destroy)

settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Светлая тема", command=lambda: change_theme("light"))
settings_menu.add_command(label="Темная тема", command=lambda: change_theme("dark"))

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(
    label="О программе",
    command=lambda: messagebox.showinfo("О программе", "TaskManager 'Malamute' v1.1"),
)

menu_bar.add_cascade(label="Файл", menu=file_menu)
menu_bar.add_cascade(label="Настройки", menu=settings_menu)
menu_bar.add_cascade(label="Справка", menu=help_menu)
main_window.config(menu=menu_bar)

# Применение темы

apply_theme()

main_window.mainloop()
