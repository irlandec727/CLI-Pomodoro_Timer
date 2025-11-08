# tests/test_timer.py
from datetime import datetime, timedelta
from app import timer


def reset_state():
    """Хелпер, чтобы перед каждым тестом очищать состояние таймера."""
    timer.state["pause_event"].clear()
    timer.state["stop_event"].clear()
    timer.state["start_ts"] = None
    timer.state["paused_at"] = None
    timer.state["accumulated_pause"] = 0
    timer.state["deadline"] = datetime.now()
    timer.state["remaining"] = timedelta(seconds=0)


def test_pause_sets_pause_event_and_paused_at():
    reset_state()

    timer.pause()

    assert timer.state["pause_event"].is_set()
    assert isinstance(timer.state["paused_at"], datetime)


def test_resume_clears_pause_event_and_increases_accumulated_pause(mocker):
    reset_state()

    # зафейкуем время, чтобы тест проходил быстро
    fake_now_1 = datetime(2024, 1, 1, 12, 0, 0)
    fake_now_2 = datetime(2024, 1, 1, 12, 0, 5)

    mocker.patch("app.timer.datetime")
    timer.datetime.now.return_value = fake_now_1

    timer.pause()
    timer.state["deadline"] = fake_now_1 + timedelta(minutes=25)

    timer.datetime.now.return_value = fake_now_2
    timer.resume()

    # накопленная пауза 5 секунд
    assert timer.state["accumulated_pause"] == 5
    assert not timer.state["pause_event"].is_set()
    assert timer.state["paused_at"] is None


def test_stop_sets_stop_event():
    reset_state()

    timer.stop()

    assert timer.state["stop_event"].is_set()


def test_ask_duration_valid(monkeypatch):
    reset_state()

    monkeypatch.setattr("builtins.input", lambda _: "25")
    assert timer.ask_duration() == 25.0


def test_ask_duration_invalid_then_valid(monkeypatch, capsys):
    reset_state()

    answers = iter(["abc", "15"])

    def fake_input(_):
        return next(answers)

    monkeypatch.setattr("builtins.input", fake_input)

    result = timer.ask_duration()
    captured = capsys.readouterr().out

    assert "Нужно ввести число!" in captured
    assert result == 15.0


def test_status_prints_correct_format(capsys):
    reset_state()

    timer.state["remaining"] = timedelta(minutes=1, seconds=30)
    timer.status()

    out = capsys.readouterr().out.strip()
    assert "Осталось:" in out
    assert "1 минут" in out
    assert "30 секунд" in out
