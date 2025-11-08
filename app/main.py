from app import timer
import threading
from app.db import engine
from app.models import Base

# создаём таблицы, если их ещё нет
Base.metadata.create_all(bind=engine)



if __name__ == "__main__":
    dur = timer.ask_duration()
    thread = threading.Thread(target=timer.run, args=(dur,))
    thread.daemon = True  # таймер существует в виде отдельного потока, поэтому его нужно сделать демоном (дочерний поток, который вырубается, если основной поток завершен)
    print("Таймер запущен!")
    thread.start()

    while True:

        print("Доступные команды - status, pause, resume, stop")
        command = input(">>>").strip().lower()

        if command == "pause":
            if timer.state["pause_event"].is_set():
                print("Таймер уже на паузе!")
                continue
            timer.pause()

        elif command == "resume":
            if not timer.state["pause_event"].is_set():
                print("Таймер уже идет!")
                continue
            timer.resume()

        elif command == "stop":
            timer.stop()
            print("\n ---ОТМЕНЕНО ПОЛЬЗОВАТЕЛЕМ---")
            break

        elif command == "status":
            timer.status()

        else:
            print("Введена несуществующая команда")