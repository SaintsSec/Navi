#!/bin/bash

art="
   ___________ ____         __           __         ____         _____           _       __ 
  / ____/ ___//  _/        / /___ ______/ /__      /  _/___     / ___/__________(_)___  / /_
 / /    \__ \ / /(_)  __  / / __ `/ ___/ //_/_____ / // __ \    \__ \/ ___/ ___/ / __ \/ __/
/ /___ ___/ // /_    / /_/ / /_/ / /__/ ,< /_____// // / / /   ___/ / /__/ /  / / /_/ / /_  
\____//____/___(_)   \____/\__,_/\___/_/|_|     /___/_/ /_/   /____/\___/_/  /_/ .___/\__/  
                                                                              /_/           
"

clear

echo "$art"

install_reqs() {
    sudo apt-get update
    sudo apt-get install -y python3-pip nmap clamav
    pip3 install -r requirements.txt
    sudo pip3 install -r requirements.txt
}

setup_aliases() {
    local config_path="/home/$USER/.bashrc"
    declare -A aliases=( ["navi"]="python3 /opt/Navi/navi-shell.py")

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
    echo "Cleaned up installation directory."
}

set_permissions_csi() {
    sudo chown -R :csi /opt/Navi
    sudo chmod 770 /opt/Navi
    echo "Permissions set for CSI"
}

fresh_clam() {
    sudo freshclam
}

# Execution starts here

install_reqs
setup_aliases
create_navi_group
delete_navi
copy_navi
set_permissions_csi
setup_csi_service
cleanup_install_directory
fresh_clam

echo "Navi: CSI Linux Installation completed!"

