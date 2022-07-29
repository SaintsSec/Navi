#!/bin/bash
# installer for Cryptex
# created by : Soulsender and C0SM0
# DO NOT FUCK WITH THIS SCRIPT

# color variables
red="\e[0;91m"
green="\e[0;92m"
blue="\e[0;94m"
bold="\e[1m"
reset="\e[0m"

function alias_workflow {
    # set up alias workflow
    echo -e "${blue}[*] Setting up alias...${reset}"

    # check if it already exists in bashrc
    if ! cat ~/.bashrc | grep "NAVI_PATH" > /dev/null; then
        # Do it in one command instead of repeating yourself.
        echo "
        export NAVI_PATH=\"~/.navi\"
        alias navi=\"python3 ~/.navi/core.py\"
        " >> ~/.bashrc
    fi

    #check if it already exists in zshrc
    if ! cat ~/.zshrc | grep "NAVI_PATH" > /dev/null; then
        # Do it in one command instead of repeating yourself.
        echo "
        export NAVI_PATH=\"~/.navi\"
        alias navi=\"python3 ~/.navi/core.py\"
        " >> ~/.zshrc
    fi

    echo -e "${green}[+] Completed${reset}"

    # clean up
    echo -e "${green}[+] Installation Successful"
    echo -e "[+] Please Restart your terminal"
    echo -e "[+] type 'navi' to launch navi${reset}"
    bash
}

# check if run with sudo
if [ "$EUID" -ne 0 ]; then
    continue
else
    echo -e "${red}Do not run as root. The script will prompt you for root access.${reset}"
    exit 0
fi

# arguments
while [ -n "$1" ]
do
case "$1" in
--help) 
  echo "
        SUPPORTED DISTROS:
        - Debian
            - Parrot
            - Ubuntu
            - Kali
        - Arch
        - Void
  "
  exit 0
;;

--unsupported-distro)
    # call alias workflow function
    alias_workflow
;;

esac
shift
done

# check for valid distro (Parrot, Ubuntu, Void, Debian, Arch)
distro=`sudo cat /etc/issue | awk '{print $1;}'`

# staging for testing
echo -e "${blue}[*] Staging process...${reset}"
mkdir ~/.navi
cd ..
cp navi/* ~/.navi -r
cd ~/.navi
echo -e "${green}[+] Completed${reset}"

if [[ "$distro" == "Debian" ]] || [[ "$distro" == "Parrot" ]] || [[ "$distro" == "Ubuntu" ]] || [[ "$distro" == "Linux" ]] || [[ "$distro" == "Kali" ]]; then
    # installing tools for debian
    echo -e "${blue}[*] Installing tools...${reset}"
    sudo apt update
    sudo apt-get install python3
    sudo apt-get install python3-pip python-dev
    pip3 install transformers
    pip3 install torch
    echo -e "${green}[+] Completed${reset}"

elif [[ "$distro" == "Void" ]]; then
    # installing tools for void
    echo -e "${blue}[*] Installing tools...${reset}"
    sudo xbps-install -S python3
    pip3 install transformers
    pip3 install torch
    echo -e "${green}[+] Completed${reset}"

elif [[ "$arch" = "Arch" ]]; then
    # installing tools for arch
    echo -e "${blue}[*] Installing tools...${reset}"
    sudo pacman -Syu
    sudo pacman -S python python-pip
    pip3 install transformers
    pip3 install torch
    echo -e "${green}[+] Completed${reset}"

else
    echo -e "${red}[!] Unknown distro, please see documentation for unknown distros.${reset}"
    exit 0
fi

# call alias workflow
alias_workflow