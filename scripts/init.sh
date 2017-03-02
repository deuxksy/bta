#!/usr/bin/env bash

export PATH="${HOME}/.pyenv/bin:$PATH"

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
source `which activate.sh`

pyenv shell 3.5.3
pyenv virtualenvwrapper
workon bta
