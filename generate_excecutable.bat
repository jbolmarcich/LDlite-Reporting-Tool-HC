pip install tk
pip install psycopg2
pip install datetime
pip install pyinstaller
pip install sys
pip install os
pyinstaller LDliteSingleSelect.py -F -n LDliteSingleSelect --distpath %cd% --workpath exe_build --noconfirm
del LDliteSingleSelect.spec
rmdir /Q /S exe_build
pause
