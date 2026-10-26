#!/usr/bin/env bash
#
# Yangi Alifbo (Linux) — O'rnatish Skripti
# 224.uz/alifbo loyihasi asosida
# Muallif: His perspective (https://t.me/hisperspective)
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
    sudo apt-get update && sudo apt-get install -y ibus gir1.2-ibus-1.0 python3-gi
fi

# python3-gi tekshirish
if ! /usr/bin/python3 -c "import gi; gi.require_version('IBus', '1.0'); from gi.repository import IBus" >/dev/null 2>&1; then
    echo -e "${YELLOW}IBus Python kutubxonalari yetishmayapti. O'rnatilmoqda...${NC}"
    sudo apt-get update && sudo apt-get install -y gir1.2-ibus-1.0 python3-gi python3-ibus-1.0
fi

echo -e "${GREEN}✓ Barcha talablar mavjud.${NC}"

echo -e "\n${BLUE}2. Fayllarni ko'chirish...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$COMPONENT_DIR"

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
    <version>1.0.0</version>
    <author>His perspective &lt;https://t.me/hisperspective&gt;</author>
    <license>MIT</license>
    <homepage>https://224.uz/alifbo/</homepage>
    <textdomain>ibus-yangialifbo</textdomain>
    <engines>
        <engine>
            <name>yangialifbo</name>
            <language>uz</language>
            <license>MIT</license>
            <author>His perspective</author>
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

echo -e "\n${BLUE}3. IBus keshini yangilash va qayta ishga tushirish...${NC}"
ibus write-cache >/dev/null 2>&1 || true
ibus restart >/dev/null 2>&1 || true
sleep 1

# IBus dvigatellari ro'yxatida tekshirish
if ibus list-engine 2>/dev/null | grep -q "yangialifbo"; then
    echo -e "${GREEN}✓ 'yangialifbo' IBus tizimiga muvaffaqiyatli qo'shildi!${NC}"
else
    echo -e "${YELLOW}! Kesh yangilandi. IBus qayta ishga tushgach ro'yxatda paydo bo'ladi.${NC}"
fi

echo -e "\n${BLUE}4. Kiritish usulini sozlash...${NC}"
# GNOME desktop uchun avtomatik qo'shish imkoniyatini tekshirish
if command -v gsettings >/dev/null 2>&1; then
    CURRENT_SOURCES=$(gsettings get org.gnome.desktop.input-sources sources 2>/dev/null || echo "")
    if [[ "$CURRENT_SOURCES" == *"yangialifbo"* ]]; then
        echo -e "${GREEN}✓ 'yangialifbo' allaqachon kirish manbalari ro'yxatida mavjud.${NC}"
    elif [ -n "$CURRENT_SOURCES" ] && [ "$CURRENT_SOURCES" != "@a(ss) []" ]; then
        # Oxiriga qo'shish
        NEW_SOURCES="${CURRENT_SOURCES%]*}, ('ibus', 'yangialifbo')]"
        gsettings set org.gnome.desktop.input-sources sources "$NEW_SOURCES" 2>/dev/null || true
        echo -e "${GREEN}✓ GNOME sozlamalariga 'Yangi Oʻzbek Alifbosi' qo'shildi.${NC}"
    fi
fi

echo -e "\n${GREEN}======================================================${NC}"
echo -e "${GREEN}  TABRIKLAYMIZ! Oʻrnatish muvaffaqiyatli yakunlandi!   ${NC}"
echo -e "${GREEN}======================================================${NC}"
echo -e "Foydalanish boʻyicha qoʻllanma:"
echo -e "  1. Klaviaturani almashtirish: ${YELLOW}Super (Win) + Boʻsh joy (Space)${NC}"
echo -e "  2. Matn yozish:"
echo -e "     - ${GREEN}sh${NC}  →  ${GREEN}ş${NC}"
echo -e "     - ${GREEN}ch${NC}  →  ${GREEN}ç${NC}"
echo -e "     - ${GREEN}o'${NC}  →  ${GREEN}ö${NC}"
echo -e "     - ${GREEN}g'${NC}  →  ${GREEN}ğ${NC}"
echo -e "  3. Vaqtincha yoqish / oʻchirish: ${YELLOW}Ctrl + Alt + Y${NC}"
echo -e "  4. Agar roʻyxatda koʻrinmasa: Sozlamalar (Settings) → Keyboard → Input Sources → Add (+)"
echo -e "     boʻlimidan 'Yangi Oʻzbek Alifbosi'ni tanlang yoki tizimdan chiqib qayta kiring (Log out/Log in)."
echo -e "======================================================\n"
