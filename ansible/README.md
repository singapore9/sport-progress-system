# Infrastructure for production


## Requirements
All the roles work with this ansible setup
Don't forget about having vault password file :)
```bash
$ ansible --version
ansible [core 2.14.3]
  ...
  python version = 3.11.2
  jinja version = 3.1.2
  libyaml = True

$ ansible-vault --version
ansible-vault [core 2.14.3]
  python version = 3.11.2 
  jinja version = 3.1.2
  libyaml = True

```

## Usage
Base usage (deploy to the server and run it from master branch)
```bash
ansible-playbook code-deploy.yml --vault-password-file=PASSWORDFILE
```

Specify branch with 
```bash
ansible-playbook code-deploy.yml --vault-password-file=PASSWORDFILE --extra-vars "git_repo_branch=BRANCH"
```

