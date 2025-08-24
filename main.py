import os
import sys
import subprocess

def print_separator():
    """Выводит разделитель, подстроенный под ширину консоли."""
    try:
        width = os.get_terminal_size().columns
        print("-" * width)
    except OSError:
        # Резервный вариант, если не удалось получить размер
        print("-" * 80)

def show_help():
    """Выводит список всех доступных команд."""
    print_separator()
    print("Доступные команды:")
    print("  ls, list           - Вывести список файлов в текущей директории.")
    print("  cd <путь>          - Сменить текущую директорию на указанный путь.")
    print("  find <имя>         - Найти файлы, содержащие указанную подстроку.")
    print("  rm, del <имя>      - Удалить указанный файл.")
    print("  install <имя>      - Установить одну библиотеку.")
    print("  download <имя>     - Скачать библиотеку на флешку (требует интернет).")
    print("  batch_install [путь] - Установить все библиотеки из указанной папки.")
    print("                         Если путь не указан, использует текущую директорию.")
    print("  help               - Показать это сообщение.")
    print("  exit               - Выйти из программы.")
    print_separator()

def list_files():
    """Выводит список файлов и папок в текущей директории."""
    print_separator()
    print(f"Файлы и папки в текущей директории ({os.getcwd()}):")
    files = os.listdir('.')
    for file in files:
        print(file)
    print_separator()

def find_files(search_string):
    """Ищет файлы, содержащие указанную подстроку."""
    print_separator()
    if not search_string:
        print("Ошибка: Укажите строку для поиска.")
        return

    found_files = []
    try:
        files = os.listdir('.')
        for file in files:
            if search_string.lower() in file.lower():
                found_files.append(file)
    except OSError as e:
        print(f"Ошибка: Не удалось получить доступ к файлам. Причина: {e}")
        return

    if found_files:
        print(f"Найденные файлы, содержащие '{search_string}':")
        for file in found_files:
            print(file)
    else:
        print(f"Файлов, содержащих '{search_string}', не найдено.")
    print_separator()

def change_directory(path):
    """Меняет текущую рабочую директорию."""
    print_separator()
    if not path:
        print("Ошибка: Укажите путь для перехода.")
        return

    if not os.path.isdir(path):
        print(f"Ошибка: Путь '{path}' не существует или не является папкой.")
        return

    try:
        os.chdir(path)
        print(f"Текущая директория изменена на: {os.getcwd()}")
    except OSError as e:
        print(f"Ошибка: Не удалось сменить директорию. Причина: {e}")
    print_separator()

def delete_file(filename):
    """Удаляет файл, если он существует."""
    print_separator()
    if not os.path.exists(filename):
        print(f"Ошибка: Файл '{filename}' не найден.")
        return
    
    try:
        os.remove(filename)
        print(f"Файл '{filename}' удален.")
    except OSError as e:
        print(f"Ошибка: Не удалось удалить файл '{filename}'. Причина: {e}")
    print_separator()

def install_package(file_path):
    """Устанавливает один пакет с локального диска."""
    print_separator()
    command = [sys.executable, '-m', 'pip', 'install', '--no-index', '--find-links', '.', file_path]
    try:
        subprocess.run(command, check=True)
        print(f"Пакет '{file_path}' успешно установлен.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке: {e}")
    except FileNotFoundError:
        print("Ошибка: Команда pip не найдена. Убедитесь, что Python и pip установлены.")
    print_separator()

def download_library(lib_name):
    """Скачивает библиотеку и ее зависимости в текущую директорию."""
    print_separator()
    print(f"Скачивание '{lib_name}'...")
    command = [sys.executable, '-m', 'pip', 'download', lib_name, '-d', '.']
    try:
        subprocess.run(command, check=True)
        print(f"Библиотека '{lib_name}' успешно скачана.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при скачивании: {e}")
    except FileNotFoundError:
        print("Ошибка: Команда pip не найдена. Убедитесь, что Python и pip установлены.")
    print_separator()

def batch_install(folder_path=None):
    """Устанавливает все .whl файлы из указанной папки или текущей директории."""
    print_separator()
    if folder_path is None:
        folder_path = '.'
        print("Путь не указан. Установка будет произведена из текущей директории.")
    
    if not os.path.isdir(folder_path):
        print("Ошибка: Указанная папка не существует.")
        print_separator()
        return

    try:
        files_to_install = [f for f in os.listdir(folder_path) if f.endswith('.whl')]
    except OSError as e:
        print(f"Ошибка: Не удалось получить доступ к папке. Причина: {e}")
        print_separator()
        return

    if not files_to_install:
        print("В указанной папке нет файлов для установки (.whl).")
        print_separator()
        return

    print("Начинаю установку...")
    command = [sys.executable, '-m', 'pip', 'install', '--no-index', '--find-links', folder_path] + files_to_install
    try:
        subprocess.run(command, check=True)
        print("\nВсе библиотеки успешно установлены.")
    except subprocess.CalledProcessError as e:
        print(f"\nОшибка при массовой установке: {e}")
    print_separator()

def main():
    """Основной цикл программы, обрабатывающий команды пользователя."""
    print("Добро пожаловать в консольный менеджер библиотек!")
    print("Введите 'help' для получения списка команд.")

    while True:
        try:
            command = input(f"{os.getcwd()} >> ").strip().split(' ')
            cmd = command[0].lower()
            args = command[1:]

            if cmd in ['ls', 'list']:
                list_files()
            elif cmd == 'cd':
                if args:
                    change_directory(args[0])
                else:
                    print("Ошибка: Укажите путь для перехода.")
            elif cmd == 'find':
                if args:
                    find_files(args[0])
                else:
                    print("Ошибка: Укажите подстроку для поиска.")
            elif cmd in ['rm', 'del']:
                if args:
                    delete_file(args[0])
                else:
                    print("Ошибка: Укажите имя файла для удаления.")
            elif cmd == 'install':
                if args:
                    install_package(args[0])
                else:
                    print("Ошибка: Укажите имя файла для установки.")
            elif cmd == 'download':
                if args:
                    download_library(args[0])
                else:
                    print("Ошибка: Укажите имя библиотеки для скачивания.")
            elif cmd == 'batch_install':
                batch_install(args[0] if args else None)
            elif cmd == 'help':
                show_help()
            elif cmd == 'exit':
                print("До свидания!")
                break
            else:
                print(f"Неизвестная команда: '{cmd}'. Введите 'help' для списка команд.")
        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()