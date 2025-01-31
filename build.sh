#!/bin/bash

# Set environment variables
export GPG_TTY=$(tty)
export PYTHONPATH=$(pwd):$PYTHONPATH

# Run your build commands
echo "GPG_TTY set to: $GPG_TTY"
echo "PYTHONPATH set to: $PYTHONPATH"
sudo systemctl start mongod