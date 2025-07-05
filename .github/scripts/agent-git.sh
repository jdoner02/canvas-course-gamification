#!/bin/bash

# AI Agent Autonomous Git Workflow
# This script enables AI agents to commit frequently without user interaction

set -e  # Exit on any error

# Configuration
MAX_COMMIT_SIZE=50  # Maximum files per commit
COMMIT_PREFIX="[AGENT-AUTO]"
BRANCH=$(git branch --show-current)

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "Error: Not in a git repository"
        exit 1
    fi
}

# Function to check for changes
has_changes() {
    ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]
}

# Function to stage files intelligently
stage_files() {
    # Stage modified and new files, but limit the number
    git add -A
    
    # Check if staging area is too large
    staged_files=$(git diff --cached --name-only | wc -l)
    if [ "$staged_files" -gt "$MAX_COMMIT_SIZE" ]; then
        echo "Warning: Large number of files staged ($staged_files). Consider smaller commits."
    fi
}

# Function to generate commit message based on changes
generate_commit_message() {
    local persona="$1"
    local custom_message="$2"
    
    if [ -n "$custom_message" ]; then
        echo "[AGENT-${persona}] $custom_message"
        return
    fi
    
    # Analyze changes to generate appropriate message
    local added_files=$(git diff --cached --name-only --diff-filter=A | wc -l)
    local modified_files=$(git diff --cached --name-only --diff-filter=M | wc -l)
    local deleted_files=$(git diff --cached --name-only --diff-filter=D | wc -l)
    
    local message=""
    
    if [ "$added_files" -gt 0 ]; then
        message="${message}Add $added_files files"
    fi
    
    if [ "$modified_files" -gt 0 ]; then
        if [ -n "$message" ]; then
            message="${message}, modify $modified_files files"
        else
            message="Modify $modified_files files"
        fi
    fi
    
    if [ "$deleted_files" -gt 0 ]; then
        if [ -n "$message" ]; then
            message="${message}, delete $deleted_files files"
        else
            message="Delete $deleted_files files"
        fi
    fi
    
    if [ -z "$message" ]; then
        message="Update project files"
    fi
    
    echo "[AGENT-${persona}] $message"
}

# Function to run pre-commit checks
run_pre_commit_checks() {
    local persona="$1"
    
    echo "Running pre-commit checks for $persona agent..."
    
    # Check for syntax errors in common file types
    for file in $(git diff --cached --name-only); do
        case "$file" in
            *.py)
                if command -v python3 >/dev/null 2>&1; then
                    python3 -m py_compile "$file" || {
                        echo "Python syntax error in $file"
                        return 1
                    }
                fi
                ;;
            *.js|*.ts)
                if command -v node >/dev/null 2>&1; then
                    node -c "$file" || {
                        echo "JavaScript/TypeScript syntax error in $file"
                        return 1
                    }
                fi
                ;;
            *.json)
                if command -v jq >/dev/null 2>&1; then
                    jq empty "$file" >/dev/null || {
                        echo "JSON syntax error in $file"
                        return 1
                    }
                fi
                ;;
        esac
    done
    
    # Check for large files
    for file in $(git diff --cached --name-only); do
        if [ -f "$file" ] && [ $(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0) -gt 10485760 ]; then
            echo "Warning: Large file detected: $file (>10MB)"
        fi
    done
    
    echo "Pre-commit checks passed for $persona agent"
    return 0
}

# Function to commit with agent context
agent_commit() {
    local persona="${1:-GENERAL}"
    local message="$2"
    
    check_git_repo
    
    if ! has_changes; then
        echo "No changes to commit"
        return 0
    fi
    
    echo "AI Agent ($persona) preparing commit..."
    
    # Stage files
    stage_files
    
    # Run pre-commit checks
    if ! run_pre_commit_checks "$persona"; then
        echo "Pre-commit checks failed. Aborting commit."
        return 1
    fi
    
    # Generate commit message
    local commit_msg=$(generate_commit_message "$persona" "$message")
    
    # Commit with detailed information
    git commit -m "$commit_msg" \
               -m "Agent: $persona" \
               -m "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")" \
               -m "Branch: $BRANCH" \
               -m "Automated commit by AI agent system"
    
    echo "Committed: $commit_msg"
    
    # Log the commit for tracking
    echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - [$persona] $commit_msg" >> .github/logs/agent-commits.log
}

# Function to create a checkpoint before major operations
create_checkpoint() {
    local persona="$1"
    local description="$2"
    
    agent_commit "$persona" "CHECKPOINT: $description"
    
    # Tag the checkpoint for easy reference
    local tag_name="agent-checkpoint-$(date +%Y%m%d-%H%M%S)"
    git tag -a "$tag_name" -m "AI Agent Checkpoint: $description"
    
    echo "Checkpoint created: $tag_name"
}

# Function to auto-push if configured
auto_push() {
    if [ "$AUTO_PUSH" = "true" ]; then
        echo "Auto-pushing to remote..."
        git push origin "$BRANCH" --tags || {
            echo "Failed to push. Continuing without remote sync."
        }
    fi
}

# Main execution based on command line arguments
case "${1:-commit}" in
    "commit")
        agent_commit "${2:-GENERAL}" "$3"
        auto_push
        ;;
    "checkpoint")
        create_checkpoint "${2:-GENERAL}" "$3"
        auto_push
        ;;
    "status")
        check_git_repo
        echo "Git status for AI agents:"
        git status --porcelain
        ;;
    "log")
        if [ -f ".github/logs/agent-commits.log" ]; then
            echo "Recent AI agent commits:"
            tail -20 .github/logs/agent-commits.log
        else
            echo "No agent commit log found"
        fi
        ;;
    *)
        echo "Usage: $0 {commit|checkpoint|status|log} [persona] [message]"
        echo "  commit     - Commit current changes with agent metadata"
        echo "  checkpoint - Create a checkpoint commit and tag"
        echo "  status     - Show current git status"
        echo "  log        - Show recent agent commits"
        exit 1
        ;;
esac
