@echo off
REM restore-clean.cmd — Restore HTML files from clean commit, bypassing PowerShell encoding corruption
SET REPO=C:\Users\SAMPC\repos\dogeking-us
SET COMMIT=c1c4b6b
SET TEMPDIR=%TEMP%\dogeking-restore
SET COUNT=0
SET ERRORCOUNT=0

IF NOT EXIST "%TEMPDIR%" MKDIR "%TEMPDIR%"

REM Get list of HTML files in the clean commit
git -C "%REPO%" ls-tree -r --name-only %COMMIT% > "%TEMPDIR%\files.txt"
if %ERRORLEVEL% NEQ 0 (
    echo FAILED: Could not list files from commit %COMMIT%
    echo Check that the commit exists and the repo path is correct.
    pause
    exit /b 1
)

REM Count total files
for /f %%i in ('findstr /i "\.html$" "%TEMPDIR%\files.txt" ^| find /c /v ""') do set TOTAL=%%i
echo Found %TOTAL% HTML files to restore

REM Restore each file
for /f "delims=" %%f in ('type "%TEMPDIR%\files.txt"') do (
    SETLOCAL ENABLEDELAYEDEXPANSION
    set "FILE=%%f"
    if /i "!FILE:~-5!"==".html" (
        git -C "%REPO%" show %COMMIT%:"%%f" > "%TEMPDIR%\restore.tmp"
        if !ERRORLEVEL! EQU 0 (
            copy /y "%TEMPDIR%\restore.tmp" "%REPO%\%%f" >nul
            set /a COUNT+=1
            if !COUNT! LEQ 5 echo   RESTORED: %%f
        ) else (
            echo   FAILED: %%f
            set /a ERRORCOUNT+=1
        )
    )
    ENDLOCAL
)

echo.
echo === RESULTS ===
echo Restored: %COUNT%
echo Errors: %ERRORCOUNT%

REM Clean up
del /q "%TEMPDIR%\files.txt" "%TEMPDIR%\restore.tmp" 2>nul
