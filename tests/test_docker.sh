#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

IMAGE_NAME="abot-test"

echo "=== Building Docker image ==="
docker build -t "$IMAGE_NAME" .

echo ""
echo "=== Running 'abot onboard' ==="
docker run --name abot-test-run "$IMAGE_NAME" onboard

echo ""
echo "=== Running 'abot status' ==="
STATUS_OUTPUT=$(docker commit abot-test-run abot-test-onboarded > /dev/null && \
    docker run --rm abot-test-onboarded status 2>&1) || true

echo "$STATUS_OUTPUT"

echo ""
echo "=== Validating output ==="
PASS=true

check() {
    if echo "$STATUS_OUTPUT" | grep -q "$1"; then
        echo "  PASS: found '$1'"
    else
        echo "  FAIL: missing '$1'"
        PASS=false
    fi
}

check "abot Status"
check "Config:"
check "Workspace:"
check "Model:"
check "OpenRouter:"
check "Anthropic:"
check "OpenAI:"

echo ""
if $PASS; then
    echo "=== All checks passed ==="
else
    echo "=== Some checks FAILED ==="
    exit 1
fi

# Cleanup
echo ""
echo "=== Cleanup ==="
docker rm -f abot-test-run 2>/dev/null || true
docker rmi -f abot-test-onboarded 2>/dev/null || true
docker rmi -f "$IMAGE_NAME" 2>/dev/null || true
echo "Done."

