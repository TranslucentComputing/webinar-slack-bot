#!/bin/bash
set +e  # Continue on errors

echo "Installing Python Dependencies"
python -m pip install --quiet --upgrade pip setuptools
python -m pip install --quiet poetry
poetry config virtualenvs.create false
poetry install --no-root

COLOR_RED="\033[0;31m"
COLOR_BLUE="\033[0;94m"
COLOR_GREEN="\033[0;92m"
COLOR_BG_YELLOW="\033[43m"
COLOR_BOLD="\033[1m"
COLOR_RESET="\033[0m"

echo -e "${COLOR_BLUE}"
echo -e "  ████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗     ██╗   ██╗ ██████╗███████╗███╗   ██╗████████╗"
echo -e "  ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██║   ██║██╔════╝██╔════╝████╗  ██║╚══██╔══╝"
echo -e "     ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ██║   ██║██║     █████╗  ██╔██╗ ██║   ██║   "
echo -e "     ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██║   ██║██║     ██╔══╝  ██║╚██╗██║   ██║   "
echo -e "     ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗╚██████╔╝╚██████╗███████╗██║ ╚████║   ██║   "
echo -e "     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   "
echo -e "${COLOR_RESET}"

echo -e "${COLOR_GREEN}################################################################################"
echo -e "#                                                                              #"
echo -e "#                      Welcome to your development container!                  #"
echo -e "#                                                                              #"
echo -e "################################################################################${COLOR_RESET}"
echo -e "Run ${COLOR_GREEN}python run.py${COLOR_RESET} to start the application"
echo -e ""

# Set terminal prompt
if [ -n "$BASH" ]; then
    export PS1="\[${COLOR_BLUE}\]devspace\[${COLOR_RESET}\] ./\W \[${COLOR_BLUE}\]\\$\[${COLOR_RESET}\] "
else
    export PS1="$ ";
fi

# Include project's bin/ folder in PATH
export PATH="./bin:$PATH"

# Open shell
bash --norc
