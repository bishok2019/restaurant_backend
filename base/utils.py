import json

import filetype
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response


def decimal_positive_validator(value):
    if value < 0:
        raise ValidationError(f"Value must be Positive")


def validate_file(image):
    file_size = image.size
    limit_byte_size = settings.MAX_UPLOAD_SIZE
    if file_size > limit_byte_size:
        # converting into kb
        f = limit_byte_size / 1024
        # converting into MB
        f = f / 1024
        raise ValidationError("Max size of file is %s MB" % f)

    allowed_extensions = ["png", "jpg", "jpeg", "pdf", "svg"]
    extension = image.name.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            f"Unsupported file extension. Supported extensions are: {', '.join(allowed_extensions)}."
        )
    # print(extension)
    if extension in ["png", "jpg", "jpeg"]:
        valid_image_types = ["jpeg", "png"]
        file_types = filetype.guess(image)
        if file_types.extension not in valid_image_types:
            # if file_types is None or file_types.extension not in valid_image_types:

            # print(file_types)
            raise ValidationError(
                "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
            )


def validate_file_for_content_category(image):
    file_size = image.size
    limit_byte_size = settings.MAX_UPLOAD_SIZE
    if file_size > limit_byte_size:
        # converting into kb
        f = limit_byte_size / 1024
        # converting into MB
        f = f / 1024
        raise ValidationError("Max size of file is %s MB" % f)

    allowed_extensions = ["svg"]
    extension = image.name.split(".")[-1].lower()
    print(extension)

    if extension not in allowed_extensions:
        raise ValidationError(
            f"Unsupported file extension. Supported extensions are: {', '.join(allowed_extensions)}."
        )
    if extension in ["svg"]:
        try:
            # Reset file pointer to beginning
            image.seek(0)
            # Read the first few bytes to check if it's an SVG
            content = image.read(1024)  # Read first 1KB
            image.seek(0)  # Reset pointer for further processing
            if b"<svg" not in content:
                raise ValidationError(
                    "Upload a valid svg. The file you uploaded was either not an svg or a corrupted svg."
                )
        except Exception:
            raise ValidationError(
                "Upload a valid svg. The file you uploaded was either not an svg or a corrupted svg."
            )


def get_model_from_app(app_name, model_name):
    return apps.get_model(app_name, model_name)


def is_valid_json(json_data_function, *args):
    try:
        json.loads(json_data_function(*args))
        return True
    except Exception:
        pass
    return False


def clean_response(response, include_tokens=False):
    resp_data = (
        json.loads(response.content.decode("utf-8"))
        if response.content and is_valid_json(response.content.decode, "utf-8")
        else {}
    )
    if include_tokens:
        resp_data["access"] = ""
        resp_data["refresh"] = ""
    return resp_data


def log_request_response(
    request: WSGIRequest | ASGIRequest,
    response: Response,
    body: dict,
    catch_error=False,
    server_error_logging=False,
) -> None:
    allowed_methods = ["PATCH", "PUT", "POST", "DELETE"]
    allowed_endpoints = ["/api/"]

    if (
        request.method.casefold() in [method.casefold() for method in allowed_methods]
        and any(
            str(endpoint).casefold() in str(request.get_full_path()).casefold()
            for endpoint in allowed_endpoints
        )
        or catch_error
    ):
        try:
            body.pop("password", "password")
            body.pop("new_password", "new_password")
        except Exception as e:
            pass

        device_type = {
            "mobile": request.user_agent.is_mobile,
            "pc": request.user_agent.is_pc,
            "tablet": request.user_agent.is_tablet,
            "other": request.user_agent.is_tablet,
        }
        os_ = request.user_agent.os.family.lower()
        os_type_ = os_.split()[0]
        os_type = {
            "windows": os_type_ == "windows",
            "ios": os_type_ == "ios",
            "android": os_type_ == "android",
            "mac": os_type_ == "mac",
            "linux": os_type_ == "linux",
            "other": os_type_ == "other",
        }

        true_os = next((key for key, value in os_type.items() if value), "other")
        true_device = next(
            (key for key, value in device_type.items() if value), "other"
        )

        from apps.api_logs.models import APILog

        try:
            response.render()
        except Exception as e:
            pass
        include_tokens = "login" in str(request.get_full_path()).casefold()

        headers_data = dict(request.headers)
        try:
            headers_data.pop("Authorization", None)
            headers_data.pop("authorization", None)
        except Exception as e:
            pass

        server_error = json.loads(response.headers.get("server_error", "false").lower())
        params = {
            "url": str(request.get_full_path()),
            "method": request.method,
            "ip": request.META.get("REMOTE_ADDR"),
            "user_agent": request.headers.get("user-agent"),
            "body": body,
            "header": headers_data,
            "response": clean_response(response, include_tokens=include_tokens),
            "user_id": request.user.id if request.user else 0,
            "device_type": true_device,
            "os_type": true_os,
            "status_code": 500 if server_error else response.status_code,
            # "status_code": (
            #     500
            #     if server_error_logging and request.method.lower() == "get"
            #     else response.status_code
            # ),
            # "created_by": request.user.id if request.user else 0,
        }

        APILog.objects.create(**params)
        return


def validate_video_file(video):
    # file_size = video.size
    # limit_byte_size = settings.MAX_UPLOAD_SIZE
    # if file_size > limit_byte_size:
    #     # converting into kb
    #     f = limit_byte_size / 1024
    #     # converting into MB
    #     f = f / 1024
    #     raise ValidationError("Max size of file is %s MB" % f)

    allowed_extensions = ["mp4", "mkv"]
    extension = video.name.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            f"Unsupported file extension. Supported extensions are: {', '.join(allowed_extensions)}."
        )
