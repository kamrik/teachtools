## GitHub CLI

GitHub has a CLI client that is convenient for some automations with GH Classroom.

- [cli.github.com](https://cli.github.com/)
- Run `gh auth login` to connect the CLI to your account
- To install the GitHub Classroom extension, run  
  `gh extension install github/gh-classroom`
- [Using GitHub Classroom with GitHub CLI](https://docs.github.com/en/education/manage-coursework-with-github-classroom/teach-with-github-classroom/using-github-classroom-with-github-cli)


## Getting grades as CSV

```bash
# List all your classes
gh classroom list

# Save the integer class id of the class you need
CLASS_ID=1234567

# List all assignments in the class
gh classroom assignments -c $CLASS_ID
ASGN_ID=777777

# Show general assignment info (mildly useful)
gh classroom assignment -a $ASGN_ID

# Download all grades as a CSV file
gh classroom assignment-grades -a $ASGN_ID 
# default filename is grades.csv, but you can override it
gh classroom assignment-grades -a $ASGN_ID -f grades_lab2.csv
```





