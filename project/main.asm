; UTILITY TOOLKIT - main.asm
; 16-bit DOS, NASM, linked with ALINK
;
; BUILD (in DOSBox or Command Prompt):
;   nasm -f obj main.asm      -o main.obj
;   nasm -f obj fileview.asm  -o fileview.obj
;   nasm -f obj converter.asm -o converter.obj
;   nasm -f obj clock.asm     -o clock.obj
;   nasm -f obj encrypt.asm   -o encrypt.obj
;   alink main.obj fileview.obj converter.obj clock.obj encrypt.obj -oEXE toolkit.exe
;
; RUN: toolkit.exe

BITS 16
CPU 8086

global _main
extern _file_viewer
extern _converter
extern _clock_display
extern _encrypt_menu

segment code

_main:
    ; setup DS = our data segment
    mov  ax, data
    mov  ds, ax
    mov  es, ax

    ; setup stack
    mov  ax, stack
    mov  ss, ax
    mov  sp, stacktop

.menu_loop:
    ; print banner
    mov  ah, 09h
    mov  dx, banner
    int  21h

    ; read single key (no echo)
    mov  ah, 08h
    int  21h                    ; AL = key pressed

    cmp  al, '1'
    je   .do_file
    cmp  al, '2'
    je   .do_conv
    cmp  al, '3'
    je   .do_clock
    cmp  al, '4'
    je   .do_enc
    cmp  al, '5'
    je   .do_exit
    cmp  al, 13
    je   .menu_loop

    ; invalid key - print message
    mov  ah, 09h
    mov  dx, bad_msg
    int  21h
    jmp  .menu_loop

.do_file:
    call _file_viewer
    jmp  .menu_loop

.do_conv:
    call _converter
    jmp  .menu_loop

.do_clock:
    call _clock_display
    jmp  .menu_loop

.do_enc:
    call _encrypt_menu
    jmp  .menu_loop

.do_exit:
    mov  ah, 09h
    mov  dx, bye_msg
    int  21h
    mov  ax, 4C00h              ; DOS exit
    int  21h

segment data

banner  db  13,10
        db  "+================================+",13,10
        db  "|  Assembly Utility Toolkit      |",13,10
        db  "|--------------------------------|",13,10
        db  "|  1.  File Viewer               |",13,10
        db  "|  2.  Number Converter          |",13,10
        db  "|  3.  System Clock              |",13,10
        db  "|  4.  XOR Encryption            |",13,10
        db  "|  5.  Exit                      |",13,10
        db  "+================================+",13,10
        db  "Choice: $"

bad_msg db  13,10,"Invalid key! Try 1-5.",13,10,"$"
bye_msg db  13,10,"Goodbye!",13,10,"$"

segment stack stack
    resb 256
stacktop:
