#!/usr/bin/bash
VERSION=$1
sed -i "s/__version__ = .*/__version__ = '$VERSION'/g" src/yummyanime/__init__.py
sed -i "s/version = .*/version = \"$VERSION\"/g" ./pyproject.toml
sed -i "s/pkgver=.*/pkgver=$VERSION/g" ./.aur/python-yummyanime/PKGBUILD
python -m build
FILE="dist/yummyanime-$VERSION-py3-none-any.whl"
HASH=$(./_hash.py $FILE)
echo $HASH
FIRST="${HASH:0:2}"
SECOND="${HASH:2:2}"
LAST="${HASH:4:99999}"
HASHSHA256=$(sha256sum $FILE | awk '{print $1}')

LINK="https://files.pythonhosted.org/packages/$FIRST/$SECOND/$LAST/yummyanime-$VERSION-py3-none-any.whl"

sed -i "s|^source=.*|source=(\"$LINK\")|g" ./.aur/python-yummyanime/PKGBUILD
sed -i "s|sha256sums=.*|sha256sums=(\'$HASHSHA256\')|g" ./.aur/python-yummyanime/PKGBUILD
cd ./.aur/python-yummyanime && rm .SRCINFO && makepkg --printsrcinfo >> .SRCINFO && git add . && git commit -m "Version $VERSION"
cd ../../
pwd
pip install .
python ./tests/api.py
