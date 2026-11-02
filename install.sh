#!/usr/bin/env bash
# Installs the research synthesizer into Claude Code: the research-synthesizer and
# research-verifier agents, and the /synthesize skill.
#
#   ./install.sh      installs into ~/.claude (set CLAUDE_DIR to install elsewhere)
#
# Existing agents are kept as agents/<name>.md.bak.<stamp>, and an existing skill as
# backups/synthesize.<stamp>/, outside skills/ so the copy doesn't load as a second /synthesize.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
STAMP="$(date +%Y%m%d-%H%M%S)"

echo "Installing the research synthesizer into $CLAUDE_DIR"
mkdir -p "$CLAUDE_DIR/agents" "$CLAUDE_DIR/skills"
for agent in research-synthesizer research-verifier; do
  if [ -f "$CLAUDE_DIR/agents/$agent.md" ]; then
    cp "$CLAUDE_DIR/agents/$agent.md" "$CLAUDE_DIR/agents/$agent.md.bak.$STAMP"
    echo "  kept the old agent as agents/$agent.md.bak.$STAMP"
  fi
  cp "$HERE/agents/$agent.md" "$CLAUDE_DIR/agents/$agent.md"
done
if [ -d "$CLAUDE_DIR/skills/synthesize" ]; then
  mkdir -p "$CLAUDE_DIR/backups"
  mv "$CLAUDE_DIR/skills/synthesize" "$CLAUDE_DIR/backups/synthesize.$STAMP"
  echo "  kept the old skill as backups/synthesize.$STAMP"
fi
cp -R "$HERE/skills/synthesize" "$CLAUDE_DIR/skills/synthesize"
echo "  wrote agents/research-synthesizer.md, agents/research-verifier.md and skills/synthesize/"

echo "Checking"
if command -v python3 >/dev/null 2>&1; then
  echo "  quote gate self-test: $(python3 "$CLAUDE_DIR/skills/synthesize/scripts/check_quotes.py" --selftest | tail -1)"
else
  echo "  Python 3 not found: the quote gate needs it. The agents still run; the loop skips the script check."
fi

echo
echo "Next: open a new Claude Code session (or type /reload-skills), then run /synthesize <your notes folder>."
echo "Try it first on the example: cd $HERE/example, then /synthesize notes/"
