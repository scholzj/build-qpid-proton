#!/bin/bash
#
# First argument: Autntication toke for Travic-CI
# Second argument: GitHub organization / user
# Third argument: Github repository
# Fourth argument: Name of the branch which should be triggered (by default master)
#
AUTH_TOKEN=$1
GITHUB_ORGANIZATION=$2
GITHUB_REPO=$3
if [ -z "$4" ]; then
    GITHUB_BRANCH="master"
else
    GITHUB_BRANCH=$4
fi

body="{
\"request\": {
  \"message\": \"Triggered per request from ${TRAVIS_REPO_SLUG}\",
  \"branch\": \"${GITHUB_BRANCH}\"
  }
}"

curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Travis-API-Version: 3" \
  -H "Authorization: token ${AUTH_TOKEN}" \
  -d "$body" \
  https://api.travis-ci.org/repo/${GITHUB_ORGANIZATION}%2F${GITHUB_REPO}/requests
