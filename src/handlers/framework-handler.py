import os
import subprocess
import json
from pathlib import Path

class Framework:
     # Framework definitions with their detection files and potential variants
    FRAMEWORK_DEFINITIONS = {
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
        self.repo_path = repo_path
        self.framework = self.detect_framework()


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
                    print(f"Detected {framework_name} framework")
                    return framework_name
        # If no framework is detected, return "unknown"
        print("No known framework detected (neither Hardhat nor Foundry)")
        return "unknown"
    
    
    def install_dependencies(self) -> bool:
        """
        Installs dependencies based on the detected framework

        Returns:
            bool: True if dependencies were installed successfully, False otherwise
        """
        print(f"Installing dependencies for {self.framework} framework...")
        self._install_dependencies(self.framework)

        
    def _install_dependencies(self, framework_name: str) -> bool:
        """
        Installs dependencies for a specific framework

        Args:
            framework_name (str): Name of the framework to install dependencies for
            
        """
        try:
            subprocess.run(
                self.FRAMEWORK_DEFINITIONS[framework_name]["dependencies"],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"{self.framework} dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            return False


framework: Framework = Framework("/Users/ah/Desktop/Hacken/Analysis/stHAI-contract")
     
framework.install_dependencies()