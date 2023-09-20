#!/bin/bash

art="
    _   __            _                 __           __      ____         _____           _       __ 
   / | / /___ __   __(_)               / /___ ______/ /__   /  _/___     / ___/__________(_)___  / /_
  /  |/ / __ \`/ | / / /  ______   __  / / __ \`/ ___/ //_/   / // __ \\    \\__ \\/ ___/ ___/ / __ \\/ __/
 / /|  / /_/ /| |/ / /  /_____/  / /_/ / /_/ / /__/ ,<    _/ // / / /   ___/ / /__/ /  / / /_/ / /_  
/_/ |_/\\__,_/ |___/_/            \\____/\\__,_/\\___/_/|_|  /___/_/ /_/   /____/\\___/_/  /_/ .___/\\__/  
                                                                                       /_/           
"

clear_screen() {
    clear
}

install_pip() {
    local distribution="$1"
    case "$distribution" in
        "ubuntu") sudo apt-get install python3-pip -y ;;
        "fedora") sudo dnf install python3-pip -y ;;
        "centos") sudo yum install python3-pip -y ;;
        *) echo "Sorry, this distribution is not supported yet."
           exit 1
           ;;
    esac
}

install_requirements() {
    pip3 install -r requirements.txt
}

setup_aliases() {
    local shell_choice="$1"
    declare -A config_files=( ["bash"]="~/.bashrc" ["zsh"]="~/.zshrc" )
    local config_path="${config_files[$shell_choice]}"

    declare -A aliases=( ["navi"]="python3 /opt/Navi/navi-shell.py" ["naviweb"]="python3 /opt/Navi/navi-web.py" )

    for alias_name in "${!aliases[@]}"; do
        if ! grep -q "alias $alias_name=" "$config_path"; then
            echo "alias $alias_name='${aliases[$alias_name]}'" >> "$config_path"
            echo "Alias '$alias_name' added."
        else
            echo "Alias '$alias_name' already exists."
        fi
    done

    echo "You may need to source $config_path or restart your terminal/shell."
}

setup_service() {
    sudo cp ./rasa-core.service /etc/systemd/system/
    sudo systemctl enable rasa-core.service
    echo "rasa-core.service enabled."
}

delete_navi() {
    if [ -d "/opt/Navi" ]; then
        sudo rm -rf "/opt/Navi"
        echo "Removed existing /opt/Navi directory."
    fi
}

copy_navi() {
    sudo cp -r . /opt/Navi
    echo "Copied Navi to /opt."
}

cleanup_install_directory() {
    cd /opt/Navi || exit 1
    declare -a files_to_remove=("jackin.py" "requirements.txt" "rasa-core.service" "README.md" ".git" ".gitignore")
    
    for item in "${files_to_remove[@]}"; do
        if [ -e "$item" ]; then
            sudo rm -rf "$item"
        fi
    done
    echo "Cleaned up installation directory."
}

set_permissions_recursive() {
    sudo chown -R :navi /opt/Navi/
    sudo chmod -R 070 /opt/Navi/
    echo "Set permissions for /opt/Navi."
}

# Script execution starts here:

clear_screen
echo "$art"

# Create navi group and add the current user to it
if ! grep -q "^navi:" /etc/group; then
    sudo groupadd navi
fi
sudo usermod -aG navi "$USER"
echo "Added user '$USER' to group 'navi'."

# Distribution choice
echo "Choose your Linux distribution:"
options=("Ubuntu/Debian" "Fedora" "CentOS")
select distribution in "${options[@]}"; do
    case $distribution in
        "Ubuntu/Debian") install_pip "ubuntu" ;;
        "Fedora") install_pip "fedora" ;;
        "CentOS") install_pip "centos" ;;
        *) echo "Invalid choice!"; exit 1 ;;
    esac
    break
done

# Shell choice
echo "Choose your shell:"
shells=("bash" "zsh")
select shell_choice in "${shells[@]}"; do
    case $shell_choice in
        "bash"|"zsh") setup_aliases "$shell_choice" ;;
        *) echo "Invalid choice!"; exit 1 ;;
    esac
    break
done

# Installation steps
delete_navi
copy_navi
install_requirements
setup_service
cleanup_install_directory
set_permissions_recursive

echo "Installation completed!"
