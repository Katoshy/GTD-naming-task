## Latest Updates

### Refined Claude AI Prompt

### Implemented Checked Property Tracking in Notion

- **Objective:** Prevent redundant AI checks and optimize API usage by tracking processed projects.
- **Changes Made:**
  - **Added "Checked" Property:**
    - Introduced a new checkbox property named "Checked" in the Notion projects database.
    - This property indicates whether a project has already been validated.
  - **Updated `check_projects` Function:**
    - Modified the function to query only those projects where "Checked" is `False` or not set (`None`), ensuring that already processed projects are skipped.
    - After validating a project (whether valid or invalid), the script marks it as "Checked" to avoid future reprocessing.

## **How to Update Your Setup**

If you've already cloned the repository and set up your environment, ensure that your Notion projects database includes the new "Checked" property:

1. **Add "Checked" Property in Notion:**
   - Open your projects database in Notion.
   - Click on **Add a property**.
   - Name the property `Checked` and select the **Checkbox** type.

2. **Update the `WORKSPACES` Configuration:**
   - Ensure your `WORKSPACES` list in the script includes the correct `name`, `token`, and `projects_page_id` for your Notion workspace.

3. **Set Environment Variables:**
   - Make sure the `ANTHROPIC_API_KEY` environment variable is set with your Anthropic API key.

4. **Run the Script:**
   - Execute the script manually or deploy it as a Google Cloud Function as per your setup.

---

## **Testing the Updates**

Use the following test cases to verify the updated script's functionality:

| Original Project Name           | Expected Outcome                          |
|---------------------------------|-------------------------------------------|
| Write first chapter of book     | Invalid<br>Suggested name: First chapter of book is written |
| Buy tickets                     | Invalid<br>Suggested name: Buy tickets is  |
| First milestone                 | Invalid<br>Suggested name: First milestone is |
| Upgrade Website                 | Invalid<br>Suggested name: Upgrade Website is |
| Medicine drawer is stocked      | Valid                                     |
| Medicine drawer has been stocked| Valid                                     |
| Supplies are organized          | Valid                                     |
| Supplies have been organized    | Valid                                     |
