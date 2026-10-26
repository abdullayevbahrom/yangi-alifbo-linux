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

### Asosiy afzalliklari:
1. **Oʻzbekcha (uz) tartibida avtomatik:** Tizim klaviaturasi `uz` (Oʻzbek lotin) holatida boʻlganda harflar avtomatik alishadi.
2. **Inglizcha (us) tartibida bezovta qilmaydi:** Ingliz tilida odatiy yoziladi (`sh`, `ch` oʻzgarmaydi). Agar ingliz tilida ham kerak boʻlsa, `Ctrl + Alt + Y` orqali yoqiladi.
3. **Numpad (raqamlar bloki) doimiy ishlaydi:** NumLock tugmasi oʻchiq yoki yoniq boʻlishidan qatʼi nazar, oʻng tarafdagi raqamlar klaviaturasi har doim raqam yozadi.
4. **Resurs sarfi minimal:** Bor-yoʻgʻi ~20 MB operativ xotira (RAM) oladi, protsessorga nol yuklama.

---

## 📦 Oʻrnatish (Har bir holat boʻyicha)

Quyida oʻzingizning Linux tizimingizga mos usulni tanlang:

### Case 1: Tavsiya etilgan universal usul (Root / sudo talab qilinmaydi)
Barcha Linux distributivlari (Ubuntu, Debian, Fedora, Arch, Pop!_OS, Linux Mint, Manjaro va boshqalar) uchun eng qulay usul. Barcha sozlamalarni oʻzi avtomatik toʻgʻrilaydi.

```bash
# Repozitoriyni yuklab olish
git clone https://github.com/abdullayevbahrom/yangi-alifbo-linux.git
cd yangi-alifbo-linux

# O'rnatish
./install.sh
```

Yoki terminalda bir martalik buyruq bilan:
```bash
curl -fsSL https://raw.githubusercontent.com/abdullayevbahrom/yangi-alifbo-linux/main/install.sh | bash
```

> **Eslatma:** Hech qanday `sudo` paroli soʻralmaydi. Dvigatel foydalanuvchining shaxsiy `~/.local/share/` katalogiga oʻrnatiladi va GNOME/KDE/COSMIC sozlamalariga avtomatik ulanadi.

---

### Case 2: Debian / Ubuntu / Linux Mint / Pop!_OS (.deb paket orqali)
Tizim darajasida barcha foydalanuvchilar uchun oʻrnatish:

1. [Releases](https://github.com/abdullayevbahrom/yangi-alifbo-linux/releases) boʻlimidan eng soʻnggi `.deb` faylni yuklab oling yoki terminalda bajaring:
   ```bash
   sudo dpkg -i yangi-alifbo-ibus_1.0.0_all.deb
   ```
2. Oʻrnatilgandan soʻng:
   - **Standart GNOME / KDE / XFCE tizimlarida:** Bir marta kompyuterdan chiqib qayta kiring (Log out / Log in) yoki terminalda `ibus restart` bering.
   - **Tizim sozlamalari:** *Settings (Sozlamalar) → Keyboard (Klaviatura) → Input Sources (+)* boʻlimidan **"Yangi Oʻzbek Alifbosi (ş, ç, ö, ğ)"** ni kiritish manbasi sifatida qoʻshib qoʻying.

---

### Case 3: Fedora / RHEL / openSUSE (.rpm paket orqali)
Red Hat / Fedora oilasidagi distributivlar uchun:

1. [Releases](https://github.com/abdullayevbahrom/yangi-alifbo-linux/releases) boʻlimidan `.rpm` faylni oling va oʻrnating:
   ```bash
   sudo rpm -i yangi-alifbo-ibus-1.0.0.noarch.rpm
   ```
2. IBus xizmatini yangilang:
   ```bash
   ibus write-cache && ibus restart
   ```
3. Sozlamalardan klaviatura tartibini qoʻshing.

---

### Case 4: Pop!_OS COSMIC Desktop (Wayland) foydalanuvchilari uchun
Pop!_OS 24.04+ yangi Rust asosidagi COSMIC muhitida (Wayland) IBus integratsiyasi oʻziga xos ishlaydi:

- Paket oʻrnatilgandan soʻng avtomatik `~/.config/autostart/ibus-wayland-yangialifbo.desktop` orqali seans boshida ishga tushadi.
- Agar kompyuterni qayta ishga tushirmasdan, darhol sinab koʻrmoqchi boʻlsangiz:
  ```bash
  ibus write-cache
  /home/$USER/.local/bin/ibus-wayland-start
  ```
  *(Keyingi safar tizimga kirganingizda ushbu buyruqni kiritish shart emas, u avtomatik ishlaydi).*

---

## ⌨️ Foydalanish va Boshqarish

1. **Tilni almashtirish:** `Super (Win) + Boʻsh joy (Space)` orqali kiritish usulini tanlaysiz.
2. **Vaqtincha yoqish / oʻchirish (Hot-key):**
   - Istalgan vaqtda `Ctrl + Alt + Y` tugmalarini bosish orqali dvigatelni yoqish yoki vaqtincha toʻxtatish mumkin.
3. **Tray belgisi:** Yuqori panelda (system tray) maxsus `ş` belgisi aks etadi. Uni bosib holatni tekshirish yoki [224.uz/alifbo](https://224.uz/alifbo/) saytiga oʻtish mumkin.

---

## 🛠 Nosozliklarni bartaraf etish (Troubleshooting)

- **Klaviatura roʻyxatida "Yangi Oʻzbek Alifbosi" koʻrinmayapti:**
  Terminalda keshni tozalab, IBusʼni qayta ishga tushiring:
  ```bash
  ibus write-cache
  ibus restart
  ```
- **Kutubxonalar yetishmovchiligi xatosi:**
  Agar Python IBus kutubxonalari topilmasa:
  - Ubuntu/Debian: `sudo apt install python3-gi gir1.2-ibus-1.0 python3-xlib`
  - Fedora: `sudo dnf install python3-gobject ibus-libs python3-xlib`

---

## 🗑️ Tizimdan oʻchirish

- Agar `./install.sh` orqali oʻrnatilgan boʻlsa:
  ```bash
  ./uninstall.sh
  ```
- Agar `.deb` orqali oʻrnatilgan boʻlsa:
  ```bash
  sudo dpkg -r yangi-alifbo-ibus
  ```
- Agar `.rpm` orqali oʻrnatilgan boʻlsa:
  ```bash
  sudo rpm -e yangi-alifbo-ibus
  ```

---

## 📄 Mualliflik va Litsenziya

- **Gʻoya va qoidalar:** [224.uz/alifbo](https://224.uz/alifbo/)
- **Dastur muallifi:** [His perspective](https://t.me/hisperspective) ([GitHub](https://github.com/abdullayevbahrom))
- **Litsenziya:** MIT License — erkin va ochiq kodli dasturiy taʼminot.
