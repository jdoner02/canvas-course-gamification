#!/bin/bash

# AI Agent Activation Script
# Main entry point for activating AI agent personas with full context

set -e

# Configuration
GITHUB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PERSONAS_DIR="$GITHUB_DIR/ai-personas"
SCRIPTS_DIR="$GITHUB_DIR/scripts"
LOGS_DIR="$GITHUB_DIR/logs"

# Ensure required directories exist
mkdir -p "$LOGS_DIR"

# Function to display the main initialization
show_initialization() {
    echo "🤖 AI AGENT INITIALIZATION SYSTEM"
    echo "=================================="
    echo "📍 Project: Canvas Course Gamification Platform"
    echo "🎯 Status: Production Ready - Canvas Integration Complete"
    echo "🚀 Mission: Dr. Lynch MATH 231 Pilot Deployment"
    echo ""
}

# Function to detect persona based on task description
detect_persona() {
    local task_description="$1"
    local task_lower=$(echo "$task_description" | tr '[:upper:]' '[:lower:]')
    
    # Define persona keywords
    declare -A persona_keywords=(
        ["ux-designer"]="ui ux design accessibility responsive frontend user interface experience"
        ["security-specialist"]="security privacy ferpa auth authentication encryption compliance vulnerability"
        ["data-scientist"]="analytics data research statistics ml insights metrics analysis report"
        ["devops-engineer"]="devops infrastructure deployment scaling docker kubernetes monitoring cicd"
        ["educational-specialist"]="pedagogy learning assessment course student faculty education teaching"
        ["ai-ml-specialist"]="ai ml nlp recommendation prediction automation intelligent machine learning"
        ["qa-engineer"]="testing qa validation performance bug quality automation test"
        ["mobile-developer"]="mobile ios android app offline responsive cross-platform"
        ["fullstack-developer"]="fullstack api integration architecture platform database backend"
    )
    
    declare -A persona_scores
    
    # Score each persona based on keyword matches
    for persona in "${!persona_keywords[@]}"; do
        persona_scores[$persona]=0
        for keyword in ${persona_keywords[$persona]}; do
            if echo "$task_lower" | grep -q "$keyword"; then
                ((persona_scores[$persona]++))
            fi
        done
    done
    
    # Find persona with highest score
    local best_persona="fullstack-developer"  # Default
    local best_score=0
    
    for persona in "${!persona_scores[@]}"; do
        if [ "${persona_scores[$persona]}" -gt "$best_score" ]; then
            best_score="${persona_scores[$persona]}"
            best_persona="$persona"
        fi
    done
    
    echo "$best_persona"
}

# Function to load persona context
load_persona() {
    local persona="$1"
    local persona_file="$PERSONAS_DIR/$persona.md"
    
    if [ ! -f "$persona_file" ]; then
        echo "❌ Error: Persona file not found: $persona_file"
        return 1
    fi
    
    echo "🎯 Loading AI Agent Persona: $(echo $persona | tr '-' ' ' | sed 's/\b\w/\U&/g')"
    
    # Extract key information from persona file
    local emoji=$(grep -o "^# [^[:space:]]*" "$persona_file" | head -1 | cut -c3-)
    local title=$(grep "^# " "$persona_file" | head -1 | cut -c4-)
    
    echo "$emoji $title"
    echo ""
    
    # Show core expertise
    echo "🔧 Core Expertise:"
    sed -n '/## \*\*🎯 Primary Expertise Areas\*\*/,/## /p' "$persona_file" | \
        grep -E "^- \*\*|^  - " | head -5 | sed 's/^/  /'
    echo ""
    
    # Show key tools
    echo "🛠️ Primary Tools:"
    sed -n '/### \*\*Core.*Technologies\*\*/,/### /p' "$persona_file" | \
        grep -E "^  - " | head -5 | sed 's/^/  /'
    echo ""
}

# Function to show collaboration options
show_collaboration() {
    echo "🤝 Collaboration Options:"
    echo "  - For complex tasks requiring multiple expertises"
    echo "  - Automatic handoffs between specialized agents"
    echo "  - Use 'multi-agent' as persona for collaborative tasks"
    echo ""
}

# Function to set up git workflow
setup_git_workflow() {
    local persona="$1"
    
    echo "🔄 Setting up autonomous git workflow..."
    
    # Make sure git scripts are executable
    chmod +x "$SCRIPTS_DIR/agent-git.sh" 2>/dev/null || true
    
    # Create alias for easy access
    alias agent-commit="$SCRIPTS_DIR/agent-git.sh commit $persona"
    alias agent-checkpoint="$SCRIPTS_DIR/agent-git.sh checkpoint $persona"
    alias agent-status="$SCRIPTS_DIR/agent-git.sh status"
    
    echo "  ✅ Autonomous commits enabled"
    echo "  ✅ Quality gates activated"
    echo "  ✅ Persona-specific tracking ready"
    echo ""
}

# Function to display next steps
show_next_steps() {
    local persona="$1"
    
    echo "🚀 Ready for Mission Execution!"
    echo "Next Steps:"
    echo "  1. 📖 Review your persona knowledge: .github/ai-personas/$persona.md"
    echo "  2. 🔍 Analyze the current task requirements"
    echo "  3. 💻 Begin implementation with your specialized expertise"
    echo "  4. 📝 Commit frequently using: agent-commit \"description\""
    echo "  5. 🤝 Collaborate with other personas as needed"
    echo ""
    echo "🎯 Success Metrics:"
    echo "  - Autonomous operation with minimal human intervention"
    echo "  - High-quality code with automated validation"
    echo "  - Seamless collaboration between agent personas"
    echo "  - Educational impact and student experience enhancement"
    echo ""
}

# Function to log activation
log_activation() {
    local persona="$1"
    local task="$2"
    local timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    
    echo "$timestamp - [ACTIVATION] Agent persona '$persona' activated for task: $task" >> "$LOGS_DIR/agent-activations.log"
}

# Main activation function
activate_agent() {
    local persona="$1"
    local task_description="$2"
    
    # If no persona specified, detect it
    if [ -z "$persona" ] || [ "$persona" = "auto" ]; then
        persona=$(detect_persona "$task_description")
        echo "🔍 Auto-detected persona: $persona"
        echo ""
    fi
    
    # Show initialization banner
    show_initialization
    
    # Load the persona
    load_persona "$persona"
    
    # Show collaboration options
    show_collaboration
    
    # Set up git workflow
    setup_git_workflow "$persona"
    
    # Show next steps
    show_next_steps "$persona"
    
    # Log the activation
    log_activation "$persona" "$task_description"
    
    # Export environment variables for the session
    export AI_AGENT_PERSONA="$persona"
    export AI_AGENT_TASK="$task_description"
    export AI_AGENT_PROJECT="Canvas Course Gamification"
    export AI_AGENT_STATUS="Production Ready - Canvas Integration Complete"
    
    echo "🎉 AI Agent '$persona' is now active and ready!"
    echo "💡 Tip: Use the command center at .github/AI_AGENT_INIT.md for full context"
}

# Command line interface
case "${1:-help}" in
    "activate")
        activate_agent "$2" "$3"
        ;;
    "list")
        echo "Available AI Agent Personas:"
        for persona_file in "$PERSONAS_DIR"/*.md; do
            if [ -f "$persona_file" ]; then
                persona=$(basename "$persona_file" .md)
                emoji=$(grep -o "^# [^[:space:]]*" "$persona_file" | head -1 | cut -c3-)
                title=$(grep "^# " "$persona_file" | head -1 | cut -c4- | sed 's/[^a-zA-Z ].*//')
                echo "  $emoji $persona - $title"
            fi
        done
        ;;
    "status")
        if [ -n "$AI_AGENT_PERSONA" ]; then
            echo "🤖 Active Agent: $AI_AGENT_PERSONA"
            echo "📋 Current Task: $AI_AGENT_TASK"
            echo "📍 Project: $AI_AGENT_PROJECT"
            echo "📊 Status: $AI_AGENT_STATUS"
        else
            echo "No active AI agent session"
        fi
        ;;
    "log")
        if [ -f "$LOGS_DIR/agent-activations.log" ]; then
            echo "Recent AI Agent Activations:"
            tail -10 "$LOGS_DIR/agent-activations.log"
        else
            echo "No activation log found"
        fi
        ;;
    "help"|*)
        echo "🤖 AI Agent Activation System"
        echo ""
        echo "Usage: $0 {activate|list|status|log}"
        echo ""
        echo "Commands:"
        echo "  activate [persona] [task_description] - Activate an AI agent persona"
        echo "                                        - Use 'auto' to auto-detect persona"
        echo "  list                                  - List all available personas"
        echo "  status                               - Show current agent status"
        echo "  log                                  - Show recent activations"
        echo ""
        echo "Examples:"
        echo "  $0 activate auto \"Improve accessibility in student dashboard\""
        echo "  $0 activate ux-designer \"Redesign mobile interface\""
        echo "  $0 activate multi-agent \"Full-stack feature development\""
        ;;
esac
