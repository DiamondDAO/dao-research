# How to contribute to the DiamondDAO Labs

Hello fellow research oriented person, this document will try and summarize the key steps needed to contribute to the Labs!

## Process
- First, make sure that your research is of interest to the DAO, by communicating with other DAO members in the #labs channel and joining a Labs call. 
- Second, gather the data and analyze it.
- Third, check back up in the #labs for internal discussion
- Fourth, write either a Twitter Thread or a Mirror post presenting your question and result

## The three types of labs project
For now, the labs consists of mostly two type of project: 
- Data gathering: You will build a scrapper, or some form of automated pipeline to gather new data to be used both in research and in Chainverse
- Data analysis: You will utilize Diamond DAO data, or other sources to run an analysis of questions of interests. 
- Qualitative research: You will generate new insights in the DAO space through rigorous qualitative methods.

### Data gathering
For data gathering, head over to the main [DataCollection](https://github.com/DiamondDAO/DataCollection) repo. To gather data, you are free to chose the programing language of your choice as long as your project meets the following criteria on top of the DiamondDAO [Code guidelines]():
- The code is parameterized from the command line. You can set parameters like the URL, the start time, or other parameters directly from the command line.
- The code is resilient. You have tried to foresee errors, wrote error catching mechanisms, and have some sort of logging system that can be used to reflect on issues that arose. 
- The code is dockerize. Your code has a Dockerfile and a docker-compose accompanying file. All parameters can be set through ENV variables.

For an example, you can use [this project](https://github.com/DiamondDAO/DataCollection/tree/main/ExampleScraper) written in python.

### Data analysis
To analyse data, we highly encourage you do so using standard tools such as Python or R. Your analysis must meet the following criteria:
- Your code is well annotated and the though process is clear to follow. 
- Your code is available on GitHub/GitLab as a notebook file (jupyter or R markdown).
- Your data sources are available with the code. 

For an example, you can look at [those projects](https://github.com/DiamondDAO/dao-research) written in python.

### Qualitative research
Qualitative research must be highly rigorous to allow for insights to emerge. Therefore, your analysis must follow the following criteria:
- Define the bounds of research and hypothesis that are tested
- Justify the choice of methodology by citing accepted qualitative standard in the literature
- Document the process and choice of number of interviews, or samples

We don't yet have an example to add here, be the first to do so!

## Publishing
Once the research is done and validated with the members of DiamondDAO, you need to write about it. Indeed communicating results is key to the advancement of research! For this there are two options, either this work is substantial enough for a Mirror article, or the analysis is small enough to be a Twitter thread only. It is ok to hold on to some results for some time to make a longer form mirror article afterwards, but the goal must be clear that this must be published at someor  point.

For an example of twitter threads you can look [here](https://twitter.com/XquaInTheMoon/status/1482838043123806209), [here](https://twitter.com/XquaInTheMoon/status/1468926316023975940), or [here](https://twitter.com/XquaInTheMoon/status/1466785812352225282).

For an example of a mirror post you can look [here](https://diamond.mirror.xyz/9mhfHWIFofZ0ZwWyKZJySC4b5sqKekT6hIpQ5lTh-vs)

## Repositories
### Research
If you are creating a new quantitative or qualitative research project, you will need to merge it back unto the main [dao-research repository](https://github.com/DiamondDAO/dao-research). Clone the repo, create a new folder for your analysis, and when you are ready push a merge request.

### Data
If you are creating a new scraper to collect data, follow the example and guidelines from the [ExampleScrapper](https://github.com/DiamondDAO/DataCollection/tree/main/ExampleScraper) and the [DataCollection](https://github.com/DiamondDAO/DataCollection) repository. 
