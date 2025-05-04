import os
import subprocess
from modules.log_module import Log

class Cloc(Log):
    # Cloc exclusions
    CLOC_CONFIG: dict = {
        "solidity": {
            "extension": "sol",
            "exclude_dirs": ["node_modules", "libs?", "tests?", "mocks?", "scripts?", "interfaces?", "uniswap", "openzeppelin", "curve"],
            "exclude_files": ["[Ss]cripts?", "[Ii]nterfaces?", "[Mm]ocks?", "[Tt]ests?"]
        }
    }
    

    def __init__(self, repo_path: str, slack_message: dict) -> None:
        """
        Initialize the cloc handler with the path to the cloned repository
        Args:
            repo_path (str): The path to the cloned repository
            language (str): The language of the repository
            commit (str): The commit hash to count from
            branch (str): The branch to count from
            scope (str): The scope of the files or directories to count from
            exclude_dirs (str): The directories to exclude from the count
            exclude_files (str): The files to exclude from the count
        """
        self.repo_path: str = repo_path
        self.language: str = slack_message["Language"].lower()
        self.commit: str = slack_message.get("Commit", "latest")
        self.branch: str = slack_message.get("Branch", "main")
        self.scope = slack_message.get("Scope", "all")
        self.exclude_dirs: str = "|".join(self.CLOC_CONFIG[self.language]["exclude_dirs"])
        self.exclude_files:str = "|".join(self.CLOC_CONFIG[self.language]["exclude_files"])


    def __count_loc(self) -> str:
        """
        Count the lines of code in all solidity files across the protocol.
        Returns:
            str: The total lines of code
        """
        try:
            self.log_info("\nCounting lines of code...\n")
            result: str = subprocess.run(
                self.__construct_cloc_command(self.scope),
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            self.log_info(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as clocException:
            self.log_error("Error running cloc: ", str(clocException))
            return {}
        

    def __construct_cloc_command(self, scope) -> list[str]:
        """
        Construct the cloc command based on the scope.
        Args:
            scope (str): The scope of the files or directories to count from
        Returns:
            str: The cloc command
        """
        if ".sol" in scope[0]:  # check if the scope are files
            scope_files: str = "|".join(scope)
            return ["cloc", f"--include-ext={self.CLOC_CONFIG[self.language]["extension"]}", ".", "--by-file", f"--match-f={scope_files}", f"--not-match-d={self.exclude_dirs}", f"--not-match-f={self.exclude_files}"]
        elif ".sol" not in scope[0] and scope[0] == "all":  # check if the scope are directories
            scope_dirs: str = "|".join(scope)
            return ["cloc", f"--include-ext={self.CLOC_CONFIG[self.language]["extension"]}", ".", "--by-file", f"--match-d={scope_dirs}", f"--not-match-d={self.exclude_dirs}", f"--not-match-f={self.exclude_files}"]
        return ["cloc", f"--include-ext={self.CLOC_CONFIG[self.language]["extension"]}", ".", "--by-file", f"--not-match-d={self.exclude_dirs}", f"--not-match-f={self.exclude_files}"]


    def get_cloc_result(self) -> str:
        """
        Get the result of the cloc command
        Returns:
            str: The result of the cloc command
        """
        return f"""```{self.__count_loc()}```\nCode formatted\nBranch: {self.branch}\nCommit: {self.commit}"""



        
