#!/bin/bash 


# Get the OS name and version
OS_NAME=$(cat /etc/os-release | grep PRETTY_NAME | cut -d '=' -f 2-)
VERSION=$(lsb_release -rcs)
USER=$(whoami)
SHELL=$(id -p $USER | cut -d: -f7)

# Navi auto launch option:
while getopts ":l" opt; do
  case $opt in
    l) LAUNCH_NAVI="true";;
    \?) echo "Invalid option: -$OPTARG"; exit 1;;
  esac
done

clear_screen() {
    clear
}

install_reqs() {
    sudo apt install python3 python3-pip python3-venv
}

set_venv(){
    python3 -m venv ../navienv
    source ../navienv/bin/activate
    echo 
    echo Venv has been set.
    echo 
}

pip_install(){
    echo Installing Pip requirements
    python3 -m install pip install --upgrade pip
    pip install -r requirements.txt 
    pip install spacy 
    python3 -m spacy download en_core_web_sm 
    echo
    echo Pip requirements have been installed.
    echo 
}

setup_aliases() {
    local config_files=( ["bash"]="/home/$USER/.bashrc" ["zsh"]="/home/$USER/.zshrc" )
    config_path="${config_files[$SHELL]}"
    
    declare -A aliases=( ["navi"]="source /opt/Navi/navienv/bin/activate && cd /opt/Navi/ && exec python3 ./navi_shell.py")

    for alias_name in "${!aliases[@]}"; do
        if ! grep -q "alias $alias_name=" "$config_path"; then
            echo "alias $alias_name='${aliases[$alias_name]}'" >> "$config_path"
            echo "Navi alias added..."
        else
            echo "Navi alias exists. Moving on."
        fi
    done
}

delete_navi() {
    if [ -d "/opt/Navi" ]; then
        sudo rm -rf "/opt/Navi"
        echo "Removed existing version"
    fi
}

source_shell_config(){
    echo
    echo "Installation for ${OS_NAME} ${OS_VERSION} complete!"
    echo "Attempting to source ${config_path}"
    exec ${SHELL}
    if [ "$SHELL" = "/bin/zsh" ]; then
        source ~/.zshrc
    elif [ "$SHELL" = "/bin/bash" ]; then
        source ~/.bashrc
    fi
    echo "config has been sourced."
}

copy_navi() {
    sudo cp -r ../ /opt/Navi
    echo "Copying files to /opt/Navi"
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
    echo "Removed git files and install directory from /opt/Navi"
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
    echo "Permissions set for: $OS_NAME $OS_VERSION."
}
 
# Create navi group and add the current user to it
create_navi_group(){
    if ! grep -q "^navi:" /etc/group; then
        sudo groupadd navi
    fi
    sudo usermod -aG navi "$USER"
    echo "Added user '$USER' to group 'navi'."
}

# Installation steps
install_reqs
set_venv
pip_install
create_navi_group
delete_navi
copy_navi
setup_aliases
set_permissions_All
cleanup_install_directory
source_shell_config
if [ "$LAUNCH_NAVI" = "true" ]; then
  source /opt/Navi/navienv/bin/activate && cd /opt/Navi/ && exec python3 ./navi_shell.py
fi
exit