; converter.asm - 16-bit DOS
; Type a decimal number -> shows Hex and Binary

BITS 16
CPU 8086

global _converter

segment code

_converter:
    push bp
    mov  bp, sp
    push ds

    mov  ax, data_cv
    mov  ds, ax

    ; prompt
    mov  ah, 09h
    mov  dx, cv_prompt
    int  21h

    ; buffered input
    mov  ah, 0Ah
    mov  dx, cv_inbuf
    int  21h

    ; parse decimal -> AX
    xor  ax, ax
    xor  si, si
    mov  cl, [cv_inbuf + 1]     ; chars read
    xor  ch, ch
    test cx, cx
    jz   .show

.parse:
    mov  bl, [cv_inbuf + 2 + si]
    sub  bl, '0'
    mov  bh, 0
    push cx
    push si
    mov  cx, 10
    mul  cx
    pop  si
    pop  cx
    add  ax, bx
    inc  si
    loop .parse

.show:
    mov  [cv_number], ax

    ; print HEX label
    mov  ah, 09h
    mov  dx, cv_hex_lbl
    int  21h

    ; print 4 hex digits using shift by CL
    mov  bx, [cv_number]
    mov  cl, 12                 ; start from bits 15-12

.hex_loop:
    mov  ax, bx
    push cx
    shr  ax, cl                 ; shift right by CL
    pop  cx
    and  al, 0Fh               ; keep low nibble
    cmp  al, 9
    jle  .hex_dig
    add  al, 7                  ; A-F offset
.hex_dig:
    add  al, '0'
    mov  dl, al
    mov  ah, 02h
    int  21h
    ; next nibble: subtract 4 from CL
    cmp  cl, 4
    jl   .hex_done
    sub  cl, 4
    jmp  .hex_loop
.hex_done:
    ; print last nibble (cl=0)
    mov  ax, bx
    and  al, 0Fh
    cmp  al, 9
    jle  .last_dig
    add  al, 7
.last_dig:
    add  al, '0'
    mov  dl, al
    mov  ah, 02h
    int  21h

    ; print BINARY label
    mov  ah, 09h
    mov  dx, cv_bin_lbl
    int  21h

    mov  bx, [cv_number]
    mov  cx, 16
.bin_loop:
    ; space every 4 bits for readability
    mov  ax, cx
    and  ax, 3
    jnz  .no_sp
    cmp  cx, 16
    je   .no_sp
    mov  dl, ' '
    mov  ah, 02h
    int  21h
.no_sp:
    mov  dl, '0'
    test bx, 8000h
    jz   .print_bit
    mov  dl, '1'
.print_bit:
    mov  ah, 02h
    int  21h
    shl  bx, 1
    loop .bin_loop

    mov  ah, 09h
    mov  dx, cv_nl
    int  21h

    pop  ds
    pop  bp
    ret

segment data_cv

cv_prompt   db  13,10,"Enter decimal (0-65535): $"
cv_hex_lbl  db  13,10,"Hex: 0x","$"
cv_bin_lbl  db  13,10,"Bin: 0b","$"
cv_nl       db  13,10,13,10,"$"
cv_number   dw  0
cv_inbuf    db  8, 0
            times 10 db 0