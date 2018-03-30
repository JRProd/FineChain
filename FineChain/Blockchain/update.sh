#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
pip uninstall -y Blockchain
pip install $DIR
