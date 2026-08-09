from services.vision import image_to_data_uri, is_image


class FakeImage:
    def __init__(self, name, data, mime=None):
        self.name = name
        self._data = data
        self.type = mime

    def getvalue(self):
        return self._data


def test_is_image_by_extension():
    assert is_image(FakeImage("photo.PNG", b"x"))
    assert is_image(FakeImage("pic.jpg", b"x"))
    assert not is_image(FakeImage("notes.pdf", b"x"))


def test_is_image_by_mime():
    assert is_image(FakeImage("blob", b"x", mime="image/jpeg"))
    assert not is_image(FakeImage("blob", b"x", mime="application/pdf"))


def test_image_to_data_uri():
    uri = image_to_data_uri(FakeImage("p.png", b"hello", mime="image/png"))
    assert uri.startswith("data:image/png;base64,")
    assert uri.endswith("aGVsbG8=")  # base64("hello")
