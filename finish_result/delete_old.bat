forfiles /p %~dp0 /s /m *.jpeg /d -7 /c "cmd /c del @path"
forfiles /p %~dp0 /s /m *.png /d -7 /c "cmd /c del @path"