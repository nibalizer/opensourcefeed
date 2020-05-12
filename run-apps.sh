#!/bin/bash

echo "Starting daemons"

if [ -z $GITHUB_API_KEY ]; then
    echo "Please source config file to get secrets"
    exit 1
fi

pushd web
if [ ! -d node_modules ]; then
    echo "Please run npm install first"
    exit 1
fi

npm start > ../logs/web.log 2>&1 &

popd

pushd workers/github
if [ ! -d venv  ]; then
    echo "Please virtualenv first"
    exit 1
fi

./venv/bin/python main.py > ../../logs/worker-github.log 2>&1 &

popd
