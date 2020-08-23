import os
import pathlib

EMAIL = "siarhei.ahafonau@gmail.com"
PASSWORD = "q_XEgUTnZnQ25aH"

LOGIN_FORM_LABEL = "Вход"
NICKNAME = "Sergey_7854r"
NUMBER_OF_USER_MENU_ITEMS = 7
LANGUAGE_SETTINGS_LABEL = ["Настройка языка", "Language settings"]
INTERFACE_LANGUAGES = ["Русский", "English"]
SETTINGS_PAGE_TITLE = "Настройки профиля"
UPLOAD_AVATAR_BUTTON = "Загрузить"

# URL to test
URL_TO_TEST = "https://account.habr.com/login/?state=f2a0daa40e03cc0234ebb30167e41bce&consumer=habr&hl=ru_RU"#https://habr.com/"

# _CURRENT_DIRECTORY = os.path.abspath(os.getcwd())
_CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

# Path to log
PATH_TO_LOGS = str(_CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "Logs" + os.sep
if not os.path.exists(PATH_TO_LOGS):
    os.makedirs(PATH_TO_LOGS)

# Path to screenshots of a browser
PATH_TO_SCREENSHOTS = str(_CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "Logs" + os.sep + "screenshots" + os.sep
if not os.path.exists(PATH_TO_SCREENSHOTS):
    os.makedirs(PATH_TO_SCREENSHOTS)
