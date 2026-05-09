; fileview.asm - 16-bit DOS
; Opens a file and prints its contents using int 21h

BITS 16
CPU 8086

global _file_viewer

segment code

_file_viewer:
    push bp
    mov  bp, sp
    push ds
    push es

    mov  ax, data_fv
    mov  ds, ax

    ; prompt for filename
    mov  ah, 09h
    mov  dx, fv_prompt
    int  21h

    ; read filename string (int 21h / 0Ah buffered input)
    mov  ah, 0Ah
    mov  dx, fv_inbuf
    int  21h

    ; null-terminate the input
    mov  bl, [fv_inbuf + 1]     ; actual chars read
    xor  bh, bh
    mov  byte [fv_inbuf + bx + 2], 0

    ; open file (int 21h / 3Dh)
    mov  ah, 3Dh
    xor  al, al                 ; read only
    mov  dx, fv_inbuf + 2       ; filename starts at offset 2
    int  21h
    jc   .open_err

    mov  [fv_handle], ax

    ; print header
    mov  ah, 09h
    mov  dx, fv_hdr
    int  21h

.read_loop:
    ; read 128 bytes at a time
    mov  ah, 3Fh
    mov  bx, [fv_handle]
    mov  cx, 128
    mov  dx, fv_rdbuf
    int  21h
    jc   .close_file
    test ax, ax
    jz   .close_file

    ; print what we read (char by char since int 21h/09 needs $)
    mov  cx, ax
    mov  si, fv_rdbuf
.print_loop:
    mov  dl, [si]
    mov  ah, 02h
    int  21h
    inc  si
    loop .print_loop
    jmp  .read_loop

.close_file:
    mov  ah, 3Eh
    mov  bx, [fv_handle]
    int  21h

    mov  ah, 09h
    mov  dx, fv_done
    int  21h
    jmp  .done

.open_err:
    mov  ah, 09h
    mov  dx, fv_err
    int  21h

.done:
    pop  es
    pop  ds
    pop  bp
    ret

segment data_fv

fv_prompt   db  13,10,"Enter filename: $"
fv_hdr      db  13,10,"File Contents",13,10,"$"
fv_err      db  13,10,"ERROR: File not found!",13,10,"$"
fv_done     db  13,10,"End of File",13,10,"$"
fv_handle   dw  0
; buffered input: [max][actual][chars...]
fv_inbuf    db  80, 0
            times 82 db 0
fv_rdbuf    times 130 db 0
