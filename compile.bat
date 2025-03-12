@echo off

echo Building "setup.py"
python setup.py build

echo Building Packages
python -m build

echo Local Install
pip install .

echo Uploading to TestPyPi
twine upload --repository testpypi dist/*

echo Done.