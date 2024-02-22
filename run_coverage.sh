#!/bin/bash

coverage run -m pytest . && coverage report -m && coverage html && open htmlcov/index.html
