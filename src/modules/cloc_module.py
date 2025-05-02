import subprocess
from modules.log_module import Log

class Cloc(Log):
    # Cloc definitions
    CLOC_DEFINITIONS: dict = {
        "hardhat": {
            "extension": "sol",
            "exclude": ["node_modules", "tests?", "mocks?", "uniswap", "interfaces?", "openzeppelin", "curve"]
        },
        "foundry": {
            "extension": "sol",
            "exclude": ["lib", "tests?", "mocks?", "scripts?", "interfaces?", "uniswap", "openzeppelin", "curve"]
        }
    }


    def __init__(self, repo_path: str) -> None:
        """
        Initialize the cloc handler with the path to the cloned repository
        """
        self.repo_path: str = repo_path
    

    def count_lines_of_code_full_scope(self, framework: str) -> str:
        """
        Count the lines of code in the solidity files for the given framework in the full scope of the repository.
        The total lines of code is returned.
        """
        if framework not in self.CLOC_DEFINITIONS:
            raise ValueError(f"Framework {framework} not found in available frameworks")
        
        exclusion: str = "|".join(self.CLOC_DEFINITIONS[framework]["exclude"])
        
        try:
            self.log_info("Counting lines of code...\n")
            result: str = subprocess.run(
                ["cloc", f"--include-ext={self.CLOC_DEFINITIONS[framework]["extension"]}", ".", "--by-file", f"--not-match-d={exclusion}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            self.log_info(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as clocException:
            self.log_error("Error running cloc: ", str(clocException))
            return {}
