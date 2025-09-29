
# ⚾ MLB Data Analytics AI Challenge

## 🎯Goal


Use local ahent with a Supabase MCP client to solve 4 progressive data visualization challenges. 

## Repository Structure

```
workshop-04/
├── exercise_0/          # Introductory exercise
├── exercise_1/          # Era Batting Average Trends (Line Plot)
├── exercise_2/          # Top Home Run Hitters Heatmap  
├── exercise_3/          # Home Run Distribution Box Plot
├── exercise_4/          # Team Performance Correlation Matrix
├── src/mlb/             # Database utilities & connection tools
├── outputs/             # Save your visualizations here
└── pyproject.toml       # Python dependencies (uv managed)
```

## Setup

1. **Environment Setup**: Ensure you have `uv` package manager installed.

```
pip install uv
```

2. **Database Connection**: Configure your Supabase connection via MCP. For that, add the MCP definition in `.cusros/mcp.json`. The access token will be provided in the meeting chat.

3. **Rules definition**: Complete the plotting guidelines rool in `.cursor/rules/plotting-guidelined.mdc`. Create any extra rool you consider necessary.

4. **Commands definition**: Complete the database MCP command in `.cursor/commands/database.md`. Create any extra command you consider necessary.

## 📚 Essential Documentation

| Resource | Purpose | Link |
|----------|---------|------|
| **Supabase MCP** | Database connection & queries | [Setup Guide](https://supabase.com/docs/guides/getting-started/mcp) |
| **Cursor Commands** | AI assistant capabilities | [Command Reference](https://cursor.com/docs/agent/chat/commands) |

## 💡 Pro Tips

- **Start simple**: Create a simple version of the rules and commands. Try working on exercise 1 and iterate as you identify problems with your rules.
- **Use meta promting**: Use AI to generate the rules, commands and prompts, but only once you know that do you want to include on each one.
- **Breakdown problems**: Separate each exercise into smaller pieces that you can iterate. Don't try to one-shot every problem. Use change of thought (CoT) in your promting.

