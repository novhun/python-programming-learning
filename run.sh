#!/usr/bin/env bash
# ==============================================================================
# 🐍 Complete Python Mastery: Master Runner Script
# ==============================================================================
# Usage:
#   ./run.sh                 -> Interactive Selection Menu
#   ./run.sh <number>        -> Run specific part (e.g., ./run.sh 1 or ./run.sh 12)
#   ./run.sh all             -> Run all parts 01 through 15 sequentially
#   ./run.sh test            -> Run automated unit tests (Part 10)
#   ./run.sh fastapi         -> Start FastAPI development server (Part 11)
#   ./run.sh django          -> Start Django development server (Part 12)
#   ./run.sh install         -> Install optional dependencies for web & database parts
# ==============================================================================

set -e

# Terminal colors
BOLD='\033[1m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Base directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Resolve python interpreter (use venv if present)
if [ -d "$SCRIPT_DIR/.venv" ]; then
    PYTHON="$SCRIPT_DIR/.venv/bin/python"
elif [ -d "$SCRIPT_DIR/venv" ]; then
    PYTHON="$SCRIPT_DIR/venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    PYTHON="python"
fi

print_header() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${BOLD}          🐍 Python Programming Mastery Course Runner          ${NC}${PURPLE}║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo -e "${CYAN}Interpreter:${NC} $($PYTHON --version 2>&1)\n"
}

run_part() {
    local part_num="$1"
    local script_path=""
    local title=""

    case "$part_num" in
        1|01|"part-01")
            script_path="part-01-basics-and-syntax/main.py"
            title="Part 01: Basics & Syntax"
            ;;
        2|02|"part-02")
            script_path="part-02-control-flow-and-loops/main.py"
            title="Part 02: Control Flow & Loops"
            ;;
        3|03|"part-03")
            script_path="part-03-data-structures/main.py"
            title="Part 03: Data Structures Mastery"
            ;;
        4|04|"part-04")
            script_path="part-04-functions-and-modules/main.py"
            title="Part 04: Functions, Scopes & Modules"
            ;;
        5|05|"part-05")
            script_path="part-05-oop-fundamentals/main.py"
            title="Part 05: OOP Fundamentals"
            ;;
        6|06|"part-06")
            script_path="part-06-oop-advanced/main.py"
            title="Part 06: Advanced OOP & Architecture"
            ;;
        7|07|"part-07")
            script_path="part-07-error-handling-and-files/main.py"
            title="Part 07: Error Handling & File I/O"
            ;;
        8|08|"part-08")
            script_path="part-08-functional-and-advanced-patterns/main.py"
            title="Part 08: Functional & Advanced Patterns"
            ;;
        9|09|"part-09")
            script_path="part-09-concurrency-and-async/main.py"
            title="Part 09: Concurrency, Threading & Asyncio"
            ;;
        10|"part-10")
            script_path="part-10-modern-tooling-and-best-practices/main.py"
            title="Part 10: Modern Tooling & Testing"
            ;;
        11|"part-11")
            script_path="part-11-fastapi-modern-apis/main.py"
            title="Part 11: Modern Web APIs with FastAPI"
            ;;
        12|"part-12")
            script_path="part-12-django-web-framework/main.py"
            title="Part 12: Enterprise Full-Stack Django"
            ;;
        13|"part-13")
            script_path="part-13-sqlalchemy-orm/main.py"
            title="Part 13: Database Mastery with SQLAlchemy 2.0"
            ;;
        14|"part-14")
            script_path="part-14-alembic-migrations/main.py"
            title="Part 14: Database Schema Migrations with Alembic"
            ;;
        15|"part-15")
            script_path="part-15-database-crud-patterns/main.py"
            title="Part 15: Database CRUD & Repository Patterns"
            ;;
        *)
            echo -e "${RED}Error: Unknown part '$part_num'. Available options: 1 to 15, all, test, django, fastapi.${NC}"
            exit 1
            ;;
    esac

    if [ ! -f "$script_path" ]; then
        echo -e "${RED}Error: Target file not found: $script_path${NC}"
        exit 1
    fi

    echo -e "\n${BLUE}▶ Running ${BOLD}${title}${NC} (${CYAN}${script_path}${NC})...\n"
    $PYTHON "$script_path"
    echo -e "\n${GREEN}✔ Finished ${title}!${NC}\n"
}

run_all() {
    echo -e "${BOLD}${CYAN}Running all 15 parts sequentially...${NC}\n"
    for i in {1..15}; do
        run_part "$i"
    done
    echo -e "${BOLD}${GREEN}================================================================${NC}"
    echo -e "${BOLD}${GREEN}  🎉 All 15 Python Course Modules Ran Successfully!            ${NC}"
    echo -e "${BOLD}${GREEN}================================================================${NC}"
}

run_test() {
    echo -e "${BLUE}▶ Running Automated Unit Tests for Part 10 (unittest)...${NC}\n"
    $PYTHON -m unittest part-10-modern-tooling-and-best-practices/test_calculator.py
}

run_fastapi() {
    echo -e "${BLUE}▶ Starting FastAPI server with Uvicorn (Port 8000)...${NC}"
    if ! $PYTHON -c "import fastapi, uvicorn" 2>/dev/null; then
        echo -e "${YELLOW}FastAPI/Uvicorn not found. Installing dependencies...${NC}"
        $PYTHON -m pip install -r part-11-fastapi-modern-apis/requirements.txt
    fi
    cd part-11-fastapi-modern-apis
    $PYTHON -m uvicorn main:app --reload --port 8000
}

run_django() {
    echo -e "${BLUE}▶ Starting Django development server (Port 8000)...${NC}"
    if ! $PYTHON -c "import django" 2>/dev/null; then
        echo -e "${YELLOW}Django not found. Installing dependencies...${NC}"
        $PYTHON -m pip install -r part-12-django-web-framework/requirements.txt
    fi
    $PYTHON part-12-django-web-framework/main.py runserver 8000
}

install_all_deps() {
    echo -e "${BLUE}▶ Installing dependencies for all web and database modules...${NC}"
    $PYTHON -m pip install --upgrade pip
    for req in part-*/requirements.txt; do
        if [ -f "$req" ]; then
            echo -e "${CYAN}Installing from $req...${NC}"
            $PYTHON -m pip install -r "$req"
        fi
    done
    echo -e "${GREEN}✔ All dependencies installed successfully!${NC}"
}

show_menu() {
    print_header
    echo -e "${BOLD}Select a module to run:${NC}"
    echo -e "  ${CYAN}01)${NC} Basics & Syntax             ${CYAN}09)${NC} Concurrency & Asyncio"
    echo -e "  ${CYAN}02)${NC} Control Flow & Loops        ${CYAN}10)${NC} Modern Tooling & Testing"
    echo -e "  ${CYAN}03)${NC} Data Structures             ${CYAN}11)${NC} FastAPI Modern APIs"
    echo -e "  ${CYAN}04)${NC} Functions & Modules         ${CYAN}12)${NC} Django Full-Stack Web"
    echo -e "  ${CYAN}05)${NC} OOP Fundamentals            ${CYAN}13)${NC} SQLAlchemy 2.0 ORM"
    echo -e "  ${CYAN}06)${NC} Advanced OOP                ${CYAN}14)${NC} Alembic Migrations"
    echo -e "  ${CYAN}07)${NC} Error Handling & Files      ${CYAN}15)${NC} Database CRUD Patterns"
    echo -e "  ${CYAN}08)${NC} Functional & Decorators"
    echo ""
    echo -e "${BOLD}Special Commands:${NC}"
    echo -e "  ${YELLOW}all${NC})      Run all 15 parts sequentially"
    echo -e "  ${YELLOW}test${NC})     Run Part 10 automated unit test suite"
    echo -e "  ${YELLOW}fastapi${NC})  Start live FastAPI Uvicorn server (http://127.0.0.1:8000/docs)"
    echo -e "  ${YELLOW}django${NC})   Start live Django web server (http://127.0.0.1:8000/)"
    echo -e "  ${YELLOW}install${NC})  Install all course dependencies via pip"
    echo -e "  ${RED}q${NC})        Quit"
    echo ""
    read -p "Enter choice [1-15, all, test, fastapi, django, install, q]: " choice

    case "$choice" in
        q|Q|exit)
            echo "Goodbye!"
            exit 0
            ;;
        all)
            run_all
            ;;
        test)
            run_test
            ;;
        fastapi)
            run_fastapi
            ;;
        django)
            run_django
            ;;
        install)
            install_all_deps
            ;;
        "")
            echo "No option selected. Exiting."
            exit 0
            ;;
        *)
            run_part "$choice"
            ;;
    esac
}

# --- CLI Routing ---
if [ $# -eq 0 ]; then
    show_menu
else
    case "$1" in
        all)
            print_header
            run_all
            ;;
        test)
            print_header
            run_test
            ;;
        fastapi|uvicorn)
            print_header
            run_fastapi
            ;;
        django)
            print_header
            run_django
            ;;
        install)
            print_header
            install_all_deps
            ;;
        -h|--help|help)
            print_header
            echo "Usage: ./run.sh [1-15 | all | test | fastapi | django | install]"
            ;;
        *)
            print_header
            run_part "$1"
            ;;
    esac
fi
