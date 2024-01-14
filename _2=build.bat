REM del dist\ /q /s
rd dist\ /q /s

REM python setup.py sdist bdist_wheel
python setup.py sdist
pause
