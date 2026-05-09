# Coal Project: Assembly Utility Toolkit

A 16-bit DOS utility toolkit written in **x86 Assembly (NASM)** for the **Computer Organization & Assembly Language (COAL)** course. The program presents a text-mode menu and lets the user run four small utilities: a file viewer, a number-base converter, a system clock, and an XOR encryption tool.

The whole project is hand-written 8086 assembly using `int 21h` (DOS) services. No C, no libraries.

## Features

* **File Viewer.** Prompts for a filename, opens it, and prints its contents to the screen.
* **Number Converter.** Reads a decimal number (0 to 65535) and prints it in hexadecimal and binary (4-bit grouped).
* **System Clock.** Reads the current system time via `int 21h / 2Ch` and prints it as `HH:MM:SS`.
* **XOR Encryption.** Takes a message and a numeric key, performs an XOR cipher, prints the encrypted hex bytes, then decrypts back to the original message.
* **Exit.** Returns control to DOS.

## Project Structure

```
project/
  main.asm         Menu / dispatcher (entry point _main)
  fileview.asm     Module 1, file viewer (_file_viewer)
  converter.asm    Module 2, decimal to hex / binary (_converter)
  clock.asm        Module 3, system clock (_clock_display)
  encrypt.asm      Module 4, XOR encryption (_encrypt_menu)
  build.bat        One-click build script for Windows
  toolkit.exe      Final linked executable (after building)
```

Each module is a separate `.asm` file with its own `code` and `data` segments and exposes a single `global _xxx` symbol that `main.asm` calls.

## How It Works (High Level)

* `main.asm` sets up `DS`, `ES`, and a private 256-byte stack, then prints a banner and waits for a key (`int 21h / AH=08h`).
* Based on the key (`'1'` to `'5'`), it `call`s the appropriate module's exported symbol.
* After each module returns, control loops back to the menu.
* All five `.obj` files are linked together with **ALINK** to produce a single `toolkit.exe`.

DOS interrupts used:

* `int 21h / 02h`: Print one character (DL = char)
* `int 21h / 08h`: Read one keystroke, no echo
* `int 21h / 09h`: Print `$`-terminated string
* `int 21h / 0Ah`: Buffered keyboard input
* `int 21h / 2Ch`: Get system time (CH=hour, CL=min, DH=sec)
* `int 21h / 3Dh`: Open file (read only)
* `int 21h / 3Eh`: Close file handle
* `int 21h / 3Fh`: Read from file handle
* `int 21h / 4C00h`: Terminate program, return exit code

## Requirements

You need a 16-bit assembly toolchain. The project was built and tested on Windows with:

* **NASM** (Netwide Assembler), generates `obj` files. Download from [https://www.nasm.us/](https://www.nasm.us/)
* **ALINK**, a small 16-bit linker that produces DOS / PE executables. Download from [http://alink.sourceforge.net/](http://alink.sourceforge.net/)
* **DOSBox** (optional, recommended for running), needed on modern Windows because 64-bit Windows cannot natively run 16-bit DOS executables. Download from [https://www.dosbox.com/](https://www.dosbox.com/)

The included `build.bat` assumes the following paths. **Edit it to match your machine** before running:

```
SET NASM=C:\Users\dell\AppData\Local\bin\NASM\nasm.exe
SET ALINK=C:\Assembly\ALINK.EXE
```

## Build & Run

### Option A: One-click build (Windows)

```bat
cd project
build.bat
```

If everything is set up correctly, you'll see `BUILD SUCCESS!` and a fresh `toolkit.exe` in the `project/` folder.

### Option B: Manual build

```bat
cd project
nasm -f obj main.asm      -o main.obj
nasm -f obj fileview.asm  -o fileview.obj
nasm -f obj converter.asm -o converter.obj
nasm -f obj clock.asm     -o clock.obj
nasm -f obj encrypt.asm   -o encrypt.obj
alink -oPE main.obj fileview.obj converter.obj clock.obj encrypt.obj toolkit.exe
```

### Running

On modern 64-bit Windows, native execution of 16-bit DOS programs is not supported. Use **DOSBox**:

```
1. Open DOSBox
2. mount c c:\Users\<you>\Downloads\coal\project
3. c:
4. toolkit.exe
```

Alternatively, on 32-bit Windows or inside Windows XP, you can run `toolkit.exe` directly from the command prompt.

## Sample Session

```
+================================+
|  Assembly Utility Toolkit      |
|                                |
|  1.  File Viewer               |
|  2.  Number Converter          |
|  3.  System Clock              |
|  4.  XOR Encryption            |
|  5.  Exit                      |
+================================+
Choice: 2

Enter decimal (0 to 65535): 255

Hex: 0x00FF
Bin: 0b 0000 0000 1111 1111
```

## Notes & Limitations

* Targets the **8086** instruction set only (`CPU 8086`) so it runs on every DOS compatible CPU.
* The number converter accepts 0 to 65535 (16-bit unsigned). Larger inputs will overflow.
* The XOR cipher is for **educational use only**. It is not cryptographically secure.
* The file viewer reads in 128-byte chunks and prints everything as ASCII; binary files will show garbage.

## Course Context

Built as a course project for **Computer Organization & Assembly Language (COAL)**. The aim was to combine multiple small assembly programs into one menu-driven application demonstrating segmented memory, inter-module linking, DOS interrupts, file I/O, arithmetic, time, and basic cryptography.

## License

This repository is published for educational purposes. Feel free to read, fork, and learn from it.
