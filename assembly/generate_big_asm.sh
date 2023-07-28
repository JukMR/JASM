#!/bin/bash

set -eu

objdump -d /bin/ls > ls_asm.s
