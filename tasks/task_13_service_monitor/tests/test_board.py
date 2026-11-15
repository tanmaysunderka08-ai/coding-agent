from board import status_board

LOG = "\n".join(
    f"{m}, api, {'ok' if m != 6 else 'fail'}, {100 + m}" for m in range(1, 8)
) + "\n" + "\n".join(
    f"{m}, db, {'fail' if m >= 6 else 'ok'}, {20 + m}" for m in range(1, 8)
)


def test_uptime_over_last_five_checks():
    board = status_board(LOG)
    assert board["api"]["uptime"] == 80.0
    assert board["db"]["uptime"] == 60.0


def test_current_status():
    board = status_board(LOG)
    assert board["api"]["status"] == "up" and board["api"]["since_minute"] == 7
    assert board["db"]["status"] == "down" and board["db"]["since_minute"] == 7


def test_recent_latency_newest_first():
    board = status_board(LOG)
    assert board["api"]["recent_latency"] == [107, 106, 105]
    assert board["db"]["recent_latency"] == [27, 26, 25]


def test_longer_history():
    board = status_board(LOG, keep=10)
    assert board["db"]["recent_latency"] == [27, 26, 25]
    assert board["db"]["uptime"] == round(100 * 5 / 7, 1)
