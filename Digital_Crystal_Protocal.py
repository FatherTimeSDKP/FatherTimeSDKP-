import os
import hashlib
from datetime import datetime

class DigitalCrystalProtocol:
    def __init__(self):
        # [span_1](start_span)Authorship metadata based on Unified Scientific Authorship Ledger[span_1](end_span)
        self.author = "Donald Paul Smith (FatherTime)"
        self.orcid = "0009-0003-7925-1653"
        self.doi = "https://doi.org/10.5281/zenodo.14850016"
        [span_2](start_span)[span_3](start_span)self.principles = ["SDKP", "EOS", "SD&N", "QCC", "SDVR"] #[span_2](end_span)[span_3](end_span)

    def _get_comment_style(self, ext):
        """Maps file extensions to their appropriate comment syntax."""
        styles = {
            '.py': ('"""', '"""'),
            '.js': ('/**', ' */'),
            '.cpp': ('/*', ' */'),
            '.tex': ('%', ''),
            '.md': (''),
            '.html': ('')
        }
        return styles.get(ext.lower(), ('', ''))

    def generate_authorship_text(self, file_path):
        """Creates the protocol-compliant header with a live timestamp."""
        [span_4](start_span)timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC') #[span_4](end_span)
        
        return f"""
# Digital Crystal Protocol FTS-AUTH-CRYSTAL-369
# Copyright © 2025 {self.author}. All Rights Reserved.
# Citation: {self.doi} | ORCID: {self.orcid}
# Principles: {", ".join(self.principles)}
# Verification Timestamp: {timestamp}
# Registry: fathertimesdkp.blockchain/records/2025-05-18
---------------------------------------------------------
"""

    def generate_timeseal_hash(self, content):
        """Generates a SHA-256 hash to act as an entry_hash for the ledger."""
        # Mirrors the integrity checks in timeseal_log_extended.json
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def propagate(self, file_path):
        """Applies the protocol, wraps in comments, and calculates the TimeSeal."""
        try:
            _, ext = os.path.splitext(file_path)
            start_comment, end_comment = self._get_comment_style(ext)

            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # [span_5](start_span)Prevent double-stamping[span_5](end_span)
            if self.author in original_content:
                print(f"[-] Protocol already active in {file_path}")
                return

            header = self.generate_authorship_text(file_path)
            # Final content construction
            full_header = f"{start_comment}{header}{end_comment}\n\n"
            new_content = full_header + original_content
            
            # Generate TimeSeal
            entry_hash = self.generate_timeseal_hash(new_content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"[+] Protocol Sealing Complete: {file_path}")
            print(f"    TimeSeal Hash: {entry_hash}")
            
        except Exception as e:
            print(f"[!] Protocol Error: {e}")

# Example Usage
if __name__ == "__main__":
    protocol = DigitalCrystalProtocol()
    # protocol.propagate("research_draft.tex") # Applies to individual file
