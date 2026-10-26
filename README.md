# Yangi Özbek Alifbosi (ş, ç, ö, ğ) — Linux Kiritiş Tizimi

[224.uz/alifbo/#klaviatura](https://224.uz/alifbo/#klaviatura) loyihasi asosida yaratilgan rasmiy Linux IBus dvigateli.

Uşbu tizim Linux (Wayland va X11, Ubuntu, Fedora, Debian, Pop!_OS, Linux Mint, Arch) foydalanuvçilariga xuddi Windows (AutoHotkey) va macOS (Keylayout bundle) kabi matn yozayotgan paytda harflarni bir zumda avtomatik almaştiriş imkonini beradi.

---

## ⚡ Qanday işlaydi?

Siz odatdagidek yozasiz — klaviatura esa yangi alifboga avtomatik ögiradi:
- `sh`  →  **`ş`**  (Katta harflarda: `Sh` / `SH` → **`Ş`**)
- `ch`  →  **`ç`**  (Katta harflarda: `Ch` / `CH` → **`Ç`**)
- `o'`  →  **`ö`**  (Barça tutuq belgilari: `'`, ``` ` ```, `‘`, `’`, `ʻ`, `ʼ` → **`ö`** / **`Ö`**)
- `g'`  →  **`ğ`**  (Barça tutuq belgilari: `'`, ``` ` ```, `‘`, `’`, `ʻ`, `ʼ` → **`ğ`** / **`Ğ`**)

### Asosiy afzalliklari:
1. **Özbekça (uz) tartibida avtomatik:** Tizim klaviaturasi `uz` (Özbek lotin) holatida bölganda harflar avtomatik alişadi.
2. **Inglizça (us) tartibida bezovta qilmaydi:** Ingliz tilida odatiy yoziladi (`sh`, `ch` özgarmaydi). Agar ingliz tilida ham kerak bölsa, `Ctrl + Alt + Y` orqali yoqiladi.
3. **Numpad (raqamlar bloki) doimiy işlaydi:** NumLock tugmasi öçiq yoki yoniq bölişidan qatʼi nazar, öng tarafdagi raqamlar klaviaturasi har doim raqam yozadi.
4. **Resurs sarfi minimal:** Bor-yöği ~20 MB operativ xotira (RAM) oladi, protsessorga nol yuklama.

---

## 📦 Örnatiş (Har bir holat böyiça)

Quyida özingizning Linux tizimingizga mos usulni tanlang:

### Case 1: Tavsiya etilgan universal usul (Root / sudo talab qilinmaydi)
Barça Linux distributivlari (Ubuntu, Debian, Fedora, Arch, Pop!_OS, Linux Mint, Manjaro va boşqalar) uçun eng qulay usul. Barça sozlamalarni özi avtomatik töğrilaydi.

```bash
# Repozitoriyni yuklab oliş
git clone https://github.com/abdullayevbahrom/yangi-alifbo-linux.git
cd yangi-alifbo-linux

# Örnatiş
./install.sh
```

Yoki terminalda bir martalik buyruq bilan:
```bash
curl -fsSL https://raw.githubusercontent.com/abdullayevbahrom/yangi-alifbo-linux/main/install.sh | bash
```

> **Eslatma:** Heç qanday `sudo` paroli söralmaydi. Dvigatel foydalanuvçining şaxsiy `~/.local/share/` katalogiga örnatiladi va GNOME/KDE/COSMIC sozlamalariga avtomatik ulanadi.

---

### Case 2: Debian / Ubuntu / Linux Mint / Pop!_OS (.deb paket orqali)
Tizim darajasida barça foydalanuvçilar uçun örnatiş:

1. [Releases](https://github.com/abdullayevbahrom/yangi-alifbo-linux/releases) bölimidan eng sönggi `.deb` faylni yuklab oling yoki terminalda bajaring:
   ```bash
   sudo dpkg -i yangi-alifbo-ibus_1.0.0_all.deb
   ```
2. Örnatilgandan söng:
   - **Standart GNOME / KDE / XFCE tizimlarida:** Bir marta kompyuterdan çiqib qayta kiring (Log out / Log in) yoki terminalda `ibus restart` bering.
   - **Tizim sozlamalari:** *Settings (Sozlamalar) → Keyboard (Klaviatura) → Input Sources (+)* bölimidan **"Yangi Özbek Alifbosi (ş, ç, ö, ğ)"** ni kiritiş manbasi sifatida qöşib qöying.

---

### Case 3: Fedora / RHEL / openSUSE (.rpm paket orqali)
Red Hat / Fedora oilasidagi distributivlar uçun:

1. [Releases](https://github.com/abdullayevbahrom/yangi-alifbo-linux/releases) bölimidan `.rpm` faylni oling va örnating:
   ```bash
   sudo rpm -i yangi-alifbo-ibus-1.0.0.noarch.rpm
   ```
2. IBus xizmatini yangilang:
   ```bash
   ibus write-cache && ibus restart
   ```
3. Sozlamalardan klaviatura tartibini qöşing.

---

### Case 4: Pop!_OS COSMIC Desktop (Wayland) foydalanuvçilari uçun
Pop!_OS 24.04+ yangi Rust asosidagi COSMIC muhitida (Wayland) IBus integratsiyasi öziga xos işlaydi:

- Paket örnatilgandan söng avtomatik `~/.config/autostart/ibus-wayland-yangialifbo.desktop` orqali seans boşida işga tuşadi.
- Agar kompyuterni qayta işga tuşirmasdan, darhol sinab körmoqçi bölsangiz:
   ```bash
   ibus write-cache
   /home/$USER/.local/bin/ibus-wayland-start
   ```
   *(Keyingi safar tizimga kirganingizda uşbu buyruqni kiritiş şart emas, u avtomatik işlaydi).*

---

## ⌨️ Foydalaniş va Boşqariş

1. **Tilni almaştiriş:** `Super (Win) + Böş joy (Space)` orqali kiritiş usulini tanlaysiz.
2. **Vaqtinça yoqiş / öçiriş (Hot-key):**
   - Istalgan vaqtda `Ctrl + Alt + Y` tugmalarini bosiş orqali dvigatelni yoqiş yoki vaqtinça töxtatiş mumkin.
3. **Tizim paneli integratsiyasi (GNOME / KDE):**
   - Standart GNOME va KDE iş stollarida yuqori paneldagi til indikatorida maxsus **`ş`** belgisi aks etadi. Uni bosganda [224.uz/alifbo](https://224.uz/alifbo/) saytiga ötiş va holatni köriş menyusi çiqadi.
   - Pop!_OS COSMIC va boşqa yengil oynali muhitlarda (i3, Sway) dvigatel orqa fonda xalaqit bermasdan işlaydi va barça boşqaruv `Ctrl + Alt + Y` orqali amalga oşiriladi.

---

## 🛠 Nosozliklarni bartaraf etiş (Troubleshooting)

- **Klaviatura röyxatida "Yangi Özbek Alifbosi" körinmayapti:**
  Terminalda keşni tozalab, IBusʼni qayta işga tuşiring:
  ```bash
  ibus write-cache
  ibus restart
  ```
- **Kutubxonalar yetişmovçiligi xatosi:**
  Agar Python IBus kutubxonalari topilmasa:
  - Ubuntu/Debian: `sudo apt install python3-gi gir1.2-ibus-1.0 python3-xlib`
  - Fedora: `sudo dnf install python3-gobject ibus-libs python3-xlib`

---

## 🗑️ Tizimdan öçiriş

- Agar `./install.sh` orqali örnatilgan bölsa:
  ```bash
  ./uninstall.sh
  ```
- Agar `.deb` orqali örnatilgan bölsa:
  ```bash
  sudo dpkg -r yangi-alifbo-ibus
  ```
- Agar `.rpm` orqali örnatilgan bölsa:
  ```bash
  sudo rpm -e yangi-alifbo-ibus
  ```

---

## 📄 Mualliflik va Litsenziya

- **Ğoya va qoidalar:** [224.uz/alifbo](https://224.uz/alifbo/)
- **Dastur mualliflari:** Bahrom Abdullayev ([@abdullayevbahrom](https://github.com/abdullayevbahrom)) & [His perspective](https://t.me/hisperspective)
- **Litsenziya:** MIT License — erkin va oçiq kodli dasturiy taʼminot.
