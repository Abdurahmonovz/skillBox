import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0") or 0)

    CARD_NUMBER: str = os.getenv("CARD_NUMBER", "8600 0000 0000 0000").strip()
    CARD_OWNER: str = os.getenv("CARD_OWNER", "KURS TO'LOVI").strip()
    COURSE_PRICE_TEXT: str = os.getenv("COURSE_PRICE_TEXT", "60 000 so'm").strip()

    DB_PATH: str = os.getenv("DB_PATH", "bot_database.db").strip()
