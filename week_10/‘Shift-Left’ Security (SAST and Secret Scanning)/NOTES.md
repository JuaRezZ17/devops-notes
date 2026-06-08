# ‘Shift-Left’ Security (SAST and Secret Scanning)

## Objective
Automate security in the earliest stages of development. Prevent code vulnerabilities or compromised private keys from leaving your local computer and ending up in the repositories.

### Shift-Left Philosophy
The Shift-Left philosophy means ‘moving security to the left’ within the software development lifecycle. In a traditional lifecycle, the phases are usually represented from left to right:

**`Planning → Development → Testing → Deployment → Production`**

When we talk about “moving to the left”, we mean that security measures should be applied from the earliest stages, particularly during design and development, rather than waiting until the application is already in production.

The main idea behind Shift-Left is to detect security flaws as early as possible. It is not the same to find a vulnerability whilst you are coding as it is to discover it once the application has already been released and is being used by real users. Shift-Left is important because it allows you to: detect faults earlier, reduce the cost of fixes, avoid vulnerabilities in production, improve code quality and make security part of daily development. The later a problem is discovered, the more difficult and expensive it usually is to fix.

### SAST (Static Application Security Testing)
SAST stands for Static Application Security Testing. It is a technique that analyses an application’s source code without running it. Its aim is to identify potential vulnerabilities, errors or poor coding practices directly within the code.

A static analysis is one that is carried out without running the programme. The tool scans the project files, interprets the code and looks for dangerous patterns. The main advantages of SAST are:
- It detects errors at an early stage.

- It does not require the application to be run.

- It helps developers correct poor coding practices.

- It can be easily automated.

- It allows large amounts of code to be reviewed.

- It improves the overall security of the project.

SAST also has limitations. It can generate false positives, i.e. alerts that appear to be vulnerabilities but are not actually vulnerabilities. It may also fail to fully understand the application’s runtime context. For this reason, SAST does not replace other security tests, but rather complements them.

Although SAST focuses primarily on analysing source code, many modern tools also review dependencies. An outdated dependency may contain known vulnerabilities.

### Secret Scanning
Secret scanning is the process of searching for secrets within a repository’s code and history. A ‘secret’ is any sensitive data that should not be made public. Git stores the complete history of changes made to a repository. This means that when you make a commit, Git stores a specific version of the files at that point in time. If you upload a token in one commit and then delete it in a later commit, the token disappears from the current code, but not necessarily from the history. Anyone with access to the repository could review old commits and find that secret.

Git works like a timeline. Each commit represents a snapshot of the project at a specific point in time. Even if the current file is clean, old commits may still contain sensitive information. That is why it is said that the problem lies not only in the current code, but also in the metadata and history of the repository. If a secret has been uploaded to Git, it is safest to assume that that secret is already compromised. Secrets should not be stored directly in the source code.

### Exercise 1: Install gitleaks (a secret scanner) and horusec or trivy (for file system analysis) on your local machine.
First, we update Ubuntu Server and install the basic tools:

```
sudo apt update
sudo apt install -y git curl wget gnupg python3
```

We install Gitleaks:

```
cd /tmp
GITLEAKS_VERSION=$(curl -s https://api.github.com/repos/gitleaks/gitleaks/releases/latest | grep “‘tag_name’:” | cut -d “"” -f 4)
wget ‘https://github.com/gitleaks/gitleaks/releases/download/${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION#v}_linux_x64.tar.gz’
tar -xzf ‘gitleaks_${GITLEAKS_VERSION#v}_linux_x64.tar.gz’
sudo mv gitleaks /usr/local/bin/
gitleaks version
```

![gitleaks_version](img/gitleaks_version.png)

We install Trivy:

```
sudo apt-get install -y wget gnupg

wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null

echo ‘deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main’ | sudo tee /etc/apt/sources.list.d/trivy.list

sudo apt-get update
sudo apt-get install -y trivy

trivy --version
```

![trivy_version](img/trivy_version.png)

### Exercise 2: Set up a pre-commit script in Git within your Python application repository.
We create the directory and file structure:

![app](img/app.png)

- **`def main():`:** Creates the programme’s main function.

- **`print(‘Python security lab is running’)`:** Displays a message on screen.

- **`if __name__ == ‘__main__’:`:** Ensures that main() only runs if you run this file directly.

![gitleaks](img/gitleaks.png)

- **`[extend]
useDefault = true`:** Keeps the default Gitleaks rules active.

- **`regex = “”'AWS_SECRET_KEY\s*=\s*[‘“]AKIA[0-9A-Z]{16}[’”]'“”`:** Detects a simulated key in this format: `AWS_SECRET_KEY=‘AKIAIOSFODNN7EXAMPLE’`

We commit the changes:

![git_commit](img/git_commit.png)

Finally, we create the hook and grant it execution permissions:

![pre-commit](img/pre-commit.png)

![chmod](img/chmod.png)

- **`gitleaks git --pre-commit --staged --redact --verbose --config .gitleaks.toml`:** Scans the files staged for commit.

- **`if [ $? -ne 0 ]; then`:** Checks whether Gitleaks has found a problem.

- **`exit 1`:** Blocks the commit.

- **`exit 0`:** Allows the commit if there are no secrets.

### Exercise 3: Add a commented line to your code that simulates a real AWS private key: AWS_SECRET_KEY="AKIAIOSFODNN7EXAMPLE".
We modify `app.py` to cause an error:

![app_v2](img/app_v2.png)

Although it is commented out, it is still text within the file. Gitleaks does not check whether the code is executed or not. It searches for secrets within the repository’s contents.

### Exercise 4: Try to make a git commit. Your gitleaks hook should analyse the change, intercept the fake secret, automatically abort the commit and display an alert in your terminal.
We try to commit and see that it’s going to give us an error, thanks to Gitleaks:

![git_commit_2](img/git_commit_2.png)