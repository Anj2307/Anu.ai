"""Helpers for turning uploaded/captured images into multimodal message parts."""

import base64

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp")


def is_image(uploaded_file):
    """True if a Streamlit UploadedFile (or camera photo) is an image."""
    name = (getattr(uploaded_file, "name", "") or "").lower()
    mime = getattr(uploaded_file, "type", "") or ""
    return mime.startswith("image/") or name.endswith(IMAGE_EXTENSIONS)


def image_to_data_uri(uploaded_file):
    """Encode an image file as a base64 ``data:`` URI for the vision model."""
    data = uploaded_file.getvalue()
    mime = getattr(uploaded_file, "type", None) or "image/png"
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{encoded}"
