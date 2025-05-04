import git
import os
import tempfile
import time
from datetime import datetime
from modules.log_module import Log

class Repository(Log):
    all = {}
    def __init__(self, repo_ssh: str, client: str, language: str, branch: str = "main", commit: str = "latest", scope: str = "all") -> None:
        if not all([client, repo_ssh, language]):
            raise ValueError("Client, repo_ssh, and language must be non-empty strings")

        self.repo_ssh: str = repo_ssh
        self.client: str = client
        self.language: str = language
        self.branch: str = branch
        self.commit: str = commit
        self.scope: str = scope
        self.timestamp: float = time.time()
        self.created_at: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.temp_dir: str = tempfile.mkdtemp(prefix=f"repo_clone_{self.client}") # create an instance 

        Repository.all[self.client] = {
            "repo_ssh": self.repo_ssh,
            "language": self.language,
            "branch": self.branch,
            "commit": self.commit,
            "scope": self.scope,
            "timestamp": self.timestamp,
            "created_at": self.created_at
        }


    def get_repo_info(self, client: str) -> dict:
        """
        Returns the repository info for a given client
        """
        assert len(client) > 0, "Client name is required"
        return Repository.all[client]


    def __get_modified_repo_ssh(self) -> str:
        """
        Returns the modified repository SSH URL for a given repository SSH URL(for this you need to set up your SSH keys)
        """
        return self.repo_ssh.replace("git@github.com:hknio", "git@github.com-hacken:hknio")


    def __checkout_branch(self, repo: git.Repo) -> None:
        """
        Checks out to a new branch if the client provided a branch name
        """
        if self.branch != "main":
            repo.git.checkout(self.branch)
            self.log_info("Checked out to branch: ", repo.active_branch.name)
        else:
            self.log_info("Defaulting to main.")
    

    def __checkout_commit(self, repo: git.Repo) -> None:
        """
        Checks out to a specific commit if the client provided a commit hash
        """
        if self.commit != "latest":
            repo.git.checkout(self.commit)
            self.log_info("Checked out to commit: ", repo.head.commit)
        else:
            self.log_info("Defaulting to latest commit.")


    def clone_repo(self) -> str:
        """
        Clones a repository to a temporary directory and returns the path
        """
        # Constructing a file path to an SSH key in the home directory | os.path.expanduser() - converts ~ into an absolute path like '/home/username/.ssh/'
        ssh_key_path = os.path.join(os.path.expanduser("~/.ssh/"), "id_rsa_hacken_1")
        # Modify the repo SSH URL if needed
        modified_repo_ssh = self.__get_modified_repo_ssh() 

        self.log_info("Cloning repository: ", modified_repo_ssh)

        # Store original environment
        original_env = os.environ.copy()

        try:
            # Create the SSH command with the specific key
            ssh_command = f"ssh -i {ssh_key_path} -o StrictHostKeyChecking=no"
            os.environ["GIT_SSH_COMMAND"] = ssh_command

            # Clone the repository using GitPython
            git.Repo.clone_from(modified_repo_ssh, self.temp_dir)
            repo = git.Repo(self.temp_dir)

            # Checkout to a specific branch and commit if provided
            self.__checkout_branch(repo)
            self.__checkout_commit(repo)

            self.log_success("Repository cloned successfully!")
        except git.GitCommandError as e:
            self.log_error("Failed to clone repository: ", {str(e)})
            return None
        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)