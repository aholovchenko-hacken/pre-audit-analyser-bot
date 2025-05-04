import os
import subprocess
import json
from pathlib import Path
from modules.log_module import Log

class Framework(Log):
     # Framework definitions with their detection files and potential variants
    FRAMEWORK_DEFINITIONS: dict = {
        "hardhat": {
            "config_files": ["hardhat.config.ts", "hardhat.config.js"],
            "dependencies": ["npm", "install"]
        },
        "foundry": {
            "config_files": ["foundry.toml", "remappings.txt"],
            "dependencies": ["forge", "install"]
        },
        "truffle": {  # Added for extensibility
            "config_files": ["truffle-config.js", "truffle.js"],
            "dependencies": ["npm", "install"]
        }
    }


    def __init__(self, repo_path: str) -> None:
        """
        Initialize the framework handler with the path to the cloned repository
        """
        self.repo_path: str = repo_path
        self.framework: str


    def detect_framework(self) -> str:
        """
        Detects which framework is being used in the project

        Returns:
            str: Framework name ('hardhat', 'foundry', 'truffle', or 'unknown')
        """
        for framework_name, framework_info in self.FRAMEWORK_DEFINITIONS.items():
            for config in framework_info["config_files"]:
                config_path = Path(self.repo_path) / config
                if config_path.exists():
                    self.framework = framework_name
                    self.log_info("\nDetected framework: ", framework_name)
                    return framework_name
        # If no framework is detected, return "unknown"
        self.log_error("No known framework detected (neither Hardhat nor Foundry)")
        return "unknown"
    
    
    def __install_dependencies(self) -> bool:
        """
        Installs dependencies for a specific framework

        Args:
            framework_name (str): Name of the framework to install dependencies for
            
        """
        self.log_info("Installing dependencies for ", self.framework)
        try:
            subprocess.run(
                self.FRAMEWORK_DEFINITIONS[self.framework]["dependencies"],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            self.log_info("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.log_error("Error installing dependencies: ", str(e))
            return False
        

    def __create_prettier_config(self) -> bool:
        """
        Creates a .prettierrc configuration file for the detected framework

        Returns:
            bool: True if Prettier configuration was created successfully, False otherwise
        """
        try:
            prettierrc_path: Path = Path(self.repo_path) / ".prettierrc" # in the future we can search among all folders for .prettierrc file
            if prettierrc_path.exists():
                self.log_info("Prettier configuration already exists, no need to create a new one")
                return True
            else: 
                self.log_info("Creating Prettier configuration...")
                prettier_config_path: Path = Path(__file__).parent.parent.parent / "prettier_config" / "config.json"
                # Load the JSON configuration
                with open(prettier_config_path, "r") as config_file:
                    prettier_config_data: dict = json.load(config_file)
                # Write the configuration using Path.write_text()
                prettierrc_path.write_text(json.dumps(prettier_config_data, indent=2))
                self.log_success("Prettier configuration created successfully")
                return True
        except Exception as e:
            self.log_error("Error creating Prettier configuration:", str(e))
            return False
        
        
    def __setup_formatter(self) -> bool:
        """
        Sets up a formatter for the detected framework

        Returns:
            bool: True if formatter was setup successfully, False otherwise
        """
        try:
            if self.framework == "hardhat":
                result = subprocess.run(
                    ["npm", "list", "--depth=0", "prettier"],
                    cwd=self.repo_path,
                    check=False,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0 and "prettier" in result.stdout: 
                    self.log_info("Prettier is already installed")
                    self.__create_prettier_config()
                    return True
                else:
                    self.log_info("Installing Prettier...")
                    subprocess.run(
                        ["npm", "install", "prettier", "prettier-plugin-solidity"],
                        cwd=self.repo_path,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    self.log_success("Prettier installed successfully")
                    self.__create_prettier_config()
                    return True
            elif self.framework == "foundry":
                self.log_info("Foundry framework don't need formatter detection")
                return True
        except subprocess.CalledProcessError as e:
            self.log_error("Error setting up formatter: ", str(e))
            return False
            
            
    def __run_formatter(self) -> bool:
        """
        Runs the formatting command for the detected framework

        Returns:
            bool: True if code was formatted successfully, False otherwise
        """
        try:
            if self.framework == "hardhat":
                subprocess.run(
                    ["npx", "prettier", "--write", "**/*.sol"],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True,
                    text=True
                )
                self.log_success("Hardhat code formatted successfully\n")
                return True
            elif self.framework == "foundry":
                # Create a copy of the current environment
                env: dict = os.environ.copy()
                # Set the environment variable
                env["FOUNDRY_FMT_LINE_LENGTH"] = "80"

                subprocess.run(
                    ["forge", "fmt"],
                    cwd=self.repo_path,
                    env=env, # Pass the modified environment
                    check=True,
                    capture_output=True,
                    text=True
                )
                self.log_success("Foundry code formatted successfully\n")
                return True
        except subprocess.CalledProcessError as e:
            self.log_error("Error formatting code: ", str(e))
            return False
        
        
        
    def format_code(self) -> bool:
        """
        Formats the code for the detected framework

        Returns:
            bool: True if code was formatted successfully, False otherwise
        """
        self.__install_dependencies()
        self.__setup_formatter()
        self.__run_formatter()
