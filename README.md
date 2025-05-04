# Pre Audit Analyser Bot
A Python-powered Slack bot for analyzing Solidity protocols.  
This bot can detect frameworks, count lines of code, and provide protocol analysis for Solidity codebases, all from within your Slack workspace.

## Important Information And Ideal Work Condition
### Important Information To Note
1. **!** Bot atm can work only with GitHub repositories that have inside a development framework. 
2. Bot doesn't work with repositories or files archived in **.zip** format.
3. Bot doesn't work the links from **Etherscan** or any other blockchain scanner.
### Ideal Work Condition
1. Client provide a **repository with development framework**.
2. Client provide a **clear branch and commit** for audit.
3. Client provide a **clear scope** for audit.
## Tech Stack
- **Python**  
  Core language for the bot logic and Slack integration.
- **Flask**\
  For running a local server.
- **Slack SDK for Python**  
  Handles Slack events, messaging, and authentication.

## Features
- **Framework Detection:**  
  Automatically detects if your project uses Hardhat, Foundry, or other supported frameworks(atm support only Hardhat and Foundry, but in the future we can add smth for Rust like Anchor or Cargo).
- **GitHub Repository Handling:**\
  Automatically clones the needed repository to a temporary directory and switches to a needed branch and commit.
- **Line of Code Counting:**  
  Uses [`cloc`](https://github.com/AlDanial/cloc) to count lines of code in your Solidity files, with support for custom file and directory scopes.
- **Protocol Analysis:**  
  Analyzes Solidity code snippets or files and provides feedback or summaries directly in Slack threads.
- **Threaded Replies:**  
  All bot responses are posted as threaded replies to keep your channels clean.
  Each message is processed only once, preventing spam multiple replies. 

## What Languages Bot Can Work With?
1. **Solidity**.

## Which Scope Bot Can Cover?
In the sections below I will show message examples for all these types of scope.
1. **All files in protocol**. Means that the client needs to audit all files in the protocol.
2. **Only specific files**. Means that client only needs an audit of specific files from his protocol.
3. **Only specific directories**. Means that client only needs an audit of specific directories from his protocol.

## What Languages Bot Can Not Work With?
Below information will be changed once new features will be added.
1. **Rust** - coming soon.
2. **FunC** - maybe it will come soon.
3. **Move** - maybe it will come soon.

## Which Scope Bot Can Not Cover?
Below information will be changed once new features will be added.
1. Scope when client provides both specific directories and specific files inside these directories.
2. Scope when client provides both directories and individual files(means not from provided directories).

## Usage
1. Bot is added to the chat.
2. Users send a message with required structure(provided below) to the chat with information he/she received from the client regarding the github repo, branch, commit, scope, etc.
3. Bot listens to this channel for a message.
4. Bot fetch information from the message and start analysis(cloning, installing dependencies, calculating cloc, etc...).
5. Once the bot calculates a cloc, it replies for this message in thread with cloc result + basic additional information.

## Message Structure
I propose the next message structure to give bot a chance to help us.\
Important fields will be marked with **[Imp]**
```
https://hacken.atlassian.net/browse/SPE-0000        -- Ticket link. Needed just for us to check the task. Bot do not use it.       

Client: stHAI                                       -- Client Name [Imp]
Language: Solidity                                  -- Language that client protocol is using. Solidity only at the moment [Imp]
Repo: git@github.com:hknio/stHAI-contract.git       -- Repository SSH link, not HTTPS [Imp]
Scope: stHai.sol, blabla.sol, fgfg.sol              -- Scope for audit. If not provided, then bot defaults to the scope of 'all' contract files in the project.
Branch: dev                                         -- Branch for audit. If not provided, then bot defaults to the 'main' branch.
Commit:  943c9d69ba35ddcafad4fad4d43ca7709c869002   -- Commit for audit. If not provided, then bot defaults to the 'latest' commit. 
```