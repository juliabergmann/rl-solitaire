black .
pip install pip-tools 
pip freeze > "requirements.in" 
pip-compile -o requirements.txt requirements.in 
del .\requirements.in 
git.exe add .\requirements.txt 
git.exe commit -m "update requirements" 
