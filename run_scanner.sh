#!/bin/bash

check_python() {
    if command -v python3 &>/dev/null; then
        echo "Python3 is installed"
    else
        echo "Python3 is not installed"
        echo "Installing Python3..."
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
        if [ $? -ne 0 ]; then
            echo "Failed to install Python3. Please install it manually."
            exit 1
        fi
    fi
}

check_docker() {
    if command -v docker &>/dev/null; then
        echo "Docker is installed"
    else
        echo "Docker is not installed. Installing Docker..."
        sudo apt-get update && sudo apt-get install -y docker.io
        if [ $? -ne 0 ]; then
            echo "Failed to install Docker. Please install it manually."
            exit 1
        fi
    fi
}

setup_virtualenv() {
    if [ -d "venv" ]; then
        echo "Virtual environment already exists. Activating..."
        source venv/bin/activate
    else
        echo "Setting up virtual environment..."
        if ! command -v python3 -m venv &>/dev/null; then
            echo "Installing venv module..."
            sudo apt-get install -y python3-venv
        fi

        # Create and activate virtual environment
        python3 -m venv venv
        source venv/bin/activate
    fi
}

install_dependencies() {
    echo "Installing Python dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        echo "requirements.txt not found!"
        exit 1
    fi
}

run_scanner() {
    echo "Running the NeuraScript scanner on all test files..."
    if [ -d "tests" ]; then
        echo "Listing contents of tests directory:"
        ls tests
    else
        echo "Tests directory not found!"
        exit 1
    fi

    for test_file in tests/*.ns; do
        if [ ! -f "$test_file" ]; then
            echo "No .ns files found in the tests directory."
            exit 1
        fi

        echo -e "\n\n\nProcessing $test_file..."
        output=$(python3 src/scanner.py "$test_file")
        echo "$output"
        echo
        echo
    done
}

run_scanner_and_parser() {
    echo "Running the NeuraScript scanner and parser on all test files..."
    if [ -d "tests" ]; then
        echo "Listing contents of tests directory:"
        ls tests
    else
        echo "Tests directory not found!"
        exit 1
    fi

    for test_file in tests/*.ns; do
        if [ ! -f "$test_file" ]; then
            echo "No .ns files found in the tests directory."
            exit 1
        fi

        echo -e "\n\n\nProcessing $test_file..."
        output=$(python3 src/scanner.py "$test_file")
        echo "$output"
        echo
        echo

        echo -e "\n\n\nProcessing tokens with Parser..."
        parser_output=$(python3 src/parser.py tokens.txt)
        echo "$parser_output"
        echo
        echo
    done
}


if [ "$1" == "--docker" ]; then
    echo "Using Docker to run the scanner..."
    check_docker
    docker build -t neuroscript-scanner .
    docker run neuroscript-scanner
else
    check_python
    setup_virtualenv
    install_dependencies
    run_scanner_and_parser
fi