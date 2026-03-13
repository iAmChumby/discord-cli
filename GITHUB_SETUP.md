# Discord CLI - GitHub Setup Instructions

The discord-cli repo is ready to push to GitHub!

## Quick Setup

1. **Create the GitHub repo**
   ```bash
   # Option A: Create via GitHub web interface
   # Go to https://github.com/new
   # Repository name: discord-cli
   # Description: System-wide Discord CLI for OpenClaw agents and automation
   # Public
   # Initialize with: README.md
   # Then create the repo

   # Option B: Use GitHub CLI (if installed)
   gh repo create iAmChumby/discord-cli --public --source=. --description="System-wide Discord CLI for OpenClaw agents and automation"
   ```

2. **Push to GitHub**
   ```bash
   cd /home/chumby/discord-cli
   git remote add origin https://github.com/iAmChumby/discord-cli.git
   git branch -M main
   git push -u origin main
   ```

3. **Verify the repo**
   - Visit https://github.com/iAmChumby/discord-cli
   - Check that all files are there
   - README.md should display correctly

## What's Included

- ✅ `discord_cli.py` — Main CLI executable
- ✅ `README.md` — Comprehensive documentation
- ✅ `LICENSE` — MIT license
- ✅ `docs/` — Agent integration guide, quick reference, API reference
- ✅ `.github/` — Issue and PR templates
- ✅ `.gitignore` — Python gitignore

## Next Steps After Push

1. **Add v1.0.0 release tag**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Update the token**
   - Currently token is hardcoded in `discord_cli.py`
   - Next version: use `DISCORD_BOT_TOKEN` environment variable
   - Update the hardcoded token to your actual bot token

3. **Consider GitHub Actions**
   - Add CI/CD workflow
   - Add release automation
   - Add documentation deployment

4. **Integration with openclaw-notes**
   - Add this repo as a submodule or reference
   - Update TOOLS.md to point to this repo
   - Document for future agents

## For OpenClaw Integration

The CLI is installed at `~/.local/bin/discord-cli` for system-wide use. The GitHub repo serves as:
- Source of truth for the CLI
- Documentation for agent developers
- Version control and releases
- Issue tracking and contributions

## Quick Links

- **Repo URL:** https://github.com/iAmChumby/discord-cli
- **Issue Tracker:** https://github.com/iAmChumby/discord-cli/issues
- **Documentation:** https://github.com/iAmChumby/discord-cli/blob/main/README.md

---

Ready to push! Let me know if you need help with any of these steps.
