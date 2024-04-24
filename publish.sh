export $(cat .env | xargs)
python3 -m twine upload dist/*
cd .aur/python-yummyanime && git push origin master