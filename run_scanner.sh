#!/bin/bash

check_python() {
    if command -v python3 &>/dev/null; then
        echo "Python3 is installed"
    else
        echo "Python3 is not installed"
        exit 1
    fi
}

check_docker() {
    if command -v docker &>/dev/null; then
        echo "Docker is installed"
    else
        echo "Docker is not installed."
        exit 1
    fi
}

install_dependencies() {
    echo "Installing Python dependencies..."
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
    else
        echo "requirements.txt not found!"
        exit 1
    fi
}

run_scanner() {
    echo "Running the NeuraScript scanner..."
    python3 src/scanner.py tests/test1.ns
}

if [ "$1" == "--docker" ]; then
    echo "Using Docker to run the scanner..."
    check_docker
    docker build -t neuroscript-scanner .
    docker run neuroscript-scanner
else
    check_python
    install_dependencies
    run_scanner
fi
