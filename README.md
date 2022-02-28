# March-Madness

# Components 

# Software Architecture

# Progress Reports
Progress Report (Week of 01/16/22)

Rylee Benes

I collaborated with my teammates to successfully organize a completed Final Project Proposal by filling in a few areas of the document related to success criteria and formatting the document to make it readable. I created the OSS diagram used in our Final Project Proposal. I made sure to stay updated with my teammates to confirm that our Proposal was the best it could be and that it would be turned in on time.

Luca Rivera

I successfully identified SMART Goals for the new proposal with my team. We expanded the original proposal in order for it to fit the new updated requirements. This past week was mostly meeting up with the group and researching more about our project in order to have a clearer idea on how to better our proposal. I also researched different technologies that we can possibly implement/use in our project.

Tycho Halpern 

I created the github repository and added Rylee and Luca as contributors. I then met with both of them and we came up with a guideline for the OSS diagram which Rylee converted from pen and paper to a digital image. We then added success criteria to our final proposal, using the SMART metrics. Finally, I researched data sources that we can use for our project.

Progress Report (Week of 01/23/22)

Rylee Benes

I worked with my team on Tuesday to complete the deliverable talking about repository architecture and our code review policy. I was able to find some code on GitHub that uses a Python GUI to make a nice-looking bracket visualization. Both Tuesday and Thursday, I was able to manipulate the code to produce a bracket we liked and create a mapping dictionary to keep track of all the x-y coordinates of each bracket box, so we can add team names later. I was able to create our first feature branch in our repository and push the code there.

Tycho Halpern

I started the function for parsing the data, the next step is to add all of the teams in the tournament from a given year to a set, and the data will be organized nicely for each year. I also worked on the deliverables with Rylee and Luca this week during lab. We completed them during 
lab so we did not need to do any more work on them individually.

Luca Rivera

Worked with my team in the Word doc for Code review and how we were going to build our repository. I was not able to do hands on work this week because I was sick and could not attend a group meeting. I am now up to date with the progress of the team and will be contributing more with the programming aspects.

Progress Report (Week of 01/30/22)

Rylee Benes

On Tuesday, I separated my bracket file so that the bracket mapping happens first by itself, then the bracket is created later instead of all at the same time. This allows us to add the team names to the mapping before the bracket is created. On Thursday, I created our CI using GitHub Actions through python-app.yml. This allows us after every commit to set up an environment, set up our dependencies, and run any testing that we later create to squash bugs. We can track if everything works properly through the Actions tab on our repository. I also created the deliverable that summarizes our build-system and CI thoroughly.

Luca Rivera-

This week I met up with the team on Tuesday and Thursday. We were working on data processing for our project. This week I mainly worked on researching how github actions worked and discussing on the best data structures to use to store all of the CSV files. We also discussed future steps of our project.

Tycho Halpern

I finished the parsing function, and changed the data structure for storing the team by team data. The parsing function now does not need a list of the teams who participated in the tournament as an input, and can separate teams on its own. I also set up the build environment and compared the outputs of the build using diffoscope.


Progress Report (Week of 2/7/2022)

Tycho Halpern

I wrote the unit test to test the parsing function, and our team worked on the coverage report during lab. I also rewrote the structure of our main file to increase coverage. Our tests did not cover all of our code, so changing the structure of the code increased coverage. I learned how the actions tab works on github and figured out how to monitor issues that are raised with the repository. I then wrote the skeleton for how an individual game would be simulated and talked with my group about more specifica plans for the simulation portion of our bracket generator.

Luca Rivera-

This week our team worked on making our first unit test and adding a code coverage feature for the code. I helped my teammate Rylee to both research and implement an automated way to get code coverage. For now we have it on every commit to the repository. I also proposed new ideas as to how we should approach the main part of the program the actual 'simulation'. It feels like we are on milestones and work done.

Rylee Benes

On Tuesday, I created the GitHub Action for code coverage that prints out a comprehensive table after every commit to our repository. I also edited the testing section of our CI so we could run a unit test. On Thursday, I documented our deliverable for the week and submitted it. Then, I brainstormed with the group what to do with our AI weighting and simulator. On Friday, I assisted Tycho in creating and organizing new functions and files for our weighting and simulator. I also helping in finding more data for stats we were missing.

Progress Report (Week of 02/13/22)

Rylee Benes

On Tuesday, we found new, better data on a new website, so I created an Excel sheet so that we could transfer the stats we wanted into a useable .csv file. I then completed filling out the seven remaining Excel sheets over Tuesday, Wednesday, and Thursday. On Thursday, I also helped the group in getting the data into our program and working on our game simulator.

Tycho Halpern

During lab this week we decided to create our own data set in order to include every statistic that we want to use in the same format. We then talked about how we want our final simulation algorithm to work and I implemented the skeleton for the simulation. We then ran a test case on the simulation and found that the structure will work well. 


Progress Report (Week of 02/20/22)

Rylee Benes

On Tuesday, I helped in creating the data flow diagram and writing the security design deliverable. I edited the bracket to save as a .jpg file. I fixed the bracket to include the final two game. Later, I helped Tycho in connecting the game simulator to the bracket maker, so that we can feed in 68 teams, the teams play games and are arranged into the bracket, then saved. I started working on the midterm PowerPoint and fixed up the rest of our input files, so that all of our data can be simulated into a bracket. 

# References
