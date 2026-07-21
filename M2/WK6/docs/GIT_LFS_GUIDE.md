# Git LFS Guide for Large Model Artifacts

This repository now includes Git LFS tracking for common binary model files.

## Why use Git LFS

GitHub repositories have a 100 MB file size limit for normal Git commits.
Large model artifacts such as `*.pkl`, `*.h5`, `*.pt`, and `*.onnx` should be stored with Git LFS so the repo stays lightweight and push/pull works reliably.

## What was added

- `.gitattributes` configured to track:
  - `*.pkl`
  - `*.h5`
  - `*.pt`
  - `*.onnx`

## Setup steps

1. Install Git LFS:

   - macOS / Linux:

     ```bash
     brew install git-lfs
     git lfs install
     ```

   - Windows:

     ```powershell
     winget install --id Git.GitLFS
     git lfs install
     ```

2. Verify Git LFS is enabled:

   ```bash
   git lfs install --force
   git lfs version
   ```

3. Track binary files in this repository:

   ```bash
   git lfs track "*.pkl"
   git lfs track "*.h5"
   git lfs track "*.pt"
   git lfs track "*.onnx"
   ```

4. Commit the `.gitattributes` file:

   ```bash
   git add .gitattributes
   git commit -m "Add Git LFS tracking for model artifacts"
   git push origin main
   ```

## How to add a new model file

Save the file under your project folder, for example:

```python
import joblib
joblib.dump(model, "models/telco_bayes_lr_v1.pkl")
```

Then add and push normally:

```bash
git add models/telco_bayes_lr_v1.pkl
git commit -m "Add trained telco model artifact"
git push origin main
```

Git LFS will store the file content outside the normal Git object storage.

## If you already committed a large file

If a large file was accidentally committed, remove it from Git history before pushing:

```bash
git rm --cached path/to/large-file.pkl
git commit -m "Remove oversized model artifact"
git push origin main
```

If the file is still present in history and needs migration, use:

```bash
git lfs migrate import --include="*.pkl,*.h5,*.pt,*.onnx"
```

> Note: `git lfs migrate` rewrites history. Use it carefully and only after verifying that collaborators are aware.

## Cloning this repo in the future

When you clone the repo, run:

```bash
git lfs install
git clone <repo-url>
```

Git LFS-aware clients will automatically download the tracked binary files.

## Best practice

- Keep large binary artifacts out of regular Git when possible.
- Store trained models or checkpoints in cloud storage if they are extremely large.
- Use Git LFS only for files that need versioned history at the repo level.
