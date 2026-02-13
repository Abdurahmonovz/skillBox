import aiosqlite
from typing import Optional, Dict, List

DEFAULT_MODULES = [
    "1. IDE o‘rnatish va sozlash",
    "2. Tayanch to‘plamlar: ro‘yxatlar",
    "3. Ro‘yxatlar bilan ishlash usullari",
    "4. List comprehensions",
    "5. Asosiy to‘plamlar: setlar",
    "6. Tayanch kolleksiyalar: lug‘atlar",
    "7. Bazaviy kolleksiyalar: kortejlar",
    "8. Funksiyalar: davomi",
    "9. Fayllar bilan ishlash",
    "10. Istisnolar: xatolar ustida ishlash",
]

class DB:
    def __init__(self, path: str):
        self.path = path

    async def init(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
              user_id INTEGER PRIMARY KEY,
              full_name TEXT,
              username TEXT,
              is_paid INTEGER DEFAULT 0
            )""")

            await db.execute("""
            CREATE TABLE IF NOT EXISTS payments(
              payment_code TEXT PRIMARY KEY,
              user_id INTEGER,
              status TEXT DEFAULT 'pending',
              created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )""")

            await db.execute("""
            CREATE TABLE IF NOT EXISTS modules(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              sort INTEGER DEFAULT 0
            )""")

            await db.execute("""
            CREATE TABLE IF NOT EXISTS lessons(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              module_id INTEGER NOT NULL,
              title TEXT NOT NULL,
              description TEXT DEFAULT '',
              video_file_id TEXT DEFAULT '',
              sort INTEGER DEFAULT 0,
              FOREIGN KEY(module_id) REFERENCES modules(id)
            )""")

            await db.execute("""
            CREATE TABLE IF NOT EXISTS lesson_pdfs(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              lesson_id INTEGER NOT NULL,
              pdf_file_id TEXT NOT NULL,
              sort INTEGER DEFAULT 0,
              FOREIGN KEY(lesson_id) REFERENCES lessons(id)
            )""")
            await db.commit()

    async def seed_modules_if_empty(self):
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT COUNT(*) FROM modules")
            (cnt,) = await cur.fetchone()
            if int(cnt) == 0:
                for i, title in enumerate(DEFAULT_MODULES, start=1):
                    await db.execute("INSERT INTO modules(title, sort) VALUES(?, ?)", (title, i))
                await db.commit()

    # users
    async def upsert_user(self, user_id: int, full_name: str, username: Optional[str]):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users(user_id, full_name, username) VALUES(?,?,?)",
                (user_id, full_name, username),
            )
            await db.commit()

    async def get_user(self, user_id: int) -> Optional[Dict]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
            row = await cur.fetchone()
            return dict(row) if row else None

    async def set_paid(self, user_id: int, paid: bool):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE users SET is_paid=? WHERE user_id=?", (1 if paid else 0, user_id))
            await db.commit()

    # payments
    async def create_payment(self, code: str, user_id: int):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO payments(payment_code, user_id, status) VALUES(?,?, 'pending')",
                (code, user_id),
            )
            await db.commit()

    async def get_payment(self, code: str) -> Optional[Dict]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM payments WHERE payment_code=?", (code,))
            row = await cur.fetchone()
            return dict(row) if row else None

    async def set_payment_status(self, code: str, status: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE payments SET status=? WHERE payment_code=?", (status, code))
            await db.commit()

    # modules / lessons / pdfs
    async def list_modules(self) -> List[Dict]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM modules ORDER BY sort, id")
            rows = await cur.fetchall()
            return [dict(r) for r in rows]

    async def update_module_title(self, module_id: int, title: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE modules SET title=? WHERE id=?", (title, module_id))
            await db.commit()

    async def add_lesson(self, module_id: int, title: str, desc: str) -> int:
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute(
                "INSERT INTO lessons(module_id, title, description) VALUES(?,?,?)",
                (module_id, title, desc),
            )
            await db.commit()
            return cur.lastrowid

    async def list_lessons(self, module_id: int) -> List[Dict]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM lessons WHERE module_id=? ORDER BY sort, id", (module_id,))
            rows = await cur.fetchall()
            return [dict(r) for r in rows]

    async def get_lesson(self, lesson_id: int) -> Optional[Dict]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM lessons WHERE id=?", (lesson_id,))
            row = await cur.fetchone()
            return dict(row) if row else None

    async def set_lesson_video(self, lesson_id: int, file_id: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE lessons SET video_file_id=? WHERE id=?", (file_id, lesson_id))
            await db.commit()

    async def add_pdf(self, lesson_id: int, file_id: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("INSERT INTO lesson_pdfs(lesson_id, pdf_file_id) VALUES(?,?)", (lesson_id, file_id))
            await db.commit()

    async def list_pdfs(self, lesson_id: int) -> List[str]:
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT pdf_file_id FROM lesson_pdfs WHERE lesson_id=? ORDER BY sort, id", (lesson_id,))
            rows = await cur.fetchall()
            return [r[0] for r in rows]
