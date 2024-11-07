from notion_client import Client
import os
import re
from typing import List, Dict, Tuple


# List of Notion workspaces with their tokens and root page IDs
WORKSPACES = [
    {
        "name": "Name here",
        "token": "token here",  # Replace with actual token
        "projects_page_id": "12439e8a-6df1-4d48-826d-c89b99707206"  # Replace with actual projects page ID
    }
]

# --- Improvement: Rewrote the prompt for Claude a bit. ---

def check_with_claude(name: str) -> Tuple[bool, str]:
    """Use Claude to check project name validity and get suggestions"""
    try:
        from anthropic import Anthropic

        anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        prompt = f"""
You are to analyze the following project name: "{name}"
The project name should:
- Be a description of a desired outcome.
- Be phrased in the present perfect tense ("has been") or present tense ("is"/"are").
- Describe a completed state.
- Be clear and specific.

If the project name follows these rules, respond with:
"Valid"
"Suggested name: [Original Project name]"

If it does not, respond with:
"Invalid"
"Suggested name: [Your suggested project name]"

Do not include any additional text.
"""
        message = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        response = message.content.split('\n')
        is_valid = response[0].strip().lower() == "valid"
        suggestion = response[1].strip()

        return is_valid, suggestion

    except Exception as e:
        print(f"Error using Claude API: {str(e)}")
        # Fall back to basic validation if Claude fails
        return is_valid_project_name(name), suggest_project_name(name)


def is_valid_project_name(name: str) -> bool:
    """Check if project name follows GTD outcome-focused naming convention"""
    # Look for present perfect ("has been") or present tense ("is") constructions
    patterns = [
        r'.+\s+is\s+.+',  # "drawer is stocked"
        r'.+\s+has\s+been\s+.+',  # "drawer has been stocked"
        r'.+\s+are\s+.+',  # "supplies are organized"
        r'.+\s+have\s+been\s+.+'  # "supplies have been organized"
    ]

    return any(re.match(pattern, name.lower()) for pattern in patterns)


def suggest_project_name(name: str) -> str:
    """Generate a suggestion for better project name"""
    # Simple transformation to add "is" if not present
    if not is_valid_project_name(name):
        words = name.split()
        # Basic suggestion by adding "is" after first word
        return f"{words[0]} is {' '.join(words[1:])}"
    return name


"""
Improvements:
    Using Notion Properties
    1) Added a new checkbox property to projects database called "Checked".
    2) Updated script to set this property to True after checking a project.
    3) Modified script to skip any projects where this property is True.
"""
def check_projects(workspace: Dict):
    """Check projects in a workspace for proper naming"""
    notion = Client(auth=workspace["token"])

    try:
        response = notion.databases.query(
            database_id=workspace["projects_page_id"],
            filter={
                "or": [
                    {
                        "property": "Checked",
                        "checkbox": {
                            "equals": False
                        }
                    },
                    {
                        "property": "Checked",
                        "checkbox": {
                            "equals": None
                        }
                    }
                ]
            }
        )

        for page in response["results"]:
            if "properties" in page and "Project name" in page["properties"]:
                project_name = page["properties"]["Project name"]["title"][0]["text"]["content"]
                is_valid, suggestion = check_with_claude(project_name)

                if not is_valid:
                    print(f"""
                        Workspace: {workspace['name']}
                        Invalid project name: {project_name}
                        Suggested name: {suggestion}
                        """)

            notion.pages.update(
                page_id=page["id"],
                properties={
                    "Checked": {
                        "checkbox": True
                    }
                }
            )
    except Exception as e:
        print(f"Error processing workspace {workspace['name']}: {str(e)}")


def main(request):
    """Entry point for Google Cloud Function"""
    for workspace in WORKSPACES:
        check_projects(workspace)

    return 'Project names checked successfully'


if __name__ == "__main__":
    main(None)

