#!/bin/bash

art=="
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

install_reqs() {
    local distribution="$1"
    case "$distribution" in
        "ubuntu" | "debian" | "Pop!_OS") 
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip whois nmap clamav
            python3 -m pip install --upgrade pip
            pip3 install -r requirements.txt
            sudo pip3 install -r requirements.txt
            pip install -U pyopenssl cryptography
            sudo pip install -U pyopenssl cryptography

            ;;
        "CSI") 
            sudo apt-get update
            sudo apt-get install -y python3-pip whois nmap clamav
            python -m pip install --upgrade pip
            pip3 install -r requirements.txt
            sudo pip3 install -r requirements.txt
            pip install -U pyopenssl cryptography
            sudo pip install -U pyopenssl cryptography
            ;;
        "Arch") 
            sudo pacman -S python-pip whois nmap clamav -y
            python -m pip install --upgrade pip
            pip3 install -r requirements.txt
            sudo pip3 install -r requirements.txt
            pip install -U pyopenssl cryptography
            sudo pip install -U pyopenssl cryptography
            ;;
        "fedora") 
            sudo dnf install -y python3-pip whois nmap clamav
            python -m pip install --upgrade pip
            pip3 install -r requirements.txt
            sudo pip3 install -r requirements.txt
            pip install -U pyopenssl cryptography
            sudo pip install -U pyopenssl cryptography

            ;;
        "centos") 
            sudo yum install -y python3-pip whois nmap clamav
            pip3 install -r requirements.txt
            sudo pip3 install -r requirements.txt
            pip install -U pyopenssl cryptography
            sudo pip install -U pyopenssl cryptography
            ;;
    esac
}

fresh_clam() {
    sudo freshclam
}

setup_aliases() {
    local shell_choice="$1"
    declare -A config_files=( ["bash"]="/home/$USER/.bashrc" ["zsh"]="/home/$USER/.zshrc" )
    local config_path="${config_files[$shell_choice]}"

    declare -A aliases=( ["navi"]="python3 /opt/Navi/navi-shell.py" )

    for alias_name in "${!aliases[@]}"; do
        if ! grep -q "alias $alias_name=" "$config_path"; then
            echo
            echo "alias $alias_name='${aliases[$alias_name]}'" >> "$config_path"
            echo "Alias '$alias_name' added."
        else
            echo 
            echo "Alias '$alias_name' already exists."
        fi
    done

    echo "You may need to source $config_path or restart your terminal/shell."
}

delete_navi() {
    if [ -d "/opt/Navi" ]; then
        sudo rm -rf "/opt/Navi"
        echo "Removed existing /opt/Navi directory."
    fi
}

copy_navi() {
    sudo cp -r ../ /opt/Navi
    echo "Copied Navi to /opt."
}

cleanup_install_directory() {
    cd /opt/Navi || exit 1
    declare -a files_to_remove=("install" "README.md" ".git" ".gitignore")
    
    for item in "${files_to_remove[@]}"; do
        if [ -e "$item" ]; then
            sudo rm -rf "$item"
        fi
    done
    echo 
    echo "Cleaned up installation directory."
}

set_permissions_csi(){
    sudo chown -R :csi /opt/Navi
    sudo chmod 777 /opt/Navi
    echo
    echo "Permissions set for CSI"
}

set_permissions_All() {
    sudo chown -R :navi /opt/Navi/
    sudo chmod -R 777 /opt/Navi/
    echo 
    echo "Set permissions for $distribution."
}

# Script execution starts here:

clear_screen
echo "$art"

# Create navi group and add the current user to it
create_navi_group(){
    if ! grep -q "^navi:" /etc/group; then
        sudo groupadd navi
    fi
    sudo usermod -aG navi "$USER"
    echo "Added user '$USER' to group 'navi'."
}

# Distribution choice
echo "Choose your Linux distribution:"
options=("Ubuntu/Debian" "Pop!_OS" "CSI" "Arch" "Fedora" "CentOS")
select distribution in "${options[@]}"; do
    case $distribution in
        "Ubuntu/Debian") install_reqs "ubuntu" ;;
        "Pop!_OS") install_reqs "ubuntu" ;;
        "Arch") install_reqs "arch" ;;
        "CSI") install_reqs "CSI" ;;
        "Fedora") install_reqs "fedora" ;;
        "CentOS") install_reqs "centos" ;;
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

csi_install(){
    delete_navi
    copy_navi
    install_reqs
    fresh_clam
    set_permissions_csi
    cleanup_install_directory
    echo "CSI Installation completed!"
}

#check if distribution is CSI and install CSI dependencies
if [ "$distribution" == "CSI" ]; then
    csi_install
    exit 0
fi

# Installation steps
create_navi_group
delete_navi
copy_navi
set_permissions_All
cleanup_install_directory
install_reqs
fresh_clam
echo
echo "Navi> $distribution Installation completed!"
