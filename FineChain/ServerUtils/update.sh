#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
echo $DIR
pip uninstall -y ServerUtils
pip install $DIR
