
VERSION=$1
sed -i "s/__version__ = .*/__version__ = '$VERSION'/g" src/yummyanime/__init__.py
sed -i "s/version = .*/version = \"$VERSION\"/g" ./pyproject.toml
python3 -m twine upload dist/*
