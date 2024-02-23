#!/bin/bash

coverage run -m pytest . && coverage report -m && coverage html && xdg-open htmlcov/index.html
