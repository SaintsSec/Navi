#!/bin/bash 

pregame(){
    clear
    cat csiart.txt
}

install_reqs() {
    sudo apt update
    sudo apt install -y python3 python3-pip
    python3 -m pip install --upgrade pip 
    pip install -r requirements.txt 
    sudo apt install clamav whois nmap    
}

setup_aliases() {
    local config_path="/home/$USER/.bashrc"
    declare -A aliases=( ["navi"]="python3 /opt/Navi/navi-shell.py" ["@Navi"]="python3 /opt/Navi/navi-shell.py -q" ["@navi"]="python3 /opt/Navi/navi-shell.py -q")

    for alias_name in "${!aliases[@]}"; do
        if ! grep -q "alias $alias_name=" "$config_path"; then
            echo "alias $alias_name='${aliases[$alias_name]}'" >> "$config_path"
            echo "Alias '$alias_name' added."
        else
            echo "Alias '$alias_name' already exists."
        fi
    done
}

delete_navi() {
    if [ -d "/opt/Navi" ]; then
        sudo rm -rf "/opt/Navi"
        echo "Navi> Removed existing /opt/Navi directory."
    fi
}

copy_navi() {
    sudo cp -r ../ /opt/Navi
    echo "Navi> Copied myself to /opt."
}

cleanup_install_directory() {
    cd /opt/Navi || exit 1
    declare -a files_to_remove=("install" "README.md" ".git" ".gitignore")

    for item in "${files_to_remove[@]}"; do
        if [ -e "$item" ]; then
            sudo rm -rf "$item"
        fi
    done
    echo "Navi> Cleaned up installation directory."
}

set_permissions_csi() {
    sudo chown -R :csi /opt/Navi
    sudo chmod 770 /opt/Navi
    echo "Navi> Permissions set for CSI"
}

fresh_clam() {
    sudo systemctl stop clamav-freshclam.service
    sudo freshclam
}

# Execution starts here
install_reqs
pregame 
setup_aliases
create_navi_group
delete_navi
copy_navi
set_permissions_csi
cleanup_install_directory
fresh_clam

echo "Navi> CSI Linux Installation completed!"
echo "Navi> [!!] - Please restart your terminal"

