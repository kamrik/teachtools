## GitHub Classroom

[GH Classroom](https://classroom.github.com/)
automates a lot of work associated with assignments submitted via GitHub.

It's good for:
- Automated grading (CI/CD style scripts). You will be able to download the grades for the entire class as a CSV file.
- Manual grading when you prefer (and can afford) to use code review styled comments on the student's repo

### Setting up a Course Offering
- Create an organization on GitHub
  - It's free, but you can get some extras if you register for [GitHub education](https://github.com/education).
  - It is recommended to create one org per __course offering__, new semester - new org.
- On GH Classroom create a class with the org
- Add student list
  - In most cases student list is the list of student college emails, one per line. But those can be any unique identifiers.

### Creating an assignment
- Create a template repository with starter code in the course org
  - You can mark a repo as "template" in the repo settings after you created it
  - Keep the template minimal, it's almost impossible to change after the first student accepted the assignment.
- On GHClassroom create a new assignment. The wizard will walk you through a bunch of questions
  - Select the template repository. It will be cloned once the assignment created, and then cloned again for each student that accepts the assignment.
  

