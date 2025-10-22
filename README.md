# Portfolio website (GitHub Pages)

This repository contains a polished static portfolio website for Anish Mulay meant to be published via GitHub Pages. It includes an index, styles, and small JS interactions. The CV PDF is included and linked from the site.

Files added
- `index.html` — main site
- `assets/css/style.css` — styles
- `assets/js/main.js` — small interactions (theme toggle, year)
- `anish_cv (9).pdf` — your CV (already present in the workspace)

How to publish on GitHub Pages

1. Create a new repository on GitHub (e.g., `anish-portfolio`).
2. In your local workspace, initialize git and push the files:

```powershell
cd "c:\Users\Anish Mulay\Documents\Portfolio website"
git init
git add .
git commit -m "Initial portfolio site"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

3. In the GitHub repo settings -> Pages, set the source to the `main` branch and root (or use `gh-pages` branch if you prefer). Wait a moment and your site will be live at `https://your-username.github.io/your-repo/`.

Notes & next steps
- Replace placeholder text (email, location, project details) in `index.html` with your real information.
- Add real project links and publications. Consider adding a `publications.html` or linking to your Google Scholar.
- For a custom domain, add a `CNAME` file with the domain and configure DNS.
- If you want automated deploys from different branches, ask and I can add a GitHub Action.
