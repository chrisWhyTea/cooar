from enum import Enum


class MediaType(Enum):
    VIDEO = "video"
    SOUND = "sound"
    IMAGE = "image"
    ARCHIVE = "archive"


class AuthType(Enum):
    NO_AUTH = "no auth required"
    PASSWORD_ONLY = "password only"
    USERNAME_PASSWORD = "username and password"
    COOKIES = "cookies"
    TOKEN = "token"
