#!/bin/bash

if [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
    if [ "$TRAVIS_BRANCH" = "master" ]; then
        body='{
        "request": {
          "message": "Triggered by build-qpid-proton",
          "branch":"master"
          }
        }'

        curl -s -X POST \
          -H "Content-Type: application/json" \
          -H "Accept: application/json" \
          -H "Travis-API-Version: 3" \
          -H "Authorization: token $TRAVIS_TOKEN" \
          -d "$body" \
          https://api.travis-ci.org/repo/scholzj%2Fdocker-qpid-proton/requests
    fi
fi
