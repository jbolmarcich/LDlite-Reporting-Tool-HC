pip install tk
pip install psycopg2
pip install datetime
pip install pyinstaller
pyinstaller --onefile --windowed LDliteSingleSelect.py -n LDliteSingleSelect --distpath %cd% --workpath exe_build --noconfirm
del LDliteSingleSelect.spec
rmdir /Q /S exe_build
pause
