# Yangi Oʻzbek Alifbosi (ş, ç, ö, ğ) — Linux Kiritish Tizimi

[224.uz/alifbo/#klaviatura](https://224.uz/alifbo/#klaviatura) loyihasi asosida yaratilgan rasmiy Linux IBus dvigateli.

Ushbu tizim Linux (Wayland va X11, Ubuntu, Fedora, Debian, Pop!_OS, Linux Mint, Arch) foydalanuvchilariga xuddi Windows (AutoHotkey) va macOS (Keylayout bundle) kabi matn yozayotgan paytda harflarni bir zumda avtomatik almashtirish imkonini beradi.

---

## ⚡ Qanday ishlaydi?

Siz odatdagidek yozasiz — klaviatura esa yangi alifboga avtomatik oʻgiradi:
- `sh`  →  **`ş`**  (Katta harflarda: `Sh` / `SH` → **`Ş`**)
- `ch`  →  **`ç`**  (Katta harflarda: `Ch` / `CH` → **`Ç`**)
- `o'`  →  **`ö`**  (Barcha tutuq belgilari: `'`, ``` ` ```, `‘`, `’`, `ʻ`, `ʼ` → **`ö`** / **`Ö`**)
- `g'`  →  **`ğ`**  (Barcha tutuq belgilari: `'`, ``` ` ```, `‘`, `’`, `ʻ`, `ʼ` → **`ğ`** / **`Ğ`**)

Oddiy soʻzlar (masalan: `salom`, `osmon`, `gap`, `choy`, `assalomu alaykum`) yozilganda hech qanday kechikish yoki xatolik boʻlmaydi.

---

## 🚀 Oʻrnatish (1 ta buyruq bilan)

Terminalni oching va quyidagi buyruqni bering:

```bash
cd yangi-alifbo-linux
chmod +x install.sh
./install.sh
```

Yoki masofadan toʻgʻridan-toʻgʻri:
```bash
curl -fsSL https://raw.githubusercontent.com/hisperspective/yangi-alifbo-linux/main/install.sh | bash
```

> **Eslatma:** Root (sudo) paroli talab qilinmaydi! Barcha fayllar foydalanuvchining shaxsiy `~/.local/share/` katalogiga oʻrnatiladi.

---

## ⌨️ Foydalanish

1. **Klaviaturani almashtirish:** `Super (Win) + Boʻsh joy (Space)` orqali "Yangi Oʻzbek Alifbosi (ş, ç, ö, ğ)" tartibiga oʻtasiz.
2. **Vaqtincha yoqish / oʻchirish:** `Ctrl + Alt + Y` kombinatsiyasini bossangiz, dvigatel vaqtincha oddiy yozuvga oʻtadi yoki qayta yoqiladi.
3. **Sozlamalar paneli:** Yuqori panelda (system tray) maxsus `ş` belgisi chiqadi. Uni bosib holatni tekshirish yoki [224.uz/alifbo](https://224.uz/alifbo/) saytiga oʻtish mumkin.

---

## 🗑️ Tizimdan oʻchirish

```bash
./uninstall.sh
```

---

## 📄 Mualliflik va Litsenziya

- Loyiha asoschisi: [224.uz](https://224.uz/alifbo/) va [His perspective](https://t.me/hisperspective)
- Litsenziya: MIT License
