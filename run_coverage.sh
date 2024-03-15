#!/bin/bash

coverage run -m pytest -vv . && coverage report -m && coverage html && xdg-open htmlcov/index.html
