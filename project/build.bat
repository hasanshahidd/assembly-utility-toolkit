@echo off
REM build.bat - full paths, no PATH variable needed

SET NASM=C:\Users\dell\AppData\Local\bin\NASM\nasm.exe
SET ALINK=C:\Assembly\ALINK.EXE

echo.
echo  === Assembling files with NASM ===
echo.

echo [1/5] main.asm...
"%NASM%" -f obj main.asm -o main.obj
if errorlevel 1 goto error

echo [2/5] fileview.asm...
"%NASM%" -f obj fileview.asm -o fileview.obj
if errorlevel 1 goto error

echo [3/5] converter.asm...
"%NASM%" -f obj converter.asm -o converter.obj
if errorlevel 1 goto error

echo [4/5] clock.asm...
"%NASM%" -f obj clock.asm -o clock.obj
if errorlevel 1 goto error

echo [5/5] encrypt.asm...
"%NASM%" -f obj encrypt.asm -o encrypt.obj
if errorlevel 1 goto error

echo.
echo  === Linking with ALINK ===
echo.

REM delete old exe if exists
if exist toolkit.exe del toolkit.exe

"%ALINK%" -oPE main.obj fileview.obj converter.obj clock.obj encrypt.obj toolkit.exe
if errorlevel 1 goto error2

echo.
echo  BUILD SUCCESS!
echo  Run: toolkit.exe
goto end

:error
echo.
echo  BUILD FAILED - Assembly error!
exit /b 1

:error2
echo.
echo  Trying alternate ALINK syntax...
"%ALINK%" main.obj fileview.obj converter.obj clock.obj encrypt.obj -o toolkit.exe
if errorlevel 1 goto error3
echo.
echo  BUILD SUCCESS!
echo  Run: toolkit.exe
goto end

:error3
echo.
echo  BUILD FAILED - Link error!
exit /b 1

:end