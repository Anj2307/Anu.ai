from utils.frontend import generate_thread_id


def test_uuid():

    first = generate_thread_id()
    second = generate_thread_id()

    assert first != second
