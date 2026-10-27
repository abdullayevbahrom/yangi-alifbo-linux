#!/usr/bin/env bash
#
# Yangi Alifbo (Linux) — O'rnatish Skripti
# 224.uz/alifbo loyihasi asosida
# Mualliflar: Bahrom Abdullayev (https://github.com/abdullayevbahrom) & His perspective (https://t.me/hisperspective)
#

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================${NC}"
echo -e "${GREEN}  Yangi Oʻzbek Alifbosi (ş, ç, ö, ğ) — Linux Oʻrnatuvchisi${NC}"
echo -e "${BLUE}  Loyiha: 224.uz/alifbo · His perspective${NC}"
echo -e "${BLUE}======================================================${NC}"

# Foydalanuvchi kataloglarini aniqlash
TARGET_HOME="${HOST_HOME:-$HOME}"
INSTALL_DIR="$TARGET_HOME/.local/share/ibus-yangialifbo"
COMPONENT_DIR="$TARGET_HOME/.local/share/ibus/component"
AUTOSTART_DIR="$TARGET_HOME/.config/autostart"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "\n${BLUE}1. Tizim talablarini tekshirish...${NC}"

# Python3 tekshirish
if ! command -v /usr/bin/python3 >/dev/null 2>&1; then
    echo -e "${RED}Xatolik: /usr/bin/python3 topilmadi.${NC}"
    exit 1
fi

# IBus tekshirish
if ! command -v ibus >/dev/null 2>&1; then
    echo -e "${YELLOW}IBus topilmadi. O'rnatilmoqda (sudo talab qilinishi mumkin)...${NC}"
    sudo apt-get update && sudo apt-get install -y ibus gir1.2-ibus-1.0 python3-gi python3-xlib
fi

# python3-gi va python3-xlib tekshirish
if ! /usr/bin/python3 -c "import gi; gi.require_version('IBus', '1.0'); from gi.repository import IBus" >/dev/null 2>&1; then
    echo -e "${YELLOW}IBus Python kutubxonalari yetishmayapti. O'rnatilmoqda...${NC}"
    sudo apt-get update && sudo apt-get install -y gir1.2-ibus-1.0 python3-gi python3-ibus-1.0 python3-xlib
fi

echo -e "${GREEN}✓ Barcha talablar mavjud.${NC}"

echo -e "\n${BLUE}2. Fayllarni ko'chirish...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$COMPONENT_DIR"
mkdir -p "$AUTOSTART_DIR"

cp "$SCRIPT_DIR/engine.py" "$INSTALL_DIR/engine.py"
chmod +x "$INSTALL_DIR/engine.py"

cp "$SCRIPT_DIR/yangialifbo.svg" "$INSTALL_DIR/yangialifbo.svg"

# XML faylni to'g'ri yo'llar bilan generatsiya qilish
cat > "$COMPONENT_DIR/yangialifbo.xml" <<EOF
<?xml version="1.0" encoding="utf-8"?>
<component>
    <name>org.freedesktop.IBus.YangiAlifbo</name>
    <description>Yangi Oʻzbek Alifbosi (ş, ç, ö, ğ) Kirish Dvigateli</description>
    <exec>${INSTALL_DIR}/engine.py --ibus</exec>
    <version>1.0.1</version>
    <author>Bahrom Abdullayev &amp; His perspective</author>
    <license>MIT</license>
    <homepage>https://224.uz/alifbo/</homepage>
    <textdomain>ibus-yangialifbo</textdomain>
    <engines>
        <engine>
            <name>yangialifbo</name>
            <language>uz</language>
            <license>MIT</license>
            <author>Bahrom Abdullayev &amp; His perspective</author>
            <icon>${INSTALL_DIR}/yangialifbo.svg</icon>
            <layout>default</layout>
            <longname>Yangi Oʻzbek Alifbosi (ş, ç, ö, ğ)</longname>
            <description>sh-&gt;ş, ch-&gt;ç, o'-&gt;ö, g'-&gt;ğ avtomatik almashtirish</description>
            <rank>99</rank>
            <symbol>ş</symbol>
        </engine>
    </engines>
</component>
EOF

# Agar HOME profil muhitida bo'lsa, ikkala katalogga ham sinxronlash
if [ "$HOME" != "$TARGET_HOME" ]; then
    mkdir -p "$HOME/.local/share/ibus/component"
    cp "$COMPONENT_DIR/yangialifbo.xml" "$HOME/.local/share/ibus/component/yangialifbo.xml"
fi

echo -e "${GREEN}✓ Dvigatel va komponent muvaffaqiyatli o'rnatildi: $INSTALL_DIR${NC}"

echo -e "\n${BLUE}3. NumLock va Numpad integratsiyasi...${NC}"
# COSMIC Desktop uchun NumLock va Numpad nuqtasini (kpdl:dot) sozlash
COSMIC_KB_CONFIG="$TARGET_HOME/.config/cosmic/com.system76.CosmicComp/v1/keyboard_config"
if [ -d "$(dirname "$COSMIC_KB_CONFIG")" ]; then
    cat > "$COSMIC_KB_CONFIG" <<EOF
(
    numlock_state: BootOn,
)
EOF
    echo -e "${GREEN}✓ COSMIC NumLock holati: BootOn (har doim yoniq)${NC}"
fi

COSMIC_XKB_CONFIG="$TARGET_HOME/.config/cosmic/com.system76.CosmicComp/v1/xkb_config"
if [ -f "$COSMIC_XKB_CONFIG" ]; then
    # Numpad nuqtasi ruscha va boshqa tartiblarda ham vergul emas, doimo nuqta bo'lishi uchun
    if grep -q 'options: None' "$COSMIC_XKB_CONFIG"; then
        sed -i 's/options: None/options: Some("kpdl:dot")/' "$COSMIC_XKB_CONFIG"
    elif grep -q 'options: Some' "$COSMIC_XKB_CONFIG" && ! grep -q 'kpdl:dot' "$COSMIC_XKB_CONFIG"; then
        sed -i 's/options: Some("\([^"]*\)")/options: Some("\1,kpdl:dot")/' "$COSMIC_XKB_CONFIG"
    fi
    echo -e "${GREEN}✓ COSMIC Numpad nuqtasi sozlamasi: kpdl:dot (doimiy nuqta)${NC}"
fi

# GNOME Desktop uchun NumLock va Numpad nuqtasi
if command -v gsettings >/dev/null 2>&1; then
    gsettings set org.gnome.desktop.peripherals.keyboard remember-numlock-state true 2>/dev/null || true
    gsettings set org.gnome.desktop.peripherals.keyboard numlock-state true 2>/dev/null || true
    gsettings set org.freedesktop.ibus.general use-system-keyboard-layout true 2>/dev/null || true
    gsettings set org.gnome.desktop.input-sources xkb-options "['kpdl:dot']" 2>/dev/null || true
    echo -e "${GREEN}✓ GNOME / XKB Numpad nuqtasi sozlamasi: kpdl:dot${NC}"
fi

echo -e "\n${BLUE}4. IBus keshini yangilash va qayta ishga tushirish...${NC}"
ibus write-cache >/dev/null 2>&1 || true
ibus restart >/dev/null 2>&1 || true
sleep 1

# IBus dvigatellari ro'yxatida tekshirish
if ibus list-engine 2>/dev/null | grep -q "yangialifbo"; then
    echo -e "${GREEN}✓ 'yangialifbo' IBus tizimiga muvaffaqiyatli qo'shildi!${NC}"
else
    echo -e "${YELLOW}! Kesh yangilandi. IBus qayta ishga tushgach ro'yxatda paydo bo'ladi.${NC}"
fi

# GNOME desktop uchun avtomatik qo'shish imkoniyatini tekshirish
if command -v gsettings >/dev/null 2>&1; then
    CURRENT_SOURCES=$(gsettings get org.gnome.desktop.input-sources sources 2>/dev/null || echo "")
    if [[ "$CURRENT_SOURCES" == *"yangialifbo"* ]]; then
        echo -e "${GREEN}✓ 'yangialifbo' allaqachon kirish manbalari ro'yxatida mavjud.${NC}"
    elif [ -n "$CURRENT_SOURCES" ] && [ "$CURRENT_SOURCES" != "@a(ss) []" ]; then
        NEW_SOURCES="${CURRENT_SOURCES%]*}, ('ibus', 'yangialifbo')]"
        gsettings set org.gnome.desktop.input-sources sources "$NEW_SOURCES" 2>/dev/null || true
        echo -e "${GREEN}✓ GNOME sozlamalariga 'Yangi Oʻzbek Alifbosi' qo'shildi.${NC}"
    fi
fi

echo -e "\n${GREEN}======================================================${NC}"
echo -e "${GREEN}  TABRIKLAYMIZ! Oʻrnatish muvaffaqiyatli yakunlandi!   ${NC}"
echo -e "${GREEN}======================================================${NC}"
echo -e "Foydalanish boʻyicha qoʻllanma:"
echo -e "  1. Uzbek Latin (uz) da: ${GREEN}Avtomatik ishlaydi!${NC}"
echo -e "     - ${GREEN}sh${NC}  →  ${GREEN}ş${NC}"
echo -e "     - ${GREEN}ch${NC}  →  ${GREEN}ç${NC}"
echo -e "     - ${GREEN}o'${NC}  →  ${GREEN}ö${NC}"
echo -e "     - ${GREEN}g'${NC}  →  ${GREEN}ğ${NC}"
echo -e "  2. English (us) da: Oddiy yozuv. Kerak bo'lsa ${YELLOW}Ctrl + Alt + Y${NC} bilan yoqiladi."
echo -e "  3. Numpad va lockscreen: Numpad tugmalari va qulf ekrani parollari to'siqsiz ishlaydi."
echo -e "======================================================\n"
