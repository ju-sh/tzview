rm -rf build/ dist/ src/tzview.egg-info/

python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# Change version number in:
#  - src/tzview/app.py:__version__ = "0.1"
#  - setup.py:    version="0.1",

