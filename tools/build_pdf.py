"""
Build the Assembly Utility Toolkit project report PDF.
Humanized prose, screenshots embedded, GitHub link pinned at the top.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(r"C:\Users\HP\Downloads\assembly-utility-toolkit")
SHOTS = ROOT / "screenshots"
OUT = Path(r"C:\Users\HP\Downloads\Assembly_Utility_Toolkit_Report.pdf")
GH_URL = "https://github.com/hasanshahidd/assembly-utility-toolkit"

# ---------- Colors ----------
NAVY = colors.HexColor("#0b3d91")
ACCENT = colors.HexColor("#1f6feb")
SOFT = colors.HexColor("#f1f6ff")
INK = colors.HexColor("#16161d")
MUTED = colors.HexColor("#5b6472")
RULE = colors.HexColor("#d0d7de")
TABLE_HEAD = colors.HexColor("#0b3d91")
TABLE_HEAD_FG = colors.white
TABLE_ROW_ALT = colors.HexColor("#f6f8fa")

# ---------- Styles ----------
base = getSampleStyleSheet()


def style(name, parent="BodyText", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)


s_title = style("Title", parent="Title", fontName="Helvetica-Bold", fontSize=26,
                leading=30, textColor=NAVY, alignment=TA_CENTER, spaceAfter=4)
s_subtitle = style("Subtitle", fontName="Helvetica", fontSize=13, leading=16,
                   textColor=MUTED, alignment=TA_CENTER, spaceAfter=14)
s_github = style("GitHub", fontName="Helvetica-Bold", fontSize=11.5, leading=16,
                 textColor=ACCENT, alignment=TA_CENTER, spaceAfter=18)
s_h1 = style("H1", fontName="Helvetica-Bold", fontSize=17, leading=22,
             textColor=NAVY, spaceBefore=18, spaceAfter=8)
s_h2 = style("H2", fontName="Helvetica-Bold", fontSize=13.5, leading=18,
             textColor=INK, spaceBefore=12, spaceAfter=6)
s_body = style("Body", fontName="Helvetica", fontSize=11, leading=16,
               textColor=INK, alignment=TA_JUSTIFY, spaceAfter=8)
s_lead = style("Lead", fontName="Helvetica", fontSize=11.5, leading=17,
               textColor=INK, alignment=TA_JUSTIFY, spaceAfter=10)
s_caption = style("Caption", fontName="Helvetica-Oblique", fontSize=9.5,
                  leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=12)
s_code = style("Code", fontName="Courier", fontSize=9.5, leading=12.5,
               textColor=INK, leftIndent=8, spaceAfter=8)
s_bullet = style("Bullet", fontName="Helvetica", fontSize=11, leading=16,
                 textColor=INK, leftIndent=14, bulletIndent=2, spaceAfter=4)

# ---------- Page template with header ----------


def on_page(canvas, doc):
    canvas.saveState()
    # Top GitHub bar pinned on every page
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 1.05 * cm, w, 1.05 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.4 * cm, h - 0.68 * cm, "Project Repository")
    canvas.setFont("Helvetica", 9.5)
    canvas.drawRightString(w - 1.4 * cm, h - 0.68 * cm, GH_URL)
    canvas.linkURL(GH_URL, (1.4 * cm, h - 1.0 * cm, w - 1.4 * cm, h - 0.35 * cm),
                   relative=0, thickness=0)
    # Footer
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(1.4 * cm, 0.8 * cm,
                      "COAL Project  -  Assembly Utility Toolkit")
    canvas.drawRightString(w - 1.4 * cm, 0.8 * cm, f"Page {doc.page}")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.3)
    canvas.line(1.4 * cm, 1.05 * cm, w - 1.4 * cm, 1.05 * cm)
    canvas.restoreState()


def build_doc():
    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.5 * cm,
        title="Assembly Utility Toolkit - COAL Project Report",
        author="Sara Hanif & Hassan Shahid",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height - 0.4 * cm, id="body")
    doc.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=on_page))
    return doc


# ---------- Helpers ----------
def table(data, col_widths, header=True, zebra=True):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    cmds = [
        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, RULE),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ]
    if header:
        cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
            ("TEXTCOLOR", (0, 0), (-1, 0), TABLE_HEAD_FG),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10.5),
        ]
    if zebra:
        for i in range(1 if header else 0, len(data)):
            if (i - (1 if header else 0)) % 2 == 1:
                cmds.append(("BACKGROUND", (0, i), (-1, i), TABLE_ROW_ALT))
    t.setStyle(TableStyle(cmds))
    return t


def figure(path, caption, width=15 * cm):
    img = Image(str(path))
    iw, ih = img.imageWidth, img.imageHeight
    scale = width / iw
    img.drawWidth = width
    img.drawHeight = ih * scale
    return KeepTogether([img, Spacer(1, 4), Paragraph(caption, s_caption)])


def bullets(items):
    return [Paragraph(f"&bull;&nbsp;&nbsp;{t}", s_bullet) for t in items]


# ---------- Story ----------
story = []

# Cover
story.append(Spacer(1, 1.4 * cm))
story.append(Paragraph("Assembly Utility Toolkit", s_title))
story.append(Paragraph(
    "A four-in-one menu driven program written in 16-bit x86 assembly",
    s_subtitle))
story.append(Paragraph(f'<a href="{GH_URL}" color="#1f6feb"><b>{GH_URL}</b></a>',
                       s_github))

# Quick fact card
fact_data = [
    ["Course", "Computer Organization & Assembly Language (COAL)"],
    ["Language", "x86 Assembly (NASM syntax), targeting 16-bit 8086"],
    ["Toolchain", "NASM 2.x + ALINK v1.6"],
    ["Runtime", "DOSBox 0.74 on Windows 11"],
    ["Lines of code", "Around 550 across five .asm files"],
    ["Modules", "File viewer, number converter, system clock, XOR cipher"],
]
story.append(table(fact_data, [4.5 * cm, 11.5 * cm], header=False))
story.append(Spacer(1, 0.6 * cm))

team = [
    ["Member", "Roll Number", "Role"],
    ["Sara Hanif", "082", "Modules: clock, number converter, encryption"],
    ["Hassan Shahid", "056", "Modules: file viewer, main menu, build script"],
]
story.append(Paragraph("Team", s_h2))
story.append(table(team, [4.5 * cm, 3 * cm, 8.5 * cm]))

story.append(PageBreak())

# What is this project
story.append(Paragraph("What this project is", s_h1))
story.append(Paragraph(
    "This is a small command line program for DOS, written from scratch in "
    "assembly language. It pulls up a menu, you press a number, and one of "
    "four little utilities runs. There is no C, no standard library, no "
    "high level helper of any kind. Everything happens through CPU "
    "instructions and DOS interrupts.",
    s_lead))
story.append(Paragraph(
    "The idea was to take a handful of independent assembly programs we wrote "
    "during the semester and stitch them into one polished tool. The result "
    "is five separate source files that get assembled into object files "
    "and then linked together into a single executable called "
    "<b>toolkit.exe</b>. Each module lives in its own file with its own "
    "code and data segments, which keeps the project tidy and makes it "
    "easy to keep working on one piece without touching the others.",
    s_lead))

story.append(Paragraph("The four utilities at a glance", s_h2))
modules_tbl = [
    ["Key", "Module", "What it does"],
    ["1", "File Viewer", "Asks for a filename, opens the file with int 21h/3Dh, "
                          "reads 128 bytes at a time and prints them to the screen."],
    ["2", "Number Converter", "Reads a decimal number up to 65535, then prints "
                                "the same value in hexadecimal and 16-bit binary."],
    ["3", "System Clock", "Calls DOS int 21h/2Ch, picks up hours, minutes, and "
                           "seconds out of CH, CL, and DH, prints HH:MM:SS."],
    ["4", "XOR Encryption", "Takes a short message and a numeric key, XORs each "
                              "byte, prints the cipher in hex, then decrypts back."],
    ["5", "Exit", "Returns control to the DOS prompt with int 21h/4C00h."],
]
story.append(table(modules_tbl, [1.2 * cm, 3.6 * cm, 11.2 * cm]))

# Screenshots section -- pages 2 and 3
story.append(PageBreak())
story.append(Paragraph("The toolkit in action", s_h1))
story.append(Paragraph(
    "All screenshots were captured live while the program was running inside "
    "DOSBox. Mount the project folder, switch to it, and run "
    "<b>toolkit.exe</b>. The first thing you see is the familiar blue DOSBox "
    "banner, followed by our menu.",
    s_body))

story.append(figure(SHOTS / "01_dosbox_launch.png",
                    "Starting DOSBox, mounting the C drive to our project folder, "
                    "and launching toolkit.exe."))

story.append(figure(SHOTS / "02_main_menu.png",
                    "The main menu, drawn entirely with int 21h/09h string prints. "
                    "A single keypress chooses a module."))

story.append(PageBreak())

story.append(Paragraph("File Viewer", s_h2))
story.append(Paragraph(
    "We tested the file viewer by asking it to show <b>clock.asm</b>, one of "
    "the other module sources. It asks for a filename, opens the file in "
    "read-only mode, and streams the contents to the screen 128 bytes at a "
    "time until it sees end of file.",
    s_body))
story.append(figure(SHOTS / "03_file_viewer_prompt.png",
                    "The viewer prompts for a filename."))
story.append(figure(SHOTS / "04_file_viewer_output.png",
                    "Tail end of clock.asm rendered on screen, followed by an "
                    "End of File marker, then back to the main menu."))

story.append(PageBreak())

story.append(Paragraph("Number Converter", s_h2))
story.append(Paragraph(
    "The converter accepts any decimal value from 0 up to 65535 (the maximum "
    "a 16-bit register can hold). It builds the value by parsing one digit "
    "at a time, multiplying the running total by ten. The hex output comes "
    "from shifting right by 12, 8, 4, and 0 bits and masking the low nibble. "
    "The binary output walks the 8000h mask from bit 15 down to bit 0.",
    s_body))
story.append(figure(SHOTS / "05_number_converter.png",
                    "Entering 45454 and getting back the matching hex and binary."))

story.append(Paragraph("System Clock", s_h2))
story.append(Paragraph(
    "Reading the time on DOS is delightfully simple. One interrupt call "
    "returns the hour, minute, and second in separate CPU registers. The "
    "module formats each one as two decimal digits with a quick divide by "
    "ten, and prints them with colons in between.",
    s_body))
story.append(figure(SHOTS / "06_system_clock.png",
                    "The current system time, printed as HH:MM:SS."))

story.append(PageBreak())

story.append(Paragraph("XOR Encryption", s_h2))
story.append(Paragraph(
    "This module shows the classic property of the XOR cipher: encrypting "
    "and decrypting use the exact same operation. The user types a short "
    "message and a numeric key. Every byte of the message is XORed with the "
    "key byte, the cipher is printed as hex, and then the same XOR is "
    "applied again to recover the original text. It is not secure "
    "encryption, but it is the right size for a teaching example.",
    s_body))
story.append(figure(SHOTS / "07_xor_encryption.png",
                    "Encrypting the message dfgtgf with key 333, then a graceful "
                    "exit back to the DOS prompt."))

# Build / Run instructions
story.append(PageBreak())
story.append(Paragraph("How to build and run it", s_h1))
story.append(Paragraph(
    "You only need three things on your machine: NASM (the assembler), "
    "ALINK (the linker), and DOSBox (so a 16-bit program can actually run "
    "on modern 64-bit Windows).",
    s_body))

story.append(Paragraph("Prerequisites", s_h2))
story.extend(bullets([
    "NASM, available from <i>nasm.us</i>.",
    "ALINK v1.6 linker. We keep it at <font face='Courier'>C:\\Assembly\\ALINK.EXE</font>.",
    "DOSBox, available from <i>dosbox.com</i>.",
]))

story.append(Paragraph("Building with the helper script", s_h2))
story.append(Paragraph(
    "The repository contains a <b>build.bat</b> that handles both steps "
    "in one go. Open a Windows command prompt and run:",
    s_body))
story.append(Paragraph(
    "cd C:\\Assembly\\project<br/>build.bat",
    s_code))
story.append(Paragraph(
    "On success the script prints <b>BUILD SUCCESS!</b> and leaves a fresh "
    "<b>toolkit.exe</b> beside the source files.",
    s_body))

story.append(Paragraph("Building by hand", s_h2))
story.append(Paragraph(
    "nasm -f obj main.asm      -o main.obj<br/>"
    "nasm -f obj fileview.asm  -o fileview.obj<br/>"
    "nasm -f obj converter.asm -o converter.obj<br/>"
    "nasm -f obj clock.asm     -o clock.obj<br/>"
    "nasm -f obj encrypt.asm   -o encrypt.obj<br/>"
    "alink -oPE main.obj fileview.obj converter.obj clock.obj encrypt.obj toolkit.exe",
    s_code))

story.append(Paragraph("Running it in DOSBox", s_h2))
story.append(Paragraph(
    "mount c c:\\Assembly<br/>"
    "c:<br/>"
    "cd project<br/>"
    "toolkit.exe",
    s_code))

# How the code is organised
story.append(PageBreak())
story.append(Paragraph("How the code is organised", s_h1))
story.append(Paragraph(
    "The project is split across five short assembly files. <b>main.asm</b> "
    "is the entry point and only knows about the menu and the four module "
    "functions. The four module files each export exactly one global "
    "symbol that the main loop calls. ALINK is responsible for stitching "
    "the five object files together and resolving those symbols.",
    s_body))

files_tbl = [
    ["File", "Type", "Role"],
    ["main.asm", ".asm", "Sets up segments, draws the menu, reads one key, "
                          "dispatches to the chosen module."],
    ["fileview.asm", ".asm", "Module 1. Opens, reads, and prints a file."],
    ["converter.asm", ".asm", "Module 2. Decimal to hex and binary."],
    ["clock.asm", ".asm", "Module 3. Reads the system clock and prints it."],
    ["encrypt.asm", ".asm", "Module 4. XOR encryption and decryption."],
    ["build.bat", ".bat", "Assembles everything and links it in one command."],
    ["toolkit.exe", ".exe", "The final executable that you actually run."],
]
story.append(table(files_tbl, [3.5 * cm, 1.6 * cm, 10.9 * cm]))

# Tech details
story.append(Paragraph("DOS interrupts we used", s_h1))
story.append(Paragraph(
    "Everything visible on the screen, every byte read from disk, and every "
    "system fact we know comes from a DOS interrupt. Here is the full "
    "catalogue used by the four modules.",
    s_body))
ints_tbl = [
    ["Call", "AH", "What it does", "Used by"],
    ["int 21h", "02h", "Print one character (DL holds it)", "fileview, clock, encrypt"],
    ["int 21h", "08h", "Read a single key without echoing it", "main menu"],
    ["int 21h", "09h", "Print a $-terminated string", "every module"],
    ["int 21h", "0Ah", "Buffered keyboard input (a whole line)", "fileview, encrypt"],
    ["int 21h", "2Ch", "Read the system time into CH, CL, DH", "clock"],
    ["int 21h", "3Dh", "Open a file in read-only mode", "fileview"],
    ["int 21h", "3Eh", "Close an open file handle", "fileview"],
    ["int 21h", "3Fh", "Read bytes from a file handle", "fileview"],
    ["int 21h", "4C00h", "Exit the program and return control to DOS", "main menu"],
]
story.append(table(ints_tbl, [2.2 * cm, 1.4 * cm, 7.5 * cm, 4.9 * cm]))

story.append(Paragraph("Assembly concepts the project exercises", s_h2))
concepts = [
    ["Concept", "Where it shows up"],
    ["BITS 16 and CPU 8086", "Every source file. Forces NASM to emit pure 8086 code "
                              "so the binary runs on any DOS compatible CPU."],
    ["Segmented memory", "Each module owns a code segment and a private data "
                          "segment, plus main.asm has its own stack."],
    ["global / extern", "main.asm declares extern for each module function, the "
                         "modules declare global for the same symbol."],
    ["push / pop", "Every module preserves DS, ES, and BP before doing anything "
                    "interesting, then restores them on the way out."],
    ["Local labels", "Names that begin with a dot belong only to the enclosing "
                      "function, so the same label name can be reused safely."],
    ["shr / shl by CL", "The 8086 cannot shift by an arbitrary immediate, so the "
                         "converter loads CL with the shift count first."],
    ["Carry flag (jc)", "After int 21h/3Dh, the fileview checks the carry flag to "
                         "detect file-open failures."],
    ["loop and div", "Used throughout to walk byte buffers and to split numbers "
                      "into digits for printing."],
]
story.append(table(concepts, [4.5 * cm, 11.5 * cm]))

# Closing
story.append(PageBreak())
story.append(Paragraph("Closing thoughts", s_h1))
story.append(Paragraph(
    "What we like about this project is how small it is. The whole thing "
    "fits in roughly 550 lines of assembly across five files, and yet it "
    "demonstrates almost every concept the course has covered: segments, "
    "the stack, system calls, file I/O, arithmetic, bit manipulation, "
    "loops, conditional jumps, and a tiny taste of cryptography.",
    s_lead))
story.append(Paragraph(
    "There are no shortcuts hidden anywhere. Every character you see on "
    "the screen got there because the program loaded it into DL and "
    "invoked int 21h with AH equal to 02h. Every file byte came back from "
    "a hand-written read loop. The point of the exercise was to feel what "
    "a real program looks like when there is no operating system "
    "abstraction between your code and the machine. We think this version "
    "does that.",
    s_lead))

story.append(Spacer(1, 0.6 * cm))
story.append(Paragraph("Repository", s_h2))
story.append(Paragraph(
    f'The complete source, build script, screenshots, and this report live '
    f'at <a href="{GH_URL}" color="#1f6feb"><b>{GH_URL}</b></a>. '
    f"Clone it, fork it, or just browse the code.",
    s_body))

story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("Submitted by", s_h2))
sub_tbl = [
    ["Name", "Roll Number"],
    ["Sara Hanif", "082"],
    ["Hassan Shahid", "056"],
]
story.append(table(sub_tbl, [9 * cm, 4 * cm]))


# ---------- Render ----------
doc = build_doc()
doc.build(story)
print(f"Wrote: {OUT}  ({OUT.stat().st_size} bytes)")
