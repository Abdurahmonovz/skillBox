from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def kb_start():
    b = InlineKeyboardBuilder()
    b.button(text="🐍 Python Kursi", callback_data="course")
    return b.as_markup()

def kb_payment(code: str):
    b = InlineKeyboardBuilder()
    b.button(text="📸 Chek yuborish", callback_data=f"receipt:{code}")
    b.button(text="🔙 Orqaga", callback_data="back")
    b.adjust(1)
    return b.as_markup()

def kb_admin_payment(code: str):
    b = InlineKeyboardBuilder()
    b.button(text="✅ Tasdiqlash", callback_data=f"ok:{code}")
    b.button(text="❌ Rad etish", callback_data=f"no:{code}")
    b.adjust(2)
    return b.as_markup()

def kb_paid_menu():
    b = ReplyKeyboardBuilder()
    b.button(text="📚 Kurslar")
    return b.as_markup(resize_keyboard=True)

def kb_modules(modules):
    b = InlineKeyboardBuilder()
    for m in modules:
        b.button(text=f"📘 {m['title']}", callback_data=f"m:{m['id']}")
    b.button(text="🔙 Orqaga", callback_data="back")
    b.adjust(1)
    return b.as_markup()

def kb_lessons(lessons, module_id: int):
    b = InlineKeyboardBuilder()
    for l in lessons:
        b.button(text=f"🎬 {l['title']}", callback_data=f"l:{l['id']}")
    b.button(text="🔙 Modullar", callback_data="modules")
    b.adjust(1)
    return b.as_markup()

def kb_back_modules():
    b = InlineKeyboardBuilder()
    b.button(text="🔙 Modullar", callback_data="modules")
    return b.as_markup()

# Admin panel
def kb_admin_panel():
    b = InlineKeyboardBuilder()
    b.button(text="➕ Dars qo‘shish", callback_data="adm:add_lesson")
    b.button(text="✏️ Modul nomini o‘zgartirish", callback_data="adm:rename_module")
    b.button(text="📚 Modullarni ko‘rish", callback_data="adm:list_modules")
    b.adjust(1)
    return b.as_markup()

def kb_pick_module(modules, prefix: str):
    b = InlineKeyboardBuilder()
    for m in modules:
        b.button(text=f"📘 {m['title']}", callback_data=f"{prefix}:{m['id']}")
    b.adjust(1)
    return b.as_markup()
