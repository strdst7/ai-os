from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.config import MonitoringConfig

APP = Path(__file__).resolve().parents[1] / "app.py"


def make_app():
    return AppTest.from_file(str(APP), default_timeout=30).run()


def test_rerun_without_new_telemetry_does_not_append_history():
    dashboard = make_app()
    assert not dashboard.exception
    assert len(dashboard.session_state.history) == 1

    dashboard.run()
    dashboard.run()
    assert not dashboard.exception
    assert len(dashboard.session_state.history) == 1


def test_changing_a_slider_appends_exactly_one_point():
    dashboard = make_app()
    before = len(dashboard.session_state.history)

    dashboard.sidebar.slider[0].set_value(0.42)
    dashboard.run()
    assert not dashboard.exception
    assert len(dashboard.session_state.history) == before + 1

    dashboard.run()
    assert len(dashboard.session_state.history) == before + 1


def test_simulate_degradation_updates_the_sliders():
    dashboard = make_app()
    defaults = [slider.value for slider in dashboard.sidebar.slider]
    before = len(dashboard.session_state.history)

    dashboard.button[0].click().run()
    assert not dashboard.exception

    values = [slider.value for slider in dashboard.sidebar.slider]
    assert values != defaults
    assert len(dashboard.session_state.history) == before + 1
    assert dashboard.metric[0].value == str(round(dashboard.session_state.history[-1], 3))


def test_history_is_bounded_by_the_configured_limit():
    dashboard = make_app()
    for index in range(MonitoringConfig.HISTORY_LIMIT + 5):
        dashboard.sidebar.slider[0].set_value(index / 100)
        dashboard.run()
    assert not dashboard.exception
    assert len(dashboard.session_state.history) == MonitoringConfig.HISTORY_LIMIT
