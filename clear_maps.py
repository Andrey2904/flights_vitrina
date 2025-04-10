import os
import glob

MAPS_DIR = "maps"

def list_maps():
    if not os.path.exists(MAPS_DIR):
        print("❗ Папка 'maps' не найдена.")
        return []
    return sorted(glob.glob(os.path.join(MAPS_DIR, "*.html")))

def show_menu(files):
    print("\n📁 Доступные карты:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {os.path.basename(file)}")
    print("0. ❌ Удалить все карты")
    print("-1. 🚪 Выход без удаления")

def delete_files(files):
    for f in files:
        os.remove(f)
    print("✅ Удалено:", len(files))


maps = list_maps()

if not maps:
    print("ℹ️ В папке 'maps' нет карт.")
    exit()

while True:
    show_menu(maps)
    try:
        choice = int(input("\n🧹 Выбери номер карты для удаления (0 — все, -1 — выход): "))
        if choice == -1:
            print("👋 Выход.")
            break
        elif choice == 0:
            confirm = input("❗ Удалить ВСЕ карты? (y/n): ")
            if confirm.lower() == "y":
                delete_files(maps)
                break
        elif 1 <= choice <= len(maps):
            file_to_delete = maps[choice - 1]
            confirm = input(f"❗ Удалить {os.path.basename(file_to_delete)}? (y/n): ")
            if confirm.lower() == "y":
                os.remove(file_to_delete)
                print("✅ Удалена:", os.path.basename(file_to_delete))
                maps = list_maps()
                if not maps:
                    print("📂 Больше карт нет.")
                    break
        else:
            print("⚠️ Неверный выбор.")
    except ValueError:
        print("⚠️ Введи число.")
