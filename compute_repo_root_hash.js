// compute_repo_root_hash.js
// Usage:
//   node compute_repo_root_hash.js file1 file2 ...
//   node compute_repo_root_hash.js ./   (scans current dir for the default files below)

const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

const defaultFiles = [
  'ledger.json',
  'ledger.md',
  'ledger.yaml',
  'ipfs_metadata.txt',
  'qcc0_bias_repro.py',
  'grok_interaction_sam.json'
];

function sha256Hex(buffer) {
  return crypto.createHash('sha256').update(buffer).digest('hex');
}

async function main() {
  const args = process.argv.slice(2);
  let files = args.length ? args : defaultFiles;

  // If a directory passed, resolve to default files within it
  if (files.length === 1 && fs.existsSync(files[0]) && fs.statSync(files[0]).isDirectory()) {
    const dir = files[0];
    files = defaultFiles.map(f => path.join(dir, f));
  }

  const entries = [];
  for (const f of files) {
    if (!fs.existsSync(f)) {
      console.warn(`Warning: file not found: ${f}`);
      continue;
    }
    const data = fs.readFileSync(f);
    const h = sha256Hex(data);
    const fname = path.basename(f);
    entries.push({ name: fname, hash: h });
    console.log(`${fname}  ${h}`);
  }

  if (entries.length === 0) {
    console.error('No files hashed. Exiting.');
    process.exit(1);
  }

  // Sort entries by filename to canonicalize
  entries.sort((a,b) => a.name.localeCompare(b.name));

  // Build canonical concatenation string: "filename:hash\n" per line
  const concat = entries.map(e => `${e.name}:${e.hash}`).join('\n');

  // Final root hash
  const root = sha256Hex(Buffer.from(concat, 'utf8'));
  console.log('\n=== CANONICAL REPOSITORY ROOT HASH ===');
  console.log(root);
  console.log('\nCanonical string used for hash:\n', concat);
}

main();
