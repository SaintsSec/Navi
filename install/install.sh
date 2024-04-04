#!/bin/bash 

clear_screen() {
    clear
}

install_reqs() {
    local distribution="$1"
    case "$distribution" in
        "ubuntu" | "Pop!_OS") 
            sudo apt update
            sudo apt install -y python3 python3-pip
            pip install -r requirements.txt 
            sudo apt install clamav whois nmap
            ;;
        "CSI") 
            sudo apt update
            sudo apt install -y python3 python3-pip whois nmap 
            sudo apt install clamav
            python3 -m pip install --upgrade pip 
            sudo pip install requests fpdf pyfiglet click tabulate openai
            pip install -U pyopenssl cryptography
            sudo pip install -U pyopenssl cryptography
            ;;
        "Arch") 
            sudo pacman -Sy python3 python3-pip whois nmap sudo pacman -Sy python python-pip python-requests python-fpdf python-pyfiglet python-click python-tabulate python-openai clamav 
            python3 -m pip install --upgrade pip
            ;;
    esac
}

fresh_clam() {
    sudo systemctl stop clamav-freshclam.service
    sudo freshclam
}

setup_aliases() {
    local shell_choice="$1"
    declare -A config_files=( ["bash"]="/home/$USER/.bashrc" ["zsh"]="/home/$USER/.zshrc" )
    local config_path="${config_files[$shell_choice]}"

    declare -A aliases=( ["navi"]="python3 /opt/Navi/navi-shell.py" ["@Navi"]="python3 /opt/Navi/navi-shell.py -q" ["@navi"]="python3 /opt/Navi/navi-shell.py -q")

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
# Define the user to check for
USER_TO_CHECK="elric"

# Get the current user
CURRENT_USER=$(whoami)

# Check if the current user matches the one we want to check
if [ "$CURRENT_USER" = "$USER_TO_CHECK" ]; then
    # If they match, cat the file 
    cat .specialArt.txt
else 
    cat installart.txt
fi

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
options=("Ubuntu" "Pop!_OS" "CSI" "Arch")
select distribution in "${options[@]}"; do
    case $distribution in
        "Ubuntu") install_reqs "ubuntu" ;;
        "Pop!_OS") install_reqs "ubuntu" ;;
        "Arch") install_reqs "arch" ;;
        "CSI") install_reqs "CSI" ;;
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
preRun
create_navi_group
delete_navi
copy_navi
set_permissions_All
cleanup_install_directory
install_reqs
fresh_clam
echo
echo "Navi> Good news $USER I have been installed on your $distribution system!"
echo "Navi> [!!] - PLEASE RESTART YOUR TERMINAL OR SOURCE YOUR SHELL CONFIG."
