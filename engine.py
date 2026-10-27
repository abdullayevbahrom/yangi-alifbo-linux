#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Yangi Alifbo — Linux IBus Kirish Dvigateli
224.uz/alifbo loyihasi (https://224.uz/alifbo/#klaviatura) asosida
Mualliflar: Bahrom Abdullayev (https://github.com/abdullayevbahrom) & His perspective (https://t.me/hisperspective)

Avtomatik almashtirishlar:
  sh -> ş,  Sh -> Ş,  SH -> Ş,  sH -> ş
  ch -> ç,  Ch -> Ç,  CH -> Ç,  cH -> ç
  o' / o` / o‘ / o’ / oʻ / oʼ -> ö  (O' -> Ö)
  g' / g` / g‘ / g’ / gʻ / gʼ -> ğ  (G' -> Ğ)

Universal imkoniyatlar:
  - Uzbek Latin (uz) klaviatura tartibida 100% avtomatik ishlaydi
  - US (English) tartibida odatiy yozuv, kerak bo'lsa Ctrl+Alt+Y orqali yoqiladi
  - Numpad (raqamlar bloki va nuqta) qulf ekrani (lockscreen) va barcha oynalarda to'siqsiz ishlaydi
  - Sichqoncha harakatlari (click, selection, middle-paste) da bufer darhol sinxronlanadi
  - Wayland (COSMIC, GNOME, KDE) va eski X11 tizimlarida universal ishlaydi
  - Preedit desinxronizatsiyasi yo'q (harflar 2 marta takrorlanmaydi)
"""

import os
import sys
import gi

gi.require_version('IBus', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import IBus, GLib

APOSTROPHES = {"'", "`", "‘", "’", "ʻ", "ʼ", chr(0x02BB), chr(0x02BC)}
PREFIX_KEYS = {'s', 'S', 'c', 'C', 'o', 'O', 'g', 'G'}
TIMEOUT_DELAY_MS = 1000  # 1 soniya (1000 ms)

# Numpad (Keypad) va NumLock tugmalari — to'g'ridan-to'g'ri tizimga o'tkaziladi
# Bu qulf ekrani (lockscreen), parol oynalari va numpad nuqtasining apparat darajasida to'siqsiz ishlashini ta'minlaydi
NUMPAD_KEYVALS = {
    IBus.KEY_KP_0, IBus.KEY_KP_1, IBus.KEY_KP_2, IBus.KEY_KP_3, IBus.KEY_KP_4,
    IBus.KEY_KP_5, IBus.KEY_KP_6, IBus.KEY_KP_7, IBus.KEY_KP_8, IBus.KEY_KP_9,
    IBus.KEY_KP_Insert, IBus.KEY_KP_End, IBus.KEY_KP_Down, IBus.KEY_KP_Page_Down,
    IBus.KEY_KP_Left, IBus.KEY_KP_Begin, IBus.KEY_KP_Right,
    IBus.KEY_KP_Home, IBus.KEY_KP_Up, IBus.KEY_KP_Page_Up,
    IBus.KEY_KP_Delete, IBus.KEY_KP_Decimal, IBus.KEY_KP_Separator,
    IBus.KEY_KP_Add, IBus.KEY_KP_Subtract, IBus.KEY_KP_Multiply, IBus.KEY_KP_Divide,
    IBus.KEY_KP_Enter, IBus.KEY_Num_Lock
}

# Maxsus navigatsiya va boshqaruv tugmalari
NAV_KEYVALS = {
    IBus.KEY_Return, IBus.KEY_KP_Enter, IBus.KEY_Tab, IBus.KEY_ISO_Left_Tab,
    IBus.KEY_Left, IBus.KEY_Right, IBus.KEY_Up, IBus.KEY_Down,
    IBus.KEY_Home, IBus.KEY_End, IBus.KEY_Page_Up, IBus.KEY_Page_Down,
    IBus.KEY_Delete, IBus.KEY_Insert
}

COMPONENT_NAME = "org.freedesktop.IBus.YangiAlifbo"
ENGINE_NAME = "yangialifbo"


class YangiAlifboEngine(IBus.Engine):
    __gtype_name__ = 'YangiAlifboEngine'

    def __init__(self, bus, obj_path):
        super().__init__(connection=bus.get_connection(), object_path=obj_path)
        self.bus = bus
        self.buffer = ""
        self.is_enabled = True
        self.prop_toggle = None
        self.timeout_id = 0

    def do_enable(self):
        self._init_properties()

    def do_disable(self):
        self._flush_buffer()

    def do_focus_in(self):
        self._cancel_timeout()
        self.buffer = ""
        if not self.prop_toggle:
            self._init_properties()

    def do_focus_out(self):
        self._flush_buffer()

    def do_reset(self):
        self._cancel_timeout()
        self.buffer = ""

    def do_set_cursor_location(self, x, y, w, h):
        # Sichqoncha bilan bosilganda kursor o'zgarganda buferni tozalash
        if self.buffer:
            self._flush_buffer()

    def do_set_surrounding_text(self, text, cursor_pos, anchor_pos):
        # Matn tanlanganda yoki sichqoncha bilan paste qilinganda buferni tozalash
        if self.buffer:
            self._flush_buffer()

    def _init_properties(self):
        prop_list = IBus.PropList()

        self.prop_toggle = IBus.Property.new(
            "yangialifbo_toggle",
            IBus.PropType.TOGGLE,
            IBus.Text.new_from_string("Yangi Alifbo (ş, ç, ö, ğ)"),
            None,
            IBus.Text.new_from_string("Holat: Yoqilgan / Oʻchirilgan (Ctrl+Alt+Y)"),
            True,
            True,
            IBus.PropState.CHECKED if self.is_enabled else IBus.PropState.UNCHECKED,
            None
        )
        prop_list.append(self.prop_toggle)

        prop_about = IBus.Property.new(
            "yangialifbo_about",
            IBus.PropType.NORMAL,
            IBus.Text.new_from_string("224.uz/alifbo · His perspective"),
            None,
            IBus.Text.new_from_string("Loyiha saytiga oʻtish"),
            True,
            True,
            IBus.PropState.UNCHECKED,
            None
        )
        prop_list.append(prop_about)

        self.register_properties(prop_list)

    def do_property_activate(self, prop_name, state):
        if prop_name == "yangialifbo_toggle":
            self.is_enabled = not self.is_enabled
            self._flush_buffer()
            self._update_property_state()
        elif prop_name == "yangialifbo_about":
            os.system("xdg-open 'https://224.uz/alifbo/' >/dev/null 2>&1 &")

    def _update_property_state(self):
        if self.prop_toggle:
            self.prop_toggle.set_state(
                IBus.PropState.CHECKED if self.is_enabled else IBus.PropState.UNCHECKED
            )
            self.update_property(self.prop_toggle)

    def _cancel_timeout(self):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = 0

    def _on_timeout(self):
        self.timeout_id = 0
        if self.buffer:
            buf = self.buffer
            self.buffer = ""
            self.commit_text(IBus.Text.new_from_string(buf))
        return GLib.SOURCE_REMOVE

    def _flush_buffer(self):
        self._cancel_timeout()
        if self.buffer:
            buf = self.buffer
            self.buffer = ""
            self.commit_text(IBus.Text.new_from_string(buf))

    def do_process_key_event(self, keyval, keycode, state):
        # 1. Tugma qo'yib yuborilganda (Release) e'tibor bermaymiz
        if state & IBus.ModifierType.RELEASE_MASK:
            return False

        # 2. Numpad (Keypad) va navigatsiya tugmalari to'g'ridan-to'g'ri o'tkaziladi
        # Bu qulf ekrani (lockscreen), parol oynalari va numpad nuqtasining apparat darajasida to'siqsiz ishlashini ta'minlaydi
        if keyval in NUMPAD_KEYVALS or keyval in NAV_KEYVALS:
            self._flush_buffer()
            return False

        # 3. Ctrl, Alt yoki Super tugmalari kombinatsiyasini tekshirish
        has_ctrl = bool(state & IBus.ModifierType.CONTROL_MASK)
        has_alt = bool(state & IBus.ModifierType.MOD1_MASK)
        has_super = bool(state & (IBus.ModifierType.MOD4_MASK | IBus.ModifierType.SUPER_MASK))

        # Ctrl+Alt+Y — Drayverni vaqtincha yoqish / o'chirish
        if has_ctrl and has_alt and not has_super and keyval in (IBus.KEY_y, IBus.KEY_Y):
            self.is_enabled = not self.is_enabled
            self._flush_buffer()
            self._update_property_state()
            return True

        # Boshqa barcha Ctrl / Alt / Super kombinatsiyalarida buferni bo'shatib, to'g'ridan-to'g'ri o'tkazamiz
        if has_ctrl or has_alt or has_super:
            self._flush_buffer()
            return False

        # 4. Agar drayver Ctrl+Alt+Y orqali o'chirilgan bo'lsa
        if not self.is_enabled:
            return False

        # 5. Escape tugmasi: agar buferda kutilayotgan harf bo'lsa uni bekor qiladi
        if keyval == IBus.KEY_Escape:
            if self.buffer:
                self._cancel_timeout()
                self.buffer = ""
                return True
            return False

        # 6. Backspace: agar buferda kutilayotgan harf bo'lsa uni bekor qiladi, bo'lmasa ilovaga o'tkazadi
        if keyval == IBus.KEY_BackSpace:
            if self.buffer:
                self._cancel_timeout()
                self.buffer = ""
                return True
            return False

        # 7. Space tugmasi
        if keyval in (IBus.KEY_space, IBus.KEY_KP_Space):
            if self.buffer:
                self._cancel_timeout()
                prev = self.buffer
                self.buffer = ""
                self.commit_text(IBus.Text.new_from_string(prev + " "))
                return True
            return False

        # 8. Oddiy belgiga aylantirish
        char = IBus.keyval_to_unicode(keyval)
        if not char or ord(char) < 32:
            self._flush_buffer()
            return False

        # Kirill (ruscha) harflar bo'lsa darhol to'g'ridan-to'g'ri o'tkazamiz
        if ord(char) >= 0x0400:
            self._flush_buffer()
            return False

        # 9. Agar bufer bo'sh bo'lsa
        if not self.buffer:
            if char in PREFIX_KEYS:
                self.buffer = char
                self._cancel_timeout()
                # 1000 ms (1 sekund) ichida keyingi harf bosilmasa avtomatik commit qilish
                self.timeout_id = GLib.timeout_add(TIMEOUT_DELAY_MS, self._on_timeout)
                return True
            # Prefiks bo'lmasa (raqamlar, boshqa harflar va belgilar) darhol ilovaga o'tadi
            return False

        # 10. Buferda prefiks harf bo'lsa, almashtirish qoidasini tekshiramiz
        self._cancel_timeout()
        prev = self.buffer
        rep = None

        # sh -> ş
        if prev in ('s', 'S') and char in ('h', 'H'):
            rep = 'Ş' if prev.isupper() else 'ş'
        # ch -> ç
        elif prev in ('c', 'C') and char in ('h', 'H'):
            rep = 'Ç' if prev.isupper() else 'ç'
        # o' -> ö
        elif prev in ('o', 'O') and char in APOSTROPHES:
            rep = 'Ö' if prev.isupper() else 'ö'
        # g' -> ğ
        elif prev in ('g', 'G') and char in APOSTROPHES:
            rep = 'Ğ' if prev.isupper() else 'ğ'

        if rep:
            self.buffer = ""
            self.commit_text(IBus.Text.new_from_string(rep))
            return True

        # Mos kelmadi:
        self.buffer = ""

        # Agar yangi kiritilgan belgi ham yangi prefiks bo'lsa (masalan "so" yoki "ss")
        if char in PREFIX_KEYS:
            self.commit_text(IBus.Text.new_from_string(prev))
            self.buffer = char
            self.timeout_id = GLib.timeout_add(TIMEOUT_DELAY_MS, self._on_timeout)
            return True

        # Oddiy holat: oldingi belgini va yangi belgini birga chiqaramiz (masalan "sa", "oz", "s1")
        self.commit_text(IBus.Text.new_from_string(prev + char))
        return True


class YangiAlifboFactory(IBus.Factory):
    __gtype_name__ = 'YangiAlifboFactory'

    def __init__(self, bus):
        super().__init__(connection=bus.get_connection(), object_path=IBus.PATH_FACTORY)
        self.bus = bus
        self.engine_id = 0

    def do_create_engine(self, engine_name):
        if engine_name == ENGINE_NAME:
            self.engine_id += 1
            obj_path = f"/org/freedesktop/IBus/Engine/{self.engine_id}"
            return YangiAlifboEngine(self.bus, obj_path)
        return None


def main():
    IBus.init()
    bus = IBus.Bus()
    if not bus.is_connected():
        print("Xatolik: IBus daemon bilan aloqa o'rnatib bo'lmadi.", file=sys.stderr)
        sys.exit(1)

    factory = YangiAlifboFactory(bus)
    factory.add_engine(ENGINE_NAME, YangiAlifboEngine.__gtype__)

    bus.request_name(COMPONENT_NAME, 0)
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
