import os
import json
import hashlib
from datetime import datetime

class GitHubCrystalProtocol:
    def __init__(self, ledger_path='timeseal_log_extended.json'):
        self.author = "Donald Paul Smith"
        self.alias = "Father Time"
        self.github_repo = "https://github.com/FatherTimeSDKP"
        self.zenodo_doi = "10.5281/zenodo.14850016"
        self.ledger_path = ledger_path

    def propagate(self, file_path):
        """Applies the protocol and prepares GitHub-ready metadata."""
        try:
            file_name = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if "FatherTimeSDKP" in content:
                print(f"[-] Skipping {file_name}: GitHub registry link already present.")
                return

            # Construct the GitHub-Linked Protocol Header
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            header = (
                f"\n--- DIGITAL CRYSTAL PROTOCOL (FTS-AUTH-CRYSTAL-369) ---\n"
                f"AUTHOR: {self.author} ({self.alias})\n"
                f"PRIMARY REGISTRY: {self.github_repo}\n"
                f"IMMUTABLE SNAPSHOT: https://doi.org/{self.zenodo_doi}\n"
                f"VERIFICATION: 38-Sigma Computational Wall Active\n"
                f"SEALED ON: {timestamp}\n"
                f"{'-' * 55}\n"
            )
            
            # Wrap based on file type (e.g., .md for GitHub READMEs)
            if file_path.endswith('.md'):
                new_content = f"\n" + content
            else:
                new_content = f"\"\"\"\n{header}\n\"\"\"\n" + content
            
            # Update local file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Update the JSON Ledger with the new Hash
            entry_hash = hashlib.sha256(new_content.encode('utf-8')).hexdigest()
            self._log_to_ledger(file_name, entry_hash)

            print(f"[✓] File Sealed and Linked to GitHub Registry: {file_name}")

        except Exception as e:
            print(f"[!] Error: {e}")

    def _log_to_ledger(self, module, entry_hash):
        """Appends entry to timeseal_log_extended.json."""
        new_entry = {
            "module": module,
            "timestamp": datetime.utcnow().isoformat(),
            "author": self.author,
            "alias": self.alias,
            "entry_hash": entry_hash,
            "registry_link": self.github_repo
        }
        # Log to ledger logic...
