#!/usr/bin/env bash
# One-command setup and launch for the VPRO Skills Adaptive RAG Assistant (macOS / Linux).
#
#   bash start.sh               full setup, tests, build, then start both servers
#   bash start.sh --skip-checks skip backend tests and the frontend build (faster restarts)
#
# Stop both servers with Ctrl+C in this terminal.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"
VENV="$ROOT/.venv"
PY="$VENV/bin/python"
SKIP_CHECKS=0
[[ "${1:-}" == "--skip-checks" ]] && SKIP_CHECKS=1

step() { printf '\n\033[1;33m==> %s\033[0m\n' "$1"; }
ok()   { printf '    \033[32m✓\033[0m %s\n' "$1"; }
fail() {
  printf '\n\033[1;31mERROR:\033[0m %s\n' "$1" >&2
  printf '\033[1mFix:\033[0m %s\n' "$2" >&2
  exit 1
}

# 1. Toolchain -------------------------------------------------------------
step "Checking Python and Node.js"
PYTHON_BIN=""
for candidate in python3.11 python3.12 python3.13 python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 &&
     "$candidate" -c 'import sys; sys.exit(0 if (3, 10) <= sys.version_info[:2] < (3, 14) else 1)' 2>/dev/null; then
    PYTHON_BIN="$(command -v "$candidate")"
    break
  fi
done
[[ -n "$PYTHON_BIN" ]] || fail "Python 3.10–3.13 was not found." "Install Python 3.11 from https://www.python.org/downloads/ and re-run."
ok "$("$PYTHON_BIN" --version) ($PYTHON_BIN)"

command -v node >/dev/null 2>&1 || fail "Node.js was not found." "Install Node.js 20.19+ or 22+ from https://nodejs.org/ and re-run."
command -v npm >/dev/null 2>&1 || fail "npm was not found." "Reinstall Node.js (npm ships with it)."
node -e 'const [major, minor] = process.versions.node.split(".").map(Number);
  process.exit(major > 22 || (major === 22 && minor >= 12) || (major === 20 && minor >= 19) ? 0 : 1)' ||
  fail "Node.js $(node --version) is too old for Vite." "Install Node.js 20.19+ or 22.12+ and re-run."
ok "Node.js $(node --version), npm $(npm --version)"

# 2-3. Python environment and dependencies --------------------------------
step "Preparing Python virtual environment"
if [[ ! -x "$PY" ]]; then
  "$PYTHON_BIN" -m venv "$VENV" || fail "Could not create the virtual environment." "Install the venv module (e.g. 'sudo apt install python3-venv') and re-run."
  ok "Created .venv"
fi
REQ_HASH="$("$PY" -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$ROOT/requirements.txt")"
if [[ "$(cat "$VENV/.deps-installed" 2>/dev/null || true)" != "$REQ_HASH" ]]; then
  "$PY" -m pip install --upgrade pip >/dev/null
  "$PY" -m pip install -r "$ROOT/requirements.txt" ||
    fail "Installing Python dependencies failed (see the pip output above)." "Check your network connection, then run: $PY -m pip install -r requirements.txt"
  echo "$REQ_HASH" > "$VENV/.deps-installed"
  ok "Installed Python dependencies"
else
  ok "Python dependencies already up to date"
fi

# 4. Sample documents -------------------------------------------------------
step "Generating missing sample documents"
"$PY" "$BACKEND/scripts/create_sample_files.py" || fail "Sample document generation failed." "Run: $PY backend/scripts/create_sample_files.py"

# 5. Frontend dependencies --------------------------------------------------
step "Installing frontend dependencies"
if [[ ! -d "$FRONTEND/node_modules" || "$FRONTEND/package-lock.json" -nt "$FRONTEND/node_modules/.package-lock.json" ]]; then
  (cd "$FRONTEND" && npm ci) || fail "npm ci failed (see output above)." "Run: cd frontend && npm ci"
  ok "Installed frontend dependencies"
else
  ok "Frontend dependencies already up to date"
fi

# 6-8. Environment files -----------------------------------------------------
step "Checking configuration"
if [[ ! -f "$BACKEND/.env" ]]; then
  cp "$BACKEND/.env.example" "$BACKEND/.env"
  ok "Created backend/.env from .env.example"
else
  ok "backend/.env exists (left unchanged)"
fi
if [[ ! -f "$FRONTEND/.env" ]]; then
  cp "$FRONTEND/.env.example" "$FRONTEND/.env"
  ok "Created frontend/.env from .env.example"
fi
if ! grep -Eq '^OPENAI_API_KEY=.+' "$BACKEND/.env"; then
  printf '    \033[33m!\033[0m OPENAI_API_KEY is empty in backend/.env — the UI will start, but chat and indexing need a key.\n'
fi

env_value() { grep -E "^$1=" "$BACKEND/.env" 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"' \r' || true; }
API_HOST="$(env_value API_HOST)"; API_HOST="${API_HOST:-127.0.0.1}"
API_PORT="$(env_value API_PORT)"; API_PORT="${API_PORT:-8000}"

# 9-10. Checks ----------------------------------------------------------------
if [[ "$SKIP_CHECKS" -eq 0 ]]; then
  step "Running backend tests"
  (cd "$BACKEND" && "$PY" -m pytest) || fail "Backend tests failed (see output above)." "Fix the failing tests, or run 'bash start.sh --skip-checks' to start anyway."
  step "Building frontend (production check)"
  (cd "$FRONTEND" && npm run build) || fail "Frontend build failed (see output above)." "Run: cd frontend && npm run build"
else
  step "Skipping tests and build (--skip-checks)"
fi

# 11-12. Launch -------------------------------------------------------------
step "Starting servers"
BACKEND_PID=""
FRONTEND_PID=""
# Each server runs in its own process group (job control on), so cleanup can stop
# the whole tree: the venv python launcher and npm both spawn the real server as a child.
stop_group() { [[ -n "$1" ]] && kill -TERM -- "-$1" 2>/dev/null || true; }
cleanup() {
  trap - EXIT INT TERM
  printf '\nStopping servers...\n'
  stop_group "$FRONTEND_PID"
  stop_group "$BACKEND_PID"
  wait 2>/dev/null || true
  echo "Stopped."
}
trap cleanup EXIT INT TERM

set -m
"$PY" -m uvicorn main:app --app-dir "$BACKEND" --host "$API_HOST" --port "$API_PORT" &
BACKEND_PID=$!
(cd "$FRONTEND" && exec npm run dev) &
FRONTEND_PID=$!
set +m

sleep 3
cat <<EOF

  Adaptive RAG Assistant is running
    Frontend : http://localhost:5173
    Backend  : http://$API_HOST:$API_PORT   (API docs: http://$API_HOST:$API_PORT/docs)

  Press Ctrl+C to stop both servers.

EOF

# macOS ships bash 3.2 (no 'wait -n'), so poll: stop everything if either server exits.
while kill -0 "$BACKEND_PID" 2>/dev/null && kill -0 "$FRONTEND_PID" 2>/dev/null; do
  sleep 1
done
echo "A server exited unexpectedly; see the log output above." >&2
exit 1
