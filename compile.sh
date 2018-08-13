#!/usr/bin/env bash
rm -rf build dist nihylisim.*
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
