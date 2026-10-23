#!/usr/bin/env bash
#
# Yangi Alifbo (Linux) — Tizimdan O'chirish Skripti
# 224.uz/alifbo loyihasi asosida
#

TARGET_HOME="${HOST_HOME:-$HOME}"
INSTALL_DIR="$TARGET_HOME/.local/share/ibus-yangialifbo"
COMPONENT_FILE="$TARGET_HOME/.local/share/ibus/component/yangialifbo.xml"

echo "Yangi Alifbo tizimdan o'chirilmoqda..."

rm -rf "$INSTALL_DIR"
rm -f "$COMPONENT_FILE"
rm -f "$HOME/.local/share/ibus/component/yangialifbo.xml"

# GNOME input-sources'dan olib tashlash
if command -v gsettings >/dev/null 2>&1; then
    CURRENT_SOURCES=$(gsettings get org.gnome.desktop.input-sources sources 2>/dev/null || echo "")
    if [[ "$CURRENT_SOURCES" == *"yangialifbo"* ]]; then
        NEW_SOURCES=$(echo "$CURRENT_SOURCES" | sed -E "s/,? *\('ibus', 'yangialifbo'\)//g" | sed -E "s/\('ibus', 'yangialifbo'\),? *//g")
        gsettings set org.gnome.desktop.input-sources sources "$NEW_SOURCES" 2>/dev/null || true
    fi
fi

ibus write-cache >/dev/null 2>&1 || true
ibus restart >/dev/null 2>&1 || true

echo "✓ Yangi Alifbo muvaffaqiyatli o'chirildi."
