#! bin/bash
echo "Navi> [!] - Welcome to the Navi Git Tool!"
echo "Navi> [!] - Do you have and update? (Yes/No)
read updateChoice
if [$updateChoice == Yes]; then
    echo "Navi\> Very well, Will all non-repo owner updates go into the edge branch." 
    echo "Navi\> You will still need to make a PR to see it reflected to main."
    git add .
    echo "Navi\> What is your commit message?"
    read commitMessage
    git commit -m "$commitMessage"
    echo "Navi\> Pushing to edge repo now!"
    git push origin edge
else:
    echo "Navi\> Maybe later!"
fi