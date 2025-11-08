from app.db import SessionLocal
from app.models import PomodoroSession

import threading
from threading import Timer
import time as t
from datetime import datetime, timedelta


# словарь состояний таймера
state = {"pause_event": threading.Event(),
         "stop_event": threading.Event(),
         "start_ts": None,
         "paused_at": None,
         "accumulated_pause": 0,
         "deadline": datetime.now(),
         "remaining": 0}


def save_session(duration_minutes: float, completed: bool, state=state) -> None:
    """
    Сохраняет информацию о сессии в БД.
    duration_minutes — запрошенная длительность сессии в минутах.
    completed — True, если дошли до конца, False, если остановился/оборвался.
    """
    db = SessionLocal()
    try:
        session_row = PomodoroSession(
            started_at=state["start_ts"],
            duration_minutes=int(duration_minutes),
            completed=completed,
            accumulated_pause_seconds=int(state["accumulated_pause"]),
        )
        db.add(session_row)
        db.commit()
    finally:
        db.close()



# пауза
def pause(state=state):
    state["pause_event"].set()
    state["paused_at"] = datetime.now()


# возобновление
def resume(state=state):
    state["accumulated_pause"] += (datetime.now() - state["paused_at"]).total_seconds()
    state["deadline"] += (datetime.now() - state["paused_at"])
    state["paused_at"] = None
    state["pause_event"].clear()


# стоп)
def stop(state=state):
    state["stop_event"].set()


def status(state=state):
    rem = int(state["remaining"].total_seconds())
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"Осталось: {minutes} минут, {seconds} секунд")





# выполняется по окончанию таймера
def on_finish() -> None:
    print("\nСессия окончена!")


# отсчитывает и выводит оставшееся время
def countdown(duration: float) -> None:

    state["start_ts"] = datetime.now()
    state["deadline"] = state["start_ts"] + timedelta(minutes=duration)
    state["remaining"] = state["deadline"] - state["start_ts"]

    while not state["stop_event"].is_set() and state["remaining"].total_seconds() >= 0:
        if state["pause_event"].is_set():
            t.sleep(1.0)
            continue
        t.sleep(0.3)
        state["remaining"] = state["deadline"] - datetime.now()


# сам раннер таймера, собственно говоря
def run(duration) -> None:
    timer = Timer(duration*60, on_finish)
    timer.daemon = True  # таймер существует в виде отдельного потока, поэтому его нужно сделать демоном (дочерний поток, который вырубается, если основной поток завершен)
    timer.start()
    try:
        countdown(duration)
        # если дошли сюда без KeyboardInterrupt —
        # либо таймер нормально закончился, либо мы нажали stop()
        completed = not state["stop_event"].is_set()
        save_session(duration_minutes=duration, completed=completed)
    except KeyboardInterrupt:
        # Ctrl+C — тоже считаем отменой
        timer.cancel()
        save_session(duration_minutes=duration, completed=False)
        print("\n ---ОТМЕНЕНО ПОЛЬЗОВАТЕЛЕМ---")



# запрашивает у пользователя кол-во минут
def ask_duration() -> float:
    while True:
        duration = input("Сколько будет длиться ваша сессия? Введите кол-во минут - ").strip()
        try:
            return float(duration)
        except ValueError:
            print("Нужно ввести число!")