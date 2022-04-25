# March-Madness

This project was created as a senior design project at Purdue University. It utilizes linear regression and game simulation to generate March Madness brackets that are aimed to do better than competing bracket A.I. Programs.

To install the package, use the terminal command: ***pip install MarchMadness***  (currently version 1.6.0) 

Then, create and edit a python file (.py) like the one below:
```python
from MarchMadness import MarchMadnessRun

MarchMadnessRun.parseData() # creates dataset
output = [0]*127 # used to store team names for printing final bracket

regressions = MarchMadnessRun.setRegressions() # calculate regregression models using data from previous tournaments

'''
Values for gameTest represent the number of possessions to run for each matchup. 
For example, using 1 will run 1 game worth of possessions for each team (40 minutes),
5 will run 5 games of possessions (200 minutes), and 0.2 will run 0.2 games of possessions (8 minutes).

Using shorter games results in more "upsets" and using too short of games will result in 
games being essentially coin flips and will result in a poor guess for the final score of the game. 

If you decide to create more than 10 brackets at a time, the value(s) of gameTest will be used as an average.
Following a bell curve, 16 percent of brackets will be decided by coin flips, and 16 percent of brackets will 
be decided using at least double length games of your input, the rest will be somewhere in between.
If you want your gameTest input to be used directly, create brackets in batches of 9 or fewer.
'''
# change these values to generate real brackets

gameTest = [2] # number of games to simulate per matchup, see block comment above
yearTest = [2022] # what year(s) do you want to generate brackets for?
numBrackets = 10 # how many unique brackets do you want to generate?
# if you leave the champion field empty (or input a string that does not match a team name) it will be ignored and brackets will be filled out with no bias.
champion = "" # If this doesn't work, match the input to what your team is named on the output file
for year in yearTest:
    for numGames in gameTest:
        MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets, champion)



'''If you only want to simulate a single bracket for a single year,
calling this function with the desired inputs instead of using lines 23-28
will generate a single bracket. You could also just enter a single year
in the yearTest list and set numBrackets to 1.'''
#  MarchMadnessRun.tournament(year, regressions, output, numGames, numBrackets)
```

Finally, to generate your brackets run the command: ***python3 <yourFile.py>*** in the terminal. Your brackets will be stored in a newly created /brackets/ directory. View them by navigating to this directory in your file system. 


# Components 
*These are the components of our project with a brief description of what they do all available in the MarchMadness folder on GitHub or in the installed package:*  

**MarchMadnessRun.py**: the driver file that helps with parsing data and tournament creation.  
**Simulate.py**: the file used to simulate matchups between teams using stats to run every game possession.  
**AIWeighting.py**: the file used to create weights for each stat based on team season stats versus individual March Madness game team stats using linear regression.  
**bracket.py**: the file used to create readable and organized brackets of each tournament saved locally as a .jpg file.  
**Previous/**: contains all of the data used for team stats and bracket creation.  
**Simulations/**: contains files used for final game bracket scores and accuracy measurements.  
**Brackets/**: contains outputted final brackets.  

*Here is our component diagram below, summarizing our project:*  
![image](https://user-images.githubusercontent.com/54416591/163599314-fbfa7155-4177-4812-828b-f4c83886ceca.png)

# Software Architecture
Our software architecture includes saving everything here on GitHub. All of the notable components saved are mentioned in the section above. We utilized a branching model when creating this project, starting with a main branch and creating a new branch for every new feature, later merging it back to main.

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

Tycho Halpern

This week I spent the majority of the time working on simulating the tournament for a given year. I created an array structure to store all of the teams so that the winners of the correct 2 games would play each other in the next round. I added an output list to store the winners of each game, and the a transformation array to reorganise the team names so they could be interpreted correctly by the bracket making program. At the end of the week we were able to output a simulated tournament to a .jpg file that was easy to read for the first time. 

Progress Report (Week of 02/27/22)

Rylee Benes

This week, we prepared our code for our midterm presentation, getting our brackets to utilize the game simulator for two and three point attempts. We met to finish up the PowerPoint and run through it. We then began to talk over how we were going to implement our AI algorithm. We ended up changing our model from Naive Bayes to linear regression, and started to work on it.

Progress Report (Week of 03/06/22)

Rylee Benes

We worked pretty much every day this week, so that our code was ready for March Madness, which starts next week. I created our regression model as Tycho finished parsing all new data. We then finished implementing all of the stats needed for the game simulator. I then did some research for a stat that may help in weighting teams from different conferences, and we deciding on implementing the Strength of Schedule stat. I then created the final bracket .txt files for 2021, 2013, and 2014, so that we could test accuracy between our create brackets and the real, final brackets. We then compared the number of games each match-up should have for low standard deviation and high accuracy.

Tycho Halpern

I finished parsing all of the data, then worked on the simulator. I added all of the new inputs that we used for the final bracket to the simulator. Then Rylee wrote a method for testing the accuracy between a generated bracket and the correct bracket for 2013, 2014, and 2019. I then spend time tweaking a few of the inputs (such as number of simulations to run for each game) in order to determine a final simulator that would produce as high accuracy as possible while still having variability in the bracket outputs. 

Progress Report (Week of 03/13/22)

Tycho Halpern

Rylee added the updated data for 2022 and we ran the final simulations. We then entered 100 brackets into espn.com's tournament challenge so we will be able to view our results easier. We met as a group on Sunday and worked on the packaging deliverable for 3/21.

Rylee Benes

Over spring break, we created the 100 brackets and I filled in 50 of them by hand on the ESPN website. I pulled all of the 2022 data and created the bracket.txt file for 2022 so we could do this. We then watched our project at work as basketball games played this week and we are at 10 games above the 90th percentile as of the end of the round of 32.

Progress Report (Week of 03/20/22)

Tycho Halpern

As a group we met to update the deliverable from last week to fix our distribution. Each time we updated setup.py to change the files included in the build, I downloaded them and ran the setup execution steps mentioned in this weeks deliverable in a secluded environment to make sure an outside user would be able to use our program. 

Rylee Benes

This week, we completed getting a package fully working for our project, and submitting the deliverable. We then created our documentation. I helped in created the user manual that works around the package, and created the deliverable we chose to submit. We have also been keeping a close eye on basketball results and how they impact our brackets. Due to various upsets, we currently have 4 brackets in the 90th percentile, but hope for that to go up.

Progress Report (Week of 03/27/22)

Tycho Halpern

This week I fixed our packaging. We were having issues with importing the data and using it in our functions. I updated our filepaths from strings to use importlib_resources and generate filepaths. Next I wrote a sample script so users would know how to use our package, and Rylee added it to the updated user manual. 
Finally, I created the software bill of materials using cyclonedx. 

Rylee Benes

This week, we fixed our package by getting it runnable with pip after uploading it to PyPi. I updated our README to reflect how to write a file that will in turn run our package properly. We then used CycloneDX to create an SBOM of our package. I also created the MIT license and deliverable summary for the week. I got our code coverage GitHub Action working again, and now Tycho and I are trying to write test cases to improve our code coverage.

Progress Report (Week of 04/03/22)

Rylee Benes

This week, we started to brainstorm how to possibly improve our bracket results as we only ended up with 2 brackets in the 90th percentile. I grabbed the percentile threshold values for 2022 and 2021 from the ESPN website and we created a function to calculate bracket points and compared them to the percentile values to see what percentile they were. We then came up with the idea to randomize the number of games each matchup plays for each bracket using a bell curve. This then accounts for having some brackets with more upsets (coin flip) and some brackets with more high-seeded wins. We plan on creating an option for users to pick their preference. I also created a progress bar for when brackets are being created for greater UI design.

Tycho Halpern

This week, I wrote functions to calculate the "score" of a bracket, using the same logic as ESPN (10 points for correctly picking a first round game, 20 for second, ..., 320 points for correctly picking the champion) and tested our simulator with 2022 data as well as 2021 data. When using the thresholds Rylee looked up from these past 2 years, our brackets perform significantly better for how the 2021 tournament played out when compared to the 2022 tournament. 


Progress Report (Week of 04/10/22)

Tycho Halpern

This week I worked with Rylee to increase our code coverage. After we restructured our code without the unneeded lines, we fixed the output bracked .jpg files to be higher quality and made sure all of the team names fully fit in the bracket boxes. 

Rylee Benes

This week, we fixed the code coverage. I implemented it into our other GitHub Action, and we got our code coverage up to 100%. We then cleaned up the rest of our code and added comments. Tycho and I fixed the font and resolution of the bracket output to make it more readable. We also started analyzing our data and brainstorming how it would be presented in our final presentation. I started cleaning up our repository, so that it looks good for the final.

Progress Report (Week of 04/17/22)

Tycho Halpern

I worked on and prepared for the final presentation. Added ability to select champion, made a final package to use in the presentation, and wrote a few scripts for the demo.

# References

https://github.com/JonathanZwiebel/bracket-generator  
https://www.kaggle.com/c/ncaam-march-mania-2021/data  
https://www.teamrankings.com/ncb/team-stats/  
https://github.com/programmingwithalex/test_repo_pylinter_v2  
https://fantasy.espn.com/tournament-challenge-bracket/2022/en/  
https://dzone.com/articles/executable-package-pip-install  
https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
