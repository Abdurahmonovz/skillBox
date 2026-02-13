import asyncio, random
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import Config
from db import DB
from keyboards import (
    kb_start, kb_payment, kb_admin_payment,
    kb_paid_menu, kb_modules, kb_lessons, kb_back_modules,
    kb_admin_panel, kb_pick_module, kb_broadcast_target
)

class PayState(StatesGroup):
    waiting_receipt = State()

class AdminState(StatesGroup):
    pick_module_for_lesson = State()
    lesson_title = State()
    lesson_desc = State()
    lesson_video = State()
    lesson_pdfs = State()

class AdminRename(StatesGroup):
    pick_module = State()
    new_title = State()

# NEW: intro video set qilish
class AdminIntro(StatesGroup):
    waiting_intro_video = State()

# NEW: broadcast
class AdminBroadcast(StatesGroup):
    pick_target = State()
    waiting_message = State()

def gen_code(user_id: int) -> str:
    return f"PY-{str(user_id)[-4:]}-{random.randint(1000,9999)}"

async def main():
    cfg = Config()
    if not cfg.BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN yo'q (.env ni tekshir)!")
    if not cfg.ADMIN_ID:
        raise RuntimeError("ADMIN_ID yo'q (.env ni tekshir)!")

    bot = Bot(cfg.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    db = DB(cfg.DB_PATH)
    await db.init()
    await db.seed_modules_if_empty()

    # ---------------- USER ----------------
    @dp.message(F.text == "/start")
    async def start(m: Message):
        await db.upsert_user(m.from_user.id, m.from_user.full_name, m.from_user.username)
        user = await db.get_user(m.from_user.id)

        # NEW: ishonch/fayda matni
        trust_text = (
            "👋 Assalomu alaykum!\n\n"
            "✅ Kurslar tartibli, bosqichma-bosqich beriladi.\n"
            "✅ To‘lov tasdiqlansa kurs darhol ochiladi.\n"
            "✅ Videolar va PDF’lar bot ichida saqlanadi.\n"
            "✅ Savollaringiz bo‘lsa admin ko‘rib chiqadi.\n"
        )
        await m.answer(trust_text)

        # NEW: intro video (faqat 1-marta)
        intro_id = await db.get_setting("intro_video_file_id")
        if intro_id and user and int(user.get("seen_intro", 0)) == 0:
            try:
                await bot.send_video(
                    m.chat.id,
                    intro_id,
                    caption="🎬 Kursni qanday sotib olish va darslarni ochish bo‘yicha qo‘llanma",
                    protect_content=True,
                )
                await db.mark_intro_seen(m.from_user.id)
            except Exception:
                pass

        if user and user.get("is_paid"):
            await m.answer("✅ Kurs sizda ochiq. '📚 Kurslar' ni bosing.", reply_markup=kb_paid_menu())

        await m.answer("Assalomu alaykum! Kurs uchun tugmani bosing:", reply_markup=kb_start())

    @dp.callback_query(F.data == "back")
    async def back(cb: CallbackQuery):
        await cb.message.edit_text("Asosiy menyu:", reply_markup=kb_start())
        await cb.answer()

    @dp.callback_query(F.data == "course")
    async def course(cb: CallbackQuery):
        user = await db.get_user(cb.from_user.id)
        if user and user.get("is_paid"):
            await cb.message.edit_text("✅ Sizda kurs ochiq. '📚 Kurslar' bo‘limiga kiring.", reply_markup=kb_start())
            await cb.answer()
            return

        code = gen_code(cb.from_user.id)
        text = (
            "🐍 <b>Python Kursi</b>\n\n"
            f"💰 Narx: <b>{cfg.COURSE_PRICE_TEXT}</b>\n\n"
            "💳 <b>To'lov uchun karta:</b>\n"
            f"• <code>{cfg.CARD_NUMBER}</code>\n"
            f"• Egasi: {cfg.CARD_OWNER}\n\n"
            "🧾 <b>Izoh (comment) ga shu kodni yozing:</b>\n"
            f"• <code>{code}</code>\n\n"
            "Keyin chekni yuborasiz."
        )
        await cb.message.edit_text(text, reply_markup=kb_payment(code))
        await cb.answer()

    @dp.callback_query(F.data.startswith("receipt:"))
    async def receipt_start(cb: CallbackQuery, state: FSMContext):
        code = cb.data.split(":", 1)[1]
        await state.set_state(PayState.waiting_receipt)
        await state.update_data(code=code)
        await cb.message.edit_text(
            "📸 Chekni rasm yoki PDF qilib yuboring.\n"
            f"To'lov kodi: <code>{code}</code>"
        )
        await cb.answer()

    @dp.message(PayState.waiting_receipt, F.photo | F.document)
    async def receipt_get(m: Message, state: FSMContext):
        data = await state.get_data()
        code = data.get("code")
        if not code:
            await m.answer("❌ Xatolik. /start dan qayta urinib ko'ring.")
            await state.clear()
            return

        await db.create_payment(code, m.from_user.id)

        caption = (
            "🆕 <b>Yangi to'lov</b>\n\n"
            f"👤 {m.from_user.full_name}\n"
            f"🆔 <code>{m.from_user.id}</code>\n"
            f"💳 Kod: <code>{code}</code>\n\n"
            "Tasdiqlaysizmi?"
        )

        if m.photo:
            fid = m.photo[-1].file_id
            await bot.send_photo(cfg.ADMIN_ID, fid, caption=caption, reply_markup=kb_admin_payment(code))
        else:
            fid = m.document.file_id
            await bot.send_document(cfg.ADMIN_ID, fid, caption=caption, reply_markup=kb_admin_payment(code))

        await m.answer("✅ Chek adminga yuborildi. Tasdiqlansa kurs ochiladi.", reply_markup=kb_start())
        await state.clear()

    @dp.callback_query(F.data.startswith("ok:") | F.data.startswith("no:"))
    async def admin_payment(cb: CallbackQuery):
        if cb.from_user.id != cfg.ADMIN_ID:
            await cb.answer("❌ Admin emas!", show_alert=True)
            return

        action, code = cb.data.split(":", 1)
        pay = await db.get_payment(code)
        if not pay:
            await cb.answer("❌ To'lov topilmadi!", show_alert=True)
            return
        user_id = int(pay["user_id"])

        if action == "ok":
            await db.set_payment_status(code, "approved")
            await db.set_paid(user_id, True)
            await bot.send_message(
                user_id,
                "✅ <b>To'lov tasdiqlandi!</b>\n\nEndi '📚 Kurslar' bo‘limi ochiq.",
                reply_markup=kb_paid_menu()
            )
            await cb.answer("✅ Kurs ochildi")
        else:
            await db.set_payment_status(code, "rejected")
            await bot.send_message(user_id, "❌ <b>To'lov rad etildi.</b>\n\nIltimos, qayta yuboring.")
            await cb.answer("❌ Rad etildi")

        try:
            await cb.message.edit_caption((cb.message.caption or "") + ("\n\n✅ Tasdiqlandi" if action=="ok" else "\n\n❌ Rad etildi"))
        except Exception:
            pass

    @dp.message(F.text == "📚 Kurslar")
    async def user_modules(m: Message):
        user = await db.get_user(m.from_user.id)
        if not user or not user.get("is_paid"):
            await m.answer("❌ Avval kursni sotib oling!", reply_markup=kb_start())
            return
        modules = await db.list_modules()
        await m.answer("📚 <b>Modullar</b>\nModulni tanlang:", reply_markup=kb_modules(modules))

    @dp.callback_query(F.data == "modules")
    async def user_modules_cb(cb: CallbackQuery):
        user = await db.get_user(cb.from_user.id)
        if not user or not user.get("is_paid"):
            await cb.answer("❌ Avval kursni sotib oling!", show_alert=True)
            return
        modules = await db.list_modules()
        await cb.message.edit_text("📚 <b>Modullar</b>\nModulni tanlang:", reply_markup=kb_modules(modules))
        await cb.answer()

    @dp.callback_query(F.data.startswith("m:"))
    async def open_module(cb: CallbackQuery):
        user = await db.get_user(cb.from_user.id)
        if not user or not user.get("is_paid"):
            await cb.answer("❌ Avval kursni sotib oling!", show_alert=True)
            return
        module_id = int(cb.data.split(":", 1)[1])
        lessons = await db.list_lessons(module_id)
        if not lessons:
            await cb.answer("Bu modulda hali dars yo‘q", show_alert=True)
            return
        await cb.message.edit_text("🎬 <b>Darslar</b>\nTanlang:", reply_markup=kb_lessons(lessons, module_id))
        await cb.answer()

    @dp.callback_query(F.data.startswith("l:"))
    async def open_lesson(cb: CallbackQuery):
        user = await db.get_user(cb.from_user.id)
        if not user or not user.get("is_paid"):
            await cb.answer("❌ Avval kursni sotib oling!", show_alert=True)
            return

        parts = cb.data.split(":")
        lesson_id = int(parts[-1])

        lesson = await db.get_lesson(lesson_id)
        if not lesson:
            await cb.answer("Dars topilmadi", show_alert=True)
            return

        await cb.answer()
        try:
            await cb.message.delete()
        except Exception:
            pass

        if not lesson.get("video_file_id"):
            await bot.send_message(cb.from_user.id, "⚠️ Bu darsga video qo‘yilmagan.", reply_markup=kb_back_modules())
            return

        await bot.send_video(
            cb.from_user.id,
            lesson["video_file_id"],
            caption=f"🎬 <b>{lesson['title']}</b>\n\n{lesson['description']}",
            protect_content=True,
            reply_markup=kb_back_modules()
        )

        pdfs = await db.list_pdfs(lesson_id)
        for pdf_id in pdfs:
            await bot.send_document(cb.from_user.id, pdf_id, protect_content=True)

    # ---------------- ADMIN ----------------
    @dp.message(F.text == "/admin")
    async def admin_panel(m: Message):
        if m.from_user.id != cfg.ADMIN_ID:
            return await m.answer("❌ Admin emas!")
        await m.answer("👨‍💻 Admin panel:", reply_markup=kb_admin_panel())

    @dp.callback_query(F.data == "adm:list_modules")
    async def adm_list(cb: CallbackQuery):
        if cb.from_user.id != cfg.ADMIN_ID:
            return await cb.answer("Admin emas", show_alert=True)
        modules = await db.list_modules()
        txt = "📚 <b>Modullar:</b>\n\n" + "\n".join([f"{m['id']}) {m['title']}" for m in modules])
        await cb.message.answer(txt)
        await cb.answer()

    # NEW: Intro video sozlash
    @dp.callback_query(F.data == "adm:set_intro")
    async def adm_set_intro(cb: CallbackQuery, state: FSMContext):
        if cb.from_user.id != cfg.ADMIN_ID:
            return await cb.answer("Admin emas", show_alert=True)
        await state.set_state(AdminIntro.waiting_intro_video)
        await cb.message.answer("🎬 Intro video yuboring (oddiy video fayl).")
        await cb.answer()

    @dp.message(AdminIntro.waiting_intro_video, F.video)
    async def adm_save_intro(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return
        await db.set_setting("intro_video_file_id", m.video.file_id)
        await state.clear()
        await m.answer("✅ Intro video saqlandi. Endi yangi user /start qilsa avtomatik ko‘radi.", reply_markup=kb_admin_panel())

    # NEW: Broadcast boshlash
    @dp.callback_query(F.data == "adm:broadcast")
    async def adm_broadcast_start(cb: CallbackQuery, state: FSMContext):
        if cb.from_user.id != cfg.ADMIN_ID:
            return await cb.answer("Admin emas", show_alert=True)
        await state.set_state(AdminBroadcast.pick_target)
        await cb.message.answer("📢 Reklamani kimlarga yuboramiz?", reply_markup=kb_broadcast_target())
        await cb.answer()

    @dp.callback_query(AdminBroadcast.pick_target, F.data.startswith("adm:bc:"))
    async def adm_broadcast_pick(cb: CallbackQuery, state: FSMContext):
        if cb.from_user.id != cfg.ADMIN_ID:
            return await cb.answer("Admin emas", show_alert=True)
        target = cb.data.split(":")[-1]  # all yoki paid
        await state.update_data(target=target)
        await state.set_state(AdminBroadcast.waiting_message)
        await cb.message.answer("Endi reklama xabarini yuboring (matn/rasm/video/fayl).\nBekor qilish: /cancel")
        await cb.answer()

    @dp.message(AdminBroadcast.waiting_message)
    async def adm_broadcast_send(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return

        data = await state.get_data()
        target = data.get("target", "all")
        user_ids = await db.list_users(paid_only=(target == "paid"))

        ok = 0
        fail = 0

        for uid in user_ids:
            try:
                await bot.copy_message(chat_id=uid, from_chat_id=m.chat.id, message_id=m.message_id)
                ok += 1
                await asyncio.sleep(0.05)
            except Exception:
                fail += 1

        await state.clear()
        await m.answer(f"✅ Reklama yuborildi!\nYuborildi: {ok}\nXatolik: {fail}", reply_markup=kb_admin_panel())

    @dp.message(F.text == "/cancel")
    async def cancel_any(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return
        await state.clear()
        await m.answer("❎ Bekor qilindi.", reply_markup=kb_admin_panel())

    # Modul nomini o‘zgartirish
    @dp.callback_query(F.data == "adm:rename_module")
    async def adm_rename_start(cb: CallbackQuery, state: FSMContext):
        if cb.from_user.id != cfg.ADMIN_ID:
            return await cb.answer("Admin emas", show_alert=True)
        modules = await db.list_modules()
        await state.set_state(AdminRename.pick_module)
        await cb.message.answer("Qaysi modul nomini o‘zgartiramiz?", reply_markup=kb_pick_module(modules, "adm:rename_pick"))
        await cb.answer()

    @dp.callback_query(AdminRename.pick_module, F.data.startswith("adm:rename_pick:"))
    async def adm_rename_pick(cb: CallbackQuery, state: FSMContext):
        module_id = int(cb.data.split(":")[-1])
        await state.update_data(module_id=module_id)
        await state.set_state(AdminRename.new_title)
        await cb.message.answer("Yangi modul nomini yozing:")
        await cb.answer()

    @dp.message(AdminRename.new_title)
    async def adm_rename_save(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return
        data = await state.get_data()
        module_id = data["module_id"]
        await db.update_module_title(module_id, m.text.strip())
        await state.clear()
        await m.answer("✅ Modul nomi yangilandi.", reply_markup=kb_admin_panel())

    # Dars qo‘shish
    @dp.callback_query(F.data == "adm:add_lesson")
    async def adm_add_lesson(cb: CallbackQuery, state: FSMContext):
        if cb.from_user.id != cfg.ADMIN_ID:
            return await cb.answer("Admin emas", show_alert=True)
        modules = await db.list_modules()
        await state.set_state(AdminState.pick_module_for_lesson)
        await cb.message.answer("Qaysi modulga dars qo‘shamiz?", reply_markup=kb_pick_module(modules, "adm:pick_module"))
        await cb.answer()

    @dp.callback_query(AdminState.pick_module_for_lesson, F.data.startswith("adm:pick_module:"))
    async def adm_pick_module(cb: CallbackQuery, state: FSMContext):
        module_id = int(cb.data.split(":")[-1])
        await state.update_data(module_id=module_id)
        await state.set_state(AdminState.lesson_title)
        await cb.message.answer("Dars nomini yozing:")
        await cb.answer()

    @dp.message(AdminState.lesson_title)
    async def adm_lesson_title(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return
        await state.update_data(lesson_title=m.text.strip())
        await state.set_state(AdminState.lesson_desc)
        await m.answer("Dars tavsifini yozing (qisqa):")

    @dp.message(AdminState.lesson_desc)
    async def adm_lesson_desc(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return
        data = await state.get_data()
        module_id = data["module_id"]
        title = data["lesson_title"]
        desc = m.text.strip()
        lesson_id = await db.add_lesson(module_id, title, desc)
        await state.update_data(lesson_id=lesson_id)
        await state.set_state(AdminState.lesson_video)
        await m.answer("Endi shu darsning VIDEOSINI yuboring (video fayl):")

    @dp.message(AdminState.lesson_video, F.video)
    async def adm_lesson_video(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return
        data = await state.get_data()
        lesson_id = data["lesson_id"]
        await db.set_lesson_video(lesson_id, m.video.file_id)
        await state.set_state(AdminState.lesson_pdfs)
        await m.answer("✅ Video saqlandi.\nEndi PDF(lar) yuboring (xohlagancha).\nTugatish uchun /done yozing.")

    @dp.message(AdminState.lesson_pdfs, F.document)
    async def adm_add_pdf(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return
        data = await state.get_data()
        lesson_id = data["lesson_id"]
        await db.add_pdf(lesson_id, m.document.file_id)
        await m.answer("✅ PDF qo‘shildi. Yana yuborishingiz mumkin yoki /done.")

    @dp.message(AdminState.lesson_pdfs, F.text == "/done")
    async def adm_done(m: Message, state: FSMContext):
        if m.from_user.id != cfg.ADMIN_ID:
            return
        await state.clear()
        await m.answer("✅ Dars to‘liq saqlandi!", reply_markup=kb_admin_panel())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
