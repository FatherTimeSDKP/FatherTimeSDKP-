import os
import json
import hashlib
from datetime import datetime

class DigitalCrystalProtocol:
    def __init__(self, ledger_path='timeseal_log_extended.json'):
        # [span_0](start_span)Authorship metadata from the Unified Scientific Authorship Ledger[span_0](end_span)
        self.author = "Donald Paul Smith"
        self.alias = "Father Time"
        self.orcid = "0009-0003-7925-1653"
        self.doi = "https://doi.org/10.5281/zenodo.14850016"
        self.ledger_path = ledger_path
        self.principles = ["SDKP", "EOS", "SD&N", "QCC", "SDVR"]

    def _get_comment_style(self, ext):
        """Maps file extensions to appropriate comment syntax."""
        styles = {
            '.py': ('"""', '"""'),
            '.js': ('/**', ' */'),
            '.cpp': ('/*', ' */'),
            '.tex': ('%', ''),
            '.md': (''),
            '.html': (''),
            '.txt': ('', '')
        }
        return styles.get(ext.lower(), ('', ''))

    def update_ledger(self, module_name, entry_hash):
        """Appends a new TimeSeal record to the JSON ledger."""
        new_entry = {
            "module": module_name,
            "timestamp": datetime.utcnow().isoformat(),
            "author": self.author,
            "alias": self.alias,
            "ai_validated": True,
            "nft_protected": True,
            "time_seal": True,
            "entry_hash": entry_hash
        }

        try:
            if os.path.exists(self.ledger_path):
                with open(self.ledger_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []

            data.append(new_entry)

            with open(self.ledger_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"[!] Ledger Update Error: {e}")
            return False

    def propagate(self, file_path):
        [span_1](start_span)"""Applies protocol, wraps in comments, and records the TimeSeal[span_1](end_span)."""
        try:
            file_name = os.path.basename(file_path)
            _, ext = os.path.splitext(file_path)
            start_comment, end_comment = self._get_comment_style(ext)

            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            if self.alias in original_content:
                print(f"[-] Protocol already active in {file_name}")
                return

            # Construct Protocol Header
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            header = (
                f"\nDigital Crystal Protocol FTS-AUTH-CRYSTAL-369\n"
                f"Copyright © 2025 {self.author} ({self.alias}). All Rights Reserved.\n"
                f"Citation: {self.doi} | ORCID: {self.orcid}\n"
                f"Principles: {', '.join(self.principles)}\n"
                f"Verification: fathertimesdkp.blockchain/records/2025-05-18\n"
                f"TimeSeal Date: {timestamp}\n"
                f"{'-' * 57}\n"
            )
            
            full_header = f"{start_comment}{header}{end_comment}\n\n"
            new_content = full_header + original_content
            
            # Generate Cryptographic TimeSeal
            entry_hash = hashlib.sha256(new_content.encode('utf-8')).hexdigest()

            # Save modified file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Update Ledger
            if self.update_ledger(file_name, entry_hash):
                print(f"[+] Protocol Sealing Complete: {file_name}")
                print(f"    New TimeSeal Hash: {entry_hash}")
            
        except Exception as e:
            print(f"[!] Protocol Error on {file_path}: {e}")

# Implementation for batch processing your research directory
def run_protocol_on_project(directory):
    protocol = DigitalCrystalProtocol()
    valid_extensions = ['.py', '.tex', '.md', '.txt']
    
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in valid_extensions):
                protocol.propagate(os.path.join(root, file))

if __name__ == "__main__":
    # Example: run_protocol_on_project("./my_research_folder")
    pass
