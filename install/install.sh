#!/bin/bash 

#Banners and such
COMPLETE='+----------------------------------------------------------------+
|░▀█▀░█▀█░█▀▀░▀█▀░█▀█░█░░░█░░░░░█▀▀░█▀█░█▄█░█▀█░█░░░█▀▀░▀█▀░█▀▀░█|
|░░█░░█░█░▀▀█░░█░░█▀█░█░░░█░░░░░█░░░█░█░█░█░█▀▀░█░░░█▀▀░░█░░█▀▀░▀|
|░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░▀░░▀▀▀░▀|
+----------------------------------------------------------------+'
INSTALLING='+------------------------------------------------------------------+
|░▀█▀░█▀█░█▀▀░▀█▀░█▀█░█░░░█░░░▀█▀░█▀█░█▀▀░░░█▀▀░█░█░█▀▀░▀█▀░█▀▀░█▄█|
|░░█░░█░█░▀▀█░░█░░█▀█░█░░░█░░░░█░░█░█░█░█░░░▀▀█░░█░░▀▀█░░█░░█▀▀░█░█|
|░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░░▀░░▀▀▀░░▀░░▀▀▀░▀░▀|
+------------------------------------------------------------------+'
CLEANING='+----------------------------------------------------------------------------------------+
|░█▀▀░█░░░█▀▀░█▀█░█▀█░▀█▀░█▀█░█▀▀░░░▀█▀░█▀█░█▀▀░▀█▀░█▀█░█░░░█░░░░░█▀▀░█▀█░█░░░█▀▄░█▀▀░█▀▄|
|░█░░░█░░░█▀▀░█▀█░█░█░░█░░█░█░█░█░░░░█░░█░█░▀▀█░░█░░█▀█░█░░░█░░░░░█▀▀░█░█░█░░░█░█░█▀▀░█▀▄|
|░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀░░░▀░░░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀░▀|
+----------------------------------------------------------------------------------------+'
SHELL='+----------------------------------------------+
|░█▀▀░█░█░█▀▀░█░░░█░░░░░█▀▀░█▀▀░█░░░█▀▀░█▀▀░▀█▀|
|░▀▀█░█▀█░█▀▀░█░░░█░░░░░▀▀█░█▀▀░█░░░█▀▀░█░░░░█░|
|░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░|
+----------------------------------------------+'
# Get the OS name and version
OS_NAME=$(cat /etc/os-release | grep PRETTY_NAME | cut -d '=' -f 2-)
VERSION=$(lsb_release -rcs)
distribution = $OS_NAME $OS_VERSION

clear_screen() {
    clear
}

install_reqs() {
    sudo apt install randtype nmap python3 python3-pip
    pip install -r requirements.txt --break-system-packages
    python3 -m spacy download en_core_web_sm
}

setup_aliases() {
    local shell_choice="$1"
    declare -A config_files=( ["bash"]="/home/$USER/.bashrc" ["zsh"]="/home/$USER/.zshrc" )
    local config_path="${config_files[$shell_choice]}"

    declare -A aliases=( ["navi"]="python3 /opt/Navi/navi_shell.py")

    for alias_name in "${!aliases[@]}"; do
        if ! grep -q "alias $alias_name=" "$config_path"; then
            echo "alias $alias_name='${aliases[$alias_name]}'" >> "$config_path"
            echo "Navi> My alias has been added. So you can quickly get to me!" | randtype -t 5,5000 -m 4
        else 
            echo "Navi> Oh my... My alias already exists. Moving on..." | randtype -t 5,5000 -m 4 
        fi
    done
}

delete_navi() {
    echo "$CLEANING"
    if [ -d "/opt/Navi" ]; then
        sudo rm -rf "/opt/Navi"
        echo "Navi> Removed my existing version directory. Bye Felicia!" | randtype -t 5,5000 -m 4
    fi
}

copy_navi() {
    sudo cp -r ../ /opt/Navi
    echo "Navi> Copied myself to the /opt directory. My Influence grows." | randtype -t 5,5000 -m 4
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
    echo "Navi> Removed bloat and cleaned up installation directory." | randtype -t 5,5000 -m 4
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
    echo "Navi> Set permissions for $OS_NAME $OS_VERSION." | randtype -t 5,500 -m 4
}

# Script execution starts here:
# pre-run requirements
install_reqs
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

echo "$INSTALLING"
echo "Navi> Let's see here you are on $OS_NAME $OS_VERSION" | randtype -t 5,5000 -m 4
echo "Navi> Lets get this party rolling!"

# Create navi group and add the current user to it
create_navi_group(){
    if ! grep -q "^navi:" /etc/group; then
        sudo groupadd navi
    fi
    sudo usermod -aG navi "$USER"
    echo "Navi> Added user '$USER' to group 'navi'." | randtype -t 5,5000 -m 4
}

# Shell choice
echo "$SHELL"
echo "Navi> Now what Shell do you prefer:" | randtype -t 5,5000 -m 4
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
echo 
echo "$COMPLETE"
echo "Navi> Good news $USER I have been installed on your $OS_NAME $OS_VERSION system!" | randtype -t 5,5000 -m 4
echo "Navi> [!!] - Be sure you restart your terminal or source the config for your shell before running 'navi' in the cli." | randtype -t 5,5000 -m 4 
