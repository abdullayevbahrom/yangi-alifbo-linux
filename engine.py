#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Yangi Alifbo — Linux IBus Kirish Dvigateli
224.uz/alifbo loyihasi (https://224.uz/alifbo/#klaviatura) asosida
Muallif: His perspective (https://t.me/hisperspective)

Avtomatik almashtirishlar:
  sh -> ş,  Sh -> Ş,  SH -> Ş,  sH -> ş
  ch -> ç,  Ch -> Ç,  CH -> Ç,  cH -> ç
  o' / o` / o‘ / o’ / oʻ / oʼ -> ö  (O' -> Ö)
  g' / g` / g‘ / g’ / gʻ / gʼ -> ğ  (G' -> Ğ)

Maxsus tugmalar:
  Ctrl+Alt+Y — drayverni vaqtincha yoqish / o'chirish
"""

import os
import sys
import gi

gi.require_version('IBus', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import IBus, GLib

APOSTROPHES = {"'", "`", "‘", "’", "ʻ", "ʼ"}
PREFIX_KEYS = {'s', 'S', 'c', 'C', 'o', 'O', 'g', 'G'}

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

    def do_enable(self):
        self._init_properties()

    def do_disable(self):
        self._flush_buffer()

    def do_focus_in(self):
        self._init_properties()

    def do_focus_out(self):
        self._flush_buffer()

    def do_reset(self):
        self.buffer = ""
        self.hide_preedit_text()

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
            self.toggle_enabled()
        elif prop_name == "yangialifbo_about":
            os.system("xdg-open 'https://224.uz/alifbo/' >/dev/null 2>&1 &")

    def toggle_enabled(self):
        self.is_enabled = not self.is_enabled
        self._flush_buffer()
        if self.prop_toggle:
            self.prop_toggle.set_state(
                IBus.PropState.CHECKED if self.is_enabled else IBus.PropState.UNCHECKED
            )
            self.update_property(self.prop_toggle)

    def _update_preedit(self):
        if self.buffer:
            text = IBus.Text.new_from_string(self.buffer)
            # Tagiga chiziq chizish (macOS/Windows uslubidagi preedit)
            attr = IBus.Attribute.new(
                IBus.AttrType.UNDERLINE,
                IBus.AttrUnderline.SINGLE,
                0,
                len(self.buffer)
            )
            text.append_attribute(attr)
            self.update_preedit_text(text, len(self.buffer), True)
        else:
            self.hide_preedit_text()

    def _flush_buffer(self):
        if self.buffer:
            self.commit_text(IBus.Text.new_from_string(self.buffer))
            self.buffer = ""
            self.hide_preedit_text()

    def do_process_key_event(self, keyval, keycode, state):
        # 1. Tugma qo'yib yuborilganda (Release) e'tibor bermaymiz
        if state & IBus.ModifierType.RELEASE_MASK:
            return False

        # 2. Ctrl, Alt yoki Super tugmalari kombinatsiyasini tekshirish
        has_ctrl = bool(state & IBus.ModifierType.CONTROL_MASK)
        has_alt = bool(state & (IBus.ModifierType.MOD1_MASK | IBus.ModifierType.MOD4_MASK))

        # Ctrl+Alt+Y — Yoqish / O'chirish
        if has_ctrl and has_alt and keyval in (IBus.KEY_y, IBus.KEY_Y):
            self.toggle_enabled()
            return True

        # Boshqa barcha Ctrl / Alt / Super kombinatsiyalarida buferni bo'shatib, to'g'ridan-to'g'ri o'tkazamiz
        if has_ctrl or has_alt or (state & IBus.ModifierType.SUPER_MASK):
            self._flush_buffer()
            return False

        # 3. Agar drayver vaqtincha o'chirilgan bo'lsa
        if not self.is_enabled:
            return False

        # 4. Backspace
        if keyval == IBus.KEY_BackSpace:
            if self.buffer:
                self.buffer = ""
                self._update_preedit()
                return True
            return False

        # 5. Navigatsiya va maxsus tugmalar (Enter, Tab, Escape, Arrow keys...)
        if keyval in (IBus.KEY_Return, IBus.KEY_KP_Enter, IBus.KEY_Tab, IBus.KEY_Escape,
                      IBus.KEY_Left, IBus.KEY_Right, IBus.KEY_Up, IBus.KEY_Down,
                      IBus.KEY_Home, IBus.KEY_End, IBus.KEY_Page_Up, IBus.KEY_Page_Down,
                      IBus.KEY_Delete, IBus.KEY_Insert):
            self._flush_buffer()
            return False

        # 6. Space tugmasi
        if keyval in (IBus.KEY_space, IBus.KEY_KP_Space):
            if self.buffer:
                prev = self.buffer
                self.buffer = ""
                self._update_preedit()
                self.commit_text(IBus.Text.new_from_string(prev + " "))
                return True
            return False

        # 7. Oddiy belgiga aylantirish
        char = IBus.keyval_to_unicode(keyval)
        if not char or ord(char) < 32:
            self._flush_buffer()
            return False

        # 8. Agar bufer bo'sh bo'lsa
        if not self.buffer:
            if char in PREFIX_KEYS:
                self.buffer = char
                self._update_preedit()
                return True
            # Prefiks bo'lmasa, darhol ilovaga o'tkazamiz (nol kechikish)
            return False

        # 9. Buferda harf bo'lsa, almashtirish qoidasini tekshiramiz
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
            self._update_preedit()
            self.commit_text(IBus.Text.new_from_string(rep))
            return True

        # Mos kelmadi:
        self.buffer = ""
        self._update_preedit()

        # Agar yangi kiritilgan belgi ham yangi prefiks bo'lsa (masalan "so" yoki "ss")
        if char in PREFIX_KEYS:
            self.commit_text(IBus.Text.new_from_string(prev))
            self.buffer = char
            self._update_preedit()
            return True

        # Oddiy holat: oldingi belgini va yangi belgini birga chiqaramiz
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
