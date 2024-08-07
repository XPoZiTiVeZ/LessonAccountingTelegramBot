from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from os import getenv

load_dotenv()
bot = Bot(token = getenv("BOT_TOKEN"))
dp = Dispatcher(storage = MemoryStorage())

mime_types = {
    "application/epub+zip": "epub",
    "application/gzip": "gz",
    "application/java-archive": "jar",
    "application/json": "json",
    "application/ld+json": "jsonld",
    "application/msword": "doc",
    "application/octet-stream": "bin",
    "application/ogg": "ogx",
    "application/pdf": "pdf",
    "application/rtf": "rtf",
    "application/vnd.amazon.ebook": "azw",
    "application/vnd.apple.installer+xml": "mpkg",
    "application/vnd.mozilla.xul+xml": "xul",
    "application/vnd.ms-excel": "xls",
    "application/vnd.ms-fontobject": "eot",
    "application/vnd.ms-powerpoint": "ppt",
    "application/vnd.oasis.opendocument.presentation": "odp",
    "application/vnd.oasis.opendocument.spreadsheet": "ods",
    "application/vnd.oasis.opendocument.text": "odt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.rar": "rar",
    "application/vnd.visio": "vsd",
    "application/x-7z-compressed": "7z",
    "application/x-abiword": "abw",
    "application/x-bzip": "bz",
    "application/x-bzip2": "bz2",
    "application/x-csh": "csh",
    "application/x-freearc": "arc",
    "application/x-httpd-php": "php",
    "application/x-sh": "sh",
    "application/x-tar": "tar",
    "application/xhtml+xml": "xhtml",
    "application/xml": "xml",
    "application/zip": "zip",
    "audio/aac": "aac",
    "audio/midi": "mid",
    "audio/mpeg": "mp3",
    "audio/ogg": "oga",
    "audio/opus": "opus",
    "audio/wav": "wav",
    "audio/webm": "weba",
    "audio/3gpp": "3gp",
    "audio/3gpp2": "3g2",
    "font/otf": "otf",
    "font/ttf": "ttf",
    "font/woff": "woff",
    "font/woff2": "woff2",
    "image/bmp": "bmp",
    "image/gif": "gif",
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/svg+xml": "svg",
    "image/tiff": "tiff",
    "image/webp": "webp",
    "text/css": "css",
    "text/csv": "csv",
    "text/html": "html",
    "text/javascript": "js",
    "text/plain": "txt",
    "text/xml": "xml",
    "video/mp2t": "ts",
    "video/mp4": "mp4",
    "video/mpeg": "mpeg",
    "video/ogg": "ogv",
    "video/webm": "webm",
    "video/x-msvideo": "avi"
}
