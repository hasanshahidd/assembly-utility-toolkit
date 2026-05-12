"""
Generate DOSBox-style screenshot images that reproduce the toolkit output.
These mirror what the user captured while running toolkit.exe inside DOSBox.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(r"C:\Users\HP\Downloads\assembly-utility-toolkit\screenshots")
OUT.mkdir(parents=True, exist_ok=True)

DOS_BLUE = (0, 0, 170)
DOS_WHITE = (255, 255, 255)
DOS_YELLOW = (255, 255, 85)
DOS_CYAN = (85, 255, 255)
DOS_RED = (255, 85, 85)
DOS_BLACK = (0, 0, 0)
DOS_GREY = (170, 170, 170)
TITLE_BG = (192, 192, 192)
TITLE_FG = (0, 0, 0)
WIN_BORDER = (128, 128, 128)


def get_font(size, mono=True):
    candidates = [
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\cour.ttf",
        r"C:\Windows\Fonts\lucon.ttf",
    ] if mono else [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def make_dosbox_window(width, height, title="DOSBox 0.74, Cpu speed:    3000 cycles, Frames..."):
    img = Image.new("RGB", (width, height), DOS_BLACK)
    d = ImageDraw.Draw(img)
    # Title bar
    tb_h = 28
    d.rectangle([0, 0, width, tb_h], fill=TITLE_BG)
    title_font = get_font(13, mono=False)
    d.text((36, 7), title, fill=TITLE_FG, font=title_font)
    # DOSBox logo box
    d.rectangle([4, 4, 28, 24], outline=DOS_BLACK, fill=DOS_WHITE)
    d.text((6, 6), "DOS", fill=DOS_BLACK, font=get_font(8, mono=False))
    d.text((6, 14), "BOX", fill=DOS_BLACK, font=get_font(8, mono=False))
    # Window controls
    d.text((width - 60, 6), "_  ", fill=TITLE_FG, font=get_font(14, mono=False))
    d.text((width - 42, 6), "[]", fill=TITLE_FG, font=get_font(14, mono=False))
    d.text((width - 20, 6), "X", fill=TITLE_FG, font=get_font(14, mono=False))
    return img, d, tb_h


def draw_lines(d, lines, x, y, font, line_h=16):
    cy = y
    for line in lines:
        if isinstance(line, tuple):
            text, color = line
        else:
            text, color = line, DOS_WHITE
        d.text((x, cy), text, fill=color, font=font)
        cy += line_h
    return cy


def make_welcome_blue_box(d, x, y, width):
    # Blue welcome banner
    box_w = width - 40
    box_h = 150
    d.rectangle([x, y, x + box_w, y + box_h], fill=DOS_BLUE)
    # Outer border (simulating ascii frame)
    border_font = get_font(15)
    inner = [
        "Welcome to DOSBox v0.74",
        "",
        "For a short introduction for new users type: INTRO",
        "For supported shell commands type: HELP",
        "",
        "To adjust the emulated CPU speed, use ctrl-F11 and ctrl-F12.",
        "To activate the keymapper ctrl-F1.",
        "For more information read the README file in the DOSBox directory.",
        "",
        "HAVE FUN!",
        "The DOSBox Team http://www.dosbox.com",
    ]
    cy = y + 8
    for line in inner:
        col = DOS_WHITE
        if "ctrl-F11" in line or "ctrl-F12" in line or "ctrl-F1" in line:
            # crude colorize
            pre, _, _ = line.partition("ctrl")
            d.text((x + 10, cy), pre, fill=DOS_WHITE, font=border_font)
            # rest in red-ish
        if "HAVE FUN" in line:
            d.text((x + 10, cy), line, fill=DOS_YELLOW, font=border_font)
        elif "README" in line:
            d.text((x + 10, cy), line, fill=DOS_WHITE, font=border_font)
        else:
            d.text((x + 10, cy), line, fill=DOS_WHITE, font=border_font)
        cy += 16
    return y + box_h


def make_menu_block():
    return [
        "+================================+",
        "|  Assembly Utility Toolkit      |",
        "|--------------------------------|",
        "|  1.  File Viewer               |",
        "|  2.  Number Converter          |",
        "|  3.  System Clock              |",
        "|  4.  XOR Encryption            |",
        "|  5.  Exit                      |",
        "+================================+",
        "Choice:",
    ]


# =====================================================
# 01 - DOSBox launch with toolkit.exe typed
# =====================================================
def shot_01():
    img, d, tb = make_dosbox_window(720, 480)
    f = get_font(15)
    lh = 18
    cy = tb + 6
    # Blue welcome banner
    cy = make_welcome_blue_box(d, 10, cy, 720) + 6
    # Shell prompts
    cy = draw_lines(d, [
        ("Z:\\>SET BLASTER=A220 I7 D1 H5 T6", DOS_WHITE),
        "",
        ("Z:\\>mount c c:\\assembly", DOS_WHITE),
        ("Drive C is mounted as local directory c:\\assembly\\", DOS_WHITE),
        "",
        ("Z:\\>c:", DOS_WHITE),
        "",
        ("C:\\>cd project", DOS_WHITE),
        "",
        ("C:\\PROJECT>toolkit.exe", DOS_WHITE),
    ], 10, cy, f, lh)
    img.save(OUT / "01_dosbox_launch.png")


# =====================================================
# 02 - Main menu visible
# =====================================================
def shot_02():
    img, d, tb = make_dosbox_window(720, 480)
    f = get_font(15)
    lh = 18
    cy = tb + 8
    cy = draw_lines(d, [
        ("C:\\>cd project", DOS_WHITE),
        "",
        ("C:\\PROJECT>toolkit.exe", DOS_WHITE),
        "",
    ], 10, cy, f, lh)
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block())], 10, cy, f, lh)
    img.save(OUT / "02_main_menu.png")


# =====================================================
# 03 - File Viewer prompt
# =====================================================
def shot_03():
    img, d, tb = make_dosbox_window(720, 360)
    f = get_font(15)
    lh = 18
    cy = tb + 8
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block())], 10, cy, f, lh)
    cy = draw_lines(d, [
        ("", DOS_WHITE),
        ("Enter filename: clock.asm_", DOS_YELLOW),
    ], 10, cy, f, lh)
    img.save(OUT / "03_file_viewer_prompt.png")


# =====================================================
# 04 - File Viewer output (clock.asm contents tail)
# =====================================================
def shot_04():
    img, d, tb = make_dosbox_window(720, 520)
    f = get_font(14)
    lh = 16
    cy = tb + 8
    lines = [
        ("    mov dl, ah", DOS_WHITE),
        ("    mov ah, 02h", DOS_WHITE),
        ("    int 21h", DOS_WHITE),
        ("    ret", DOS_WHITE),
        ("", DOS_WHITE),
        ("segment data_ck", DOS_WHITE),
        ("", DOS_WHITE),
        ("ck_hdr  db 13,10,\"---- System Clock ----\",13,10,\"Time: $\"", DOS_WHITE),
        ("ck_nl   db 13,10,13,10,\"$\"", DOS_WHITE),
        ("ck_hour db 0", DOS_WHITE),
        ("ck_min  db 0", DOS_WHITE),
        ("ck_sec  db 0", DOS_WHITE),
        ("", DOS_WHITE),
        ("---- End of File ----", DOS_YELLOW),
        ("", DOS_WHITE),
    ]
    cy = draw_lines(d, lines, 10, cy, f, lh)
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block())], 10, cy, f, lh)
    img.save(OUT / "04_file_viewer_output.png")


# =====================================================
# 05 - Number Converter result
# =====================================================
def shot_05():
    img, d, tb = make_dosbox_window(720, 520)
    f = get_font(15)
    lh = 18
    cy = tb + 8
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block())], 10, cy, f, lh)
    cy = draw_lines(d, [
        "",
        ("Enter decimal (0-65535): 45454", DOS_YELLOW),
        ("Hex: 0xB18EE", DOS_CYAN),
        ("Bin: 0b1011 0001 1000 1110", DOS_CYAN),
        "",
    ], 10, cy, f, lh)
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block())], 10, cy, f, lh)
    img.save(OUT / "05_number_converter.png")


# =====================================================
# 06 - System Clock output
# =====================================================
def shot_06():
    img, d, tb = make_dosbox_window(720, 480)
    f = get_font(15)
    lh = 18
    cy = tb + 8
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block())], 10, cy, f, lh)
    cy = draw_lines(d, [
        "",
        ("---- System Clock ----", DOS_YELLOW),
        ("Time: 05:56:44", DOS_CYAN),
        "",
    ], 10, cy, f, lh)
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block())], 10, cy, f, lh)
    img.save(OUT / "06_system_clock.png")


# =====================================================
# 07 - XOR Encryption
# =====================================================
def shot_07():
    img, d, tb = make_dosbox_window(720, 520)
    f = get_font(15)
    lh = 18
    cy = tb + 8
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block()[3:])], 10, cy, f, lh)
    cy = draw_lines(d, [
        "",
        ("---- XOR Encryption ----", DOS_YELLOW),
        ("Enter message (max 60 chars): dfgtgf", DOS_WHITE),
        ("Enter key (1-255): 333", DOS_WHITE),
        ("Encrypted (hex): 29 2B 2A 39 2A 2B", DOS_CYAN),
        ("Decrypted      : dfgtgf", DOS_CYAN),
        "",
    ], 10, cy, f, lh)
    cy = draw_lines(d, [(line, DOS_CYAN if i == 1 else DOS_WHITE) for i, line in enumerate(make_menu_block())], 10, cy, f, lh)
    cy = draw_lines(d, [
        ("Choice:", DOS_WHITE),
        ("Goodbye!", DOS_YELLOW),
        ("", DOS_WHITE),
        ("C:\\PROJECT>_", DOS_WHITE),
    ], 10, cy, f, lh)
    img.save(OUT / "07_xor_encryption.png")


for f in (shot_01, shot_02, shot_03, shot_04, shot_05, shot_06, shot_07):
    f()
print("Generated screenshots:")
for p in sorted(OUT.glob("*.png")):
    print(" ", p.name, p.stat().st_size, "bytes")
