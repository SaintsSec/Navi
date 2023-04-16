# Contributing to Navi 🤝
Firstly, thank you for taking the time to contribute.
<br/>
We welcome contributions from anyone willing to improve this project or add new features. You may see historic contributors on the repositories page on the right-hand panel.
<br/>
Contribution guidelines are listed below. Please take the time to go through the guidelines and follow them so that it is easy for maintainers to merge or address your contributions. 
</br>


## Table of Contents

- [Contributing to Navi 🤝](#contributing-to-navi-)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [First time Contributor](#first-time-contributor)
  - [I Want To Contribute](#i-want-to-contribute)
    - [Legal Notice](#legal-notice)
    - [Fork the Project](#fork-the-project)
    - [Create a new branch](#create-a-new-branch)
    - [Work on the issue assigned](#work-on-the-issue-assigned)
    - [Commit](#commit)
    - [Work Remotely](#work-remotely)
    - [Pull Request](#pull-request)
    - [Review](#review)
  - [Other Ways to Contribute](#other-ways-to-contribute)


## Code of Conduct

This project and everyone participating in it is governed by the [Navi Code of Conduct](https://github.com/SSGorg/Navi/blob/main/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## First time Contributor

As a first-time contributor, if you are not sure about contributing, feel free to ask our dev team on our [Discord Server](https://discord.gg/899KQFeAXr)
<br/>
A good place to start would be our list of [good first issues](https://github.com/SSGorg/Navi/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

## I Want To Contribute

- Always check for [existing issues](https://github.com/SSGorg/Navi/issues) before creating a new issue.
- Only start working on an issue if it has been assigned to you. This avoids multiple PRs for the same issue.
- Every change in this project must have an associated issue. **Issue before PR**

### Legal Notice
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content, and that the content you contribute may be provided under the project license.

To start contributing to this project, follow the steps below.

### Fork the Project

- Fork this repository. This will create a local copy of this repository on your GitHub profile.

  <a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/J4pdgJZH/Screenshot-2022-10-10-at-18-51-49.png' border='0' alt='Fork Repository'/></a>

- Now clone the forked repository on your local machine.

  ```bash
  git clone https://github.com/<your-username>/Navi.git
  ```
  
- Keep a reference to the original project in `upstream` remote.

  ```bash
  cd Navi  
  git remote add upstream https://github.com/SSGorg/Navi.git
  ```

- Synchronize your copy before working.

  ```bash
  git remote update
  git checkout -b main
  git rebase upstream/main
  ```

### Create a new branch

Creating a new branch lets you work on your issue without creating merge conflicts while making PRs.
Select a name for your branch that is in line with the issue you are addressing.

```bash
# It will create a new branch with name branch_name and switch to that branch 
git checkout -b branch_name
```

### Work on the issue assigned

- Work on the issue assigned to you.
- Add all the files/folders needed.
- After you've made your contribution to the project, add changes to the branch you've just created:

```bash
# To add all new files to branch branch_name  
git add .  

# To add only a few files to branch_name
git add <names of files changed or added>
```

### Commit

- To commit this change, give a descriptive message for the convenience of reviewer

```bash
# This message will be associated with all files you have changed  
git commit -m "message"  
```

### Work Remotely

```bash
# To push your work to your remote repository
git push -u origin branch_name
```

### Pull Request

Go to your repository on your web browser and click on 'Compare and pull request'.
This will send a request to the maintainer to add your contribution to the main repository `https://github.com/SSGorg/Navi`
<br/>
Add a title to your Pull Request.
<br/>Make sure to mention which issue is solved with this Pull Request by mentioning the issue number #. Then add a description to your Pull Request that explains your contribution.
<br/> 

### Review

🎉🌟Congratulations! Now sit and relax, you've made your contribution to the Navi project. Wait until the PR is reviewed and changes are incorporated as suggested by the reviewers, after which the PR can be successfully merged.

## Other Ways to Contribute

If you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about.
- Join our [Discord Server](https://discord.gg/899KQFeAXr)
- Star the project
- Tweet about it
- Mention this project to your peers
Any contribution is welcome!
