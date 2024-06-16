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
UPDATE='+----------------------------------------------------------+
|░█░█░█▀█░█▀▄░█▀█░▀█▀░█▀▀░░░█▀▀░█▀█░█▄█░█▀█░█░░░█▀▀░▀█▀░█▀▀|
|░█░█░█▀▀░█░█░█▀█░░█░░█▀▀░░░█░░░█░█░█░█░█▀▀░█░░░█▀▀░░█░░█▀▀|
|░▀▀▀░▀░░░▀▀░░▀░▀░░▀░░▀▀▀░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░▀░░▀▀▀|
+----------------------------------------------------------+'
CLAM='+--------------------------------------------------------------+
|░█▀█░█░█░░░█▀▀░█▀▀░▀█▀░█░█░█▀█░░░░░█░░░█░█░█▀█░█▀▄░█▀█░▀█▀░█▀▀|
|░█▀█░▀▄▀░░░▀▀█░█▀▀░░█░░█░█░█▀▀░░░▄▀░░░░█░█░█▀▀░█░█░█▀█░░█░░█▀▀|
|░▀░▀░░▀░░░░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░░░░░▀░░░░░▀▀▀░▀░░░▀▀░░▀░▀░░▀░░▀▀▀|
+--------------------------------------------------------------+'

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
            python3 -m spacy download en_core_web_sm
            sudo apt install clamav whois nmap randtype
            ;;
        "CSI") 
            sudo apt update
            sudo apt install -y python3 python3-pip randtype whois nmap 
            sudo apt install clamav
            python3 -m pip install --upgrade pip 
            sudo pip install requests pyfiglet click tabulate spacy
            pip install -U pyopenssl cryptography
            sudo pip install -U pyopenssl cryptography
            python3 -m spacy download en_core_web_sm
            ;;
        "Arch") 
            sudo pacman -Sy python3 python3-pip whois nmap randtype 
            sudo pacman -Sy python python-pip python-requests python-pyfiglet python-click python-tabulate python-spacy clamav 
            python3 -m pip install --upgrade pip
            python3 -m spacy download en_core_web_sm
            ;;
    esac
}

fresh_clam() {
    echo "$CLAM"
    echo 
    echo "Navi> Lets update Clam AV so we can bust some viruses!" | randtype -t 5,5000 -m 4
    echo 
    sudo systemctl stop clamav-freshclam.service
    sudo freshclam
}

setup_aliases() {
    local shell_choice="$1"
    declare -A config_files=( ["bash"]="/home/$USER/.bashrc" ["zsh"]="/home/$USER/.zshrc" )
    local config_path="${config_files[$shell_choice]}"

    declare -A aliases=(["navi"]="python3 /opt/Navi/navi_shell.py")

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
    echo "Navi> Set permissions for $distribution." | randtype -t 5,500 -m 4
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

echo "$INSTALLING"
echo "Navi> Lets get these pesky requirements out of the way..." | randtype -t 5,5000 -m 4

# Create navi group and add the current user to it
create_navi_group(){
    if ! grep -q "^navi:" /etc/group; then
        sudo groupadd navi
    fi
    sudo usermod -aG navi "$USER"
    echo "Navi> Added user '$USER' to group 'navi'." | randtype -t 5,5000 -m 4
}

# Distribution choice
echo "Navi> Lets see what OS are you using:" | randtype -t 5,5000 -m 4
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
echo "$UPDATE"
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
install_reqs
fresh_clam
echo 
echo "$COMPLETE"
echo "Navi> Good news $USER I have been installed on your $distribution system!" | randtype -t 5,5000 -m 4
echo "Navi> [!!] - PLEASE RESTART YOUR TERMINAL OR SOURCE YOUR SHELL CONFIG." | randtype -t 5,5000 -m 4
