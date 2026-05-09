; clock.asm - 16-bit DOS
; int 21h / 2Ch = Get System Time -> CH=hour CL=min DH=sec

BITS 16
CPU 8086

global _clock_display

segment code

_clock_display:
    push bp
    mov  bp, sp
    push ds

    mov  ax, data_ck
    mov  ds, ax

    ; print header
    mov  ah, 09h
    mov  dx, ck_hdr
    int  21h

    ; get system time
    mov  ah, 2Ch
    int  21h
    ; CH = hours (0-23)
    ; CL = minutes (0-59)
    ; DH = seconds (0-59)

    ; save values
    mov  [ck_hour], ch
    mov  [ck_min],  cl
    mov  [ck_sec],  dh

    ; print HH
    mov  al, [ck_hour]
    call print_2digit

    mov  dl, ':'
    mov  ah, 02h
    int  21h

    ; print MM
    mov  al, [ck_min]
    call print_2digit

    mov  dl, ':'
    mov  ah, 02h
    int  21h

    ; print SS
    mov  al, [ck_sec]
    call print_2digit

    mov  ah, 09h
    mov  dx, ck_nl
    int  21h

    pop  ds
    pop  bp
    ret

; print 2-digit decimal: AL = value (0-59)
print_2digit:
    xor  ah, ah
    mov  bl, 10
    div  bl                 ; AL = tens, AH = units
    push ax

    ; tens digit
    add  al, '0'
    mov  dl, al
    mov  ah, 02h
    int  21h

    pop  ax
    ; units digit
    add  ah, '0'
    mov  dl, ah
    mov  ah, 02h
    int  21h
    ret

segment data_ck

ck_hdr  db  13,10,"System Clock",13,10,"Time: $"
ck_nl   db  13,10,13,10,"$"
ck_hour db  0
ck_min  db  0
ck_sec  db  0
