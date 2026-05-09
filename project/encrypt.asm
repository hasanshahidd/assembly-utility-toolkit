; encrypt.asm - 16-bit DOS
; XOR cipher: type message + key -> shows hex -> decrypts back

BITS 16
CPU 8086

global _encrypt_menu

segment code

_encrypt_menu:
    push bp
    mov  bp, sp
    push ds

    mov  ax, data_en
    mov  ds, ax

    ; header
    mov  ah, 09h
    mov  dx, en_hdr
    int  21h

    ; prompt for message
    mov  ah, 09h
    mov  dx, en_pmsg
    int  21h

    ; buffered input for message
    mov  ah, 0Ah
    mov  dx, en_msgbuf
    int  21h

    ; get actual length
    mov  cl, [en_msgbuf + 1]
    xor  ch, ch
    mov  [en_msglen], cx

    ; prompt for key
    mov  ah, 09h
    mov  dx, en_pkey
    int  21h

    ; read key as decimal string
    mov  ah, 0Ah
    mov  dx, en_keybuf
    int  21h

    ; parse key -> BL
    xor  ax, ax
    xor  si, si
    mov  cl, [en_keybuf + 1]
    xor  ch, ch
    test cx, cx
    jz   .key_default
.parse_key:
    mov  bl, [en_keybuf + 2 + si]
    sub  bl, '0'
    xor  bh, bh
    push cx
    push si
    mov  cx, 10
    mul  cx
    pop  si
    pop  cx
    add  ax, bx
    inc  si
    loop .parse_key
    test ax, ax
    jnz  .key_set
.key_default:
    mov  ax, 42
.key_set:
    mov  [en_key], al

    ; XOR encrypt
    mov  cx, [en_msglen]
    xor  si, si
    mov  bl, [en_key]
.xor_enc:
    test cx, cx
    jz   .xor_enc_done
    xor  byte [en_msgbuf + 2 + si], bl
    inc  si
    dec  cx
    jmp  .xor_enc
.xor_enc_done:

    ; print hex output
    mov  ah, 09h
    mov  dx, en_enc_hdr
    int  21h

    mov  cx, [en_msglen]
    xor  si, si
.hex_loop:
    test cx, cx
    jz   .hex_done

    mov  al, [en_msgbuf + 2 + si]
    mov  [en_tmpbyte], al

    ; high nibble: use CL to shift
    mov  cl, 4
    shr  al, cl                 ; 8086 safe: shift by CL
    and  al, 0Fh
    cmp  al, 9
    jle  .h1
    add  al, 7
.h1:
    add  al, '0'
    mov  dl, al
    mov  ah, 02h
    int  21h

    ; low nibble
    mov  al, [en_tmpbyte]
    and  al, 0Fh
    cmp  al, 9
    jle  .h2
    add  al, 7
.h2:
    add  al, '0'
    mov  dl, al
    mov  ah, 02h
    int  21h

    ; space
    mov  dl, ' '
    mov  ah, 02h
    int  21h

    inc  si
    mov  cx, [en_msglen]
    sub  cx, si
    jmp  .hex_loop
.hex_done:

    ; XOR decrypt
    mov  cx, [en_msglen]
    xor  si, si
    mov  bl, [en_key]
.xor_dec:
    test cx, cx
    jz   .xor_dec_done
    xor  byte [en_msgbuf + 2 + si], bl
    inc  si
    dec  cx
    jmp  .xor_dec
.xor_dec_done:

    ; print decrypted
    mov  ah, 09h
    mov  dx, en_dec_hdr
    int  21h

    mov  cx, [en_msglen]
    xor  si, si
.dec_print:
    test cx, cx
    jz   .dec_done
    mov  dl, [en_msgbuf + 2 + si]
    mov  ah, 02h
    int  21h
    inc  si
    dec  cx
    jmp  .dec_print
.dec_done:

    mov  ah, 09h
    mov  dx, en_nl
    int  21h

    pop  ds
    pop  bp
    ret

segment data_en

en_hdr      db  13,10,"XOR Encryption",13,10,"$"
en_pmsg     db  "Enter message (max 60 chars): $"
en_pkey     db  13,10,"Enter key (1-255): $"
en_enc_hdr  db  13,10,"Encrypted (hex): $"
en_dec_hdr  db  13,10,"Decrypted      : $"
en_nl       db  13,10,13,10,"$"
en_key      db  0
en_tmpbyte  db  0
en_msglen   dw  0
en_msgbuf   db  60, 0
            times 62 db 0
en_keybuf   db  5, 0
            times 7  db 0