# Shefaz Been Rahim — professional portfolio

A static one-page portfolio for external audit and IFRS-related professional opportunities.

## Website files

Edit `index.html`, `styles.css`, and `script.js`. No npm packages or application server are required for the public website. Only these files and `.nojekyll` are included in the Pages artifact.

## GitHub-hosted development environment

Open the repository with **Code → Codespaces** to use a browser editor and Bash terminal. The dev container uses GitHub's default Linux image, which includes Git, GitHub CLI, Python, Node.js, and npm. The configuration verifies the tools and checks the site when the environment is created.

Preview from the repository root:

```sh
python3 -m http.server 8000
```

Open the forwarded port shown in Codespaces. Keep the preview port private. Codespaces compute usage is separate from Pages hosting; check your included allowance before starting a codespace.

## Validation and deployment

```sh
node --check script.js
python3 scripts/check_site.py
```

The Actions workflow provisions Node.js 24 and Python 3.12, validates the page, packages the public files, and deploys updates from `main` to GitHub Pages. Pull requests run validation without deployment.

Configure **Settings → Pages → Source → GitHub Actions**. The workflow uses GitHub's automatic workflow token and deployment identity; no personal token is stored in the repository.

On GitHub Free, this Pages route uses a public repository. A project site uses `https://ACCOUNT.github.io/REPOSITORY/`; an account site uses a repository named `ACCOUNT.github.io`. The final deployed address must be confirmed after a successful deployment.
