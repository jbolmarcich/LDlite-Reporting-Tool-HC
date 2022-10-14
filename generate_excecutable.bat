pyinstaller LDliteSingleSelect.py -F -n LDliteSingleSelect --distpath %cd% --workpath exe_build --noconfirm
del LDliteSingleSelect.spec
rmdir /Q /S exe_build
pause
