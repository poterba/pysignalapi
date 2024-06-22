name: Lint

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v3
      with:
        python-version: '3.x'
    - uses: rickstaa/action-black@v1
      with:
        black_args: ". --check"
