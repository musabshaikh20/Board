from django.conf import settings
import os
BASE_DIR = settings.BASE_DIR

LOG_FILE = os.path.join(BASE_DIR,"logs/error.log")
PREMIUM = 'premium'
MAX_BOARD_COUNT = 10