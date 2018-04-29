#!/bin/bash
. venv/bin/activate
. FineChain/ServerUtils/update.sh
. FineChain/Blockchain/update.sh
. FineChain/FineChainAPI/update.sh
touch finechain.wsgi
