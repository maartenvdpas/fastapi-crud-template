#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    VENV_ACTIVATE_PATH="$SCRIPT_DIR/.venv/Scripts/activate"
    PYTHON_EXECUTABLE=python
else
    VENV_ACTIVATE_PATH="$SCRIPT_DIR/.venv/bin/activate"
    PYTHON_EXECUTABLE=python3
fi

generate_default_env() {
    if [[ ! -f "$SCRIPT_DIR/.env" ]]; then
        cat > .env << EOF
DATABASE_USER=postgres
DATABASE_PASSWORD=CXxc7ppRGcazuUQL
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=postgres
DATABASE_URL="postgresql+psycopg://\${DATABASE_USER}:\${DATABASE_PASSWORD}@\${DATABASE_HOST}:\${DATABASE_PORT}/\${DATABASE_NAME}"
EOF
    fi  
}

help() {
    echo -e "Toolbox of scripts for easy python webdev. Supported functions: \n
    help - Summary of functionality.
    init - Creates a virtual environment and installs all required dependencies.
    migrate - Performs an SQL schema migration.
    install - Add and install dependencies.
    upgrade - Upgrades the installed dependencies.
    run devtools|dev|prod - Run devtools, the project in dev or production mode.
    stop devtools - Stops devtools.
    "
}

###########################################################
### Environment and dependency management 
###########################################################
test() {
    $PYTHON_EXECUTABLE --version
}

init() {
    # TODO - Add dev and prod profiles

    if [[ ! -d "$SCRIPT_DIR/.venv/" ]]; then
        echo "no venv dir found, creating..."
        $PYTHON_EXECUTABLE -m venv $SCRIPT_DIR/.venv
    fi  

    # No windows support
    source "$VENV_ACTIVATE_PATH"

    # Install dependencies
    pip install -r $SCRIPT_DIR/requirements.txt

    # Generate env file compatible with the docker compose
    generate_default_env
}

install() {
    source "$VENV_ACTIVATE_PATH"

    # Add arguments to requirements file
    for arg in "$@"
    do
        if ! grep -q $arg requirements.txt; then
            echo $arg >> requirements.txt
        else
            echo "$arg already in requirements"
        fi
    done

    # Install from requirements file
    pip install -r requirements.txt
}

upgrade() {
    # No windows support
    source "$VENV_ACTIVATE_PATH"

    pip install --upgrade -r "$SCRIPT_DIR/requirements.txt"
}

reset() {
    if [[ $1 == 'soft' ]]; then
        read -p "Are you sure? This will delete the virtual environment! " -n 1 -r
        echo 
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Soft resetting dev environment"
            rm -rf "$SCRIPT_DIR/.venv"
        fi
    else
        read -p "Are you sure? This will delete everything but the repository source files! " -n 1 -r
        echo 
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
            echo "Resetting dev environment"
            rm -rf "$SCRIPT_DIR/.venv"
            rm -rf "$SCRIPT_DIR/.docker"
            rm $SCRIPT_DIR/.env
        else
            echo "Aborting environment reset"
        fi
    fi
}

###########################################################
### SQL Migration tooling 
###########################################################

migrate() {
    source "$VENV_ACTIVATE_PATH"

    if [[ $1 == "up" ]]; then 
        ALEMBIC_ACTION="upgrade"
    elif [[ $1 == "down" ]]; then
        ALEMBIC_ACTION="downgrade"
    fi

    shift

    alembic $ALEMBIC_ACTION "$@"
}

###########################################################
### Dependency and project serving
###########################################################

run() {
    case "$1" in
        "devtools")
            echo Starting devtools...
            docker compose up -d > /dev/null
            echo Docker services running
            source "$VENV_ACTIVATE_PATH"
            ;;
        "dev")
            source "$VENV_ACTIVATE_PATH"
            python "$SCRIPT_DIR/src/main.py" 
            ;;
        "prod")
            echo run prod
            ;;
        *)
            echo usage
            ;;
    esac
}

stop() {
    case "$1" in
        "devtools")
            echo Stopping devtools...
            docker compose down > /dev/null
            echo Docker services stopped
            ;;
        "dev")
            echo run dev
            ;;
        "prod")
            echo run prod
            ;;
        *)
            echo usage
            ;;
    esac
}

FUNC=$1
shift

# Catch func not being defined and default to help
if [[ $(type -t $FUNC) == function ]]; then 
    "$FUNC" "$@"
else 
    echo "Unknown function"
    help
fi

