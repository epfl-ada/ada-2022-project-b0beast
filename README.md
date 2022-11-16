# What makes a movie successful?
**Examining the relation between characteristics of movies and their box office revenue with an emphasis on important factors like diversity and gender**

## Abstract 
_(A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?)_

Our idea would be to examine which characteristics of movies and their characters are causing high movie box office revenue. Since the movie business is a multi-billion-dollar industry, it would be very beneficial to know what sells and what does not. In order to add to this mainly capitalistic driven topic some more societal relevance, we would during the examination of these characteristics lay an emphasis on factors like ethnical diversity, gender ratio, and the age distribution between men and women in the cast and how it changed over the years. Since movies can be seen as a reflection of their time, the results of this analysis could act as an indicator for changes and advancements in society over time.

## Research Questions
_(A list of research questions you would like to address during the project)_

•	Which characteristics of movies are causing high movie box office revenue?

•	Which characteristics of movies are causing low movie box office revenue?

•	Are their differences in these characteristics between movies from the US and movies from the rest of the world?

•	Did ethnical diversity in successful movies change over time?

•	Did the gender ratio of the cast in successful movies change over time?

•	Did the age distribution of men and women of the cast in successful movies change over time?

•	What could have caused these changes?

•	What can you infer from these changes about society?

## Proposed additional datasets (if any)
_(List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible)_

## Methods

## Proposed timeline

## Organization within the team
_(A list of internal milestones up until project Milestone P3)_

## Questions for TAs (optional)
_(Add here any questions you have for us related to the proposed project)_




# ada-2022-project-b0beast
## Base research "directions" (subject to change)
### 1. The changes of character types in movies over time as an indicator for transformation processes in society.
Movies and their characters as a cultural phenomenon heavily influence our society and vice versa. Therefore, the changes of the traits and actions of the most common character types in movies (Hero, Villain etc.) over time could act as an indicator for general changes in society. Because of this, I want to find out which are the most common character types in the most successful movies for every year. The first step would be to rank all movies after box office revenue for each year, and then identify the most successful ones. Out of these movies, you can then pick out the main characters and analyze their traits and their actions. Both can be analyzed by scanning the plot summaries using Natural Language Processing, while the traits can additionally be analyzed through investigation of the actor metadata (Gender, Age, Height etc.). Afterwards, the found changes of character types in movies over the years can be outlined and be considered as an image of the advancements in society.

**Feedback:** _Overall, the idea is interesting and creative. You have quite a clear idea on how to proceed. The tricky part is the analysis of the plot, extracting traits and actions of characters will not be easy, but Learning Latent Personas of Film Characters paper can help you there maybe. About the use of metadata, I wouldn’t be sure the traits of the actor and the traits of the characters are not necesarrily close, but you can doublecheck manually some cases. Finally, if I try to think abuout the final insights that you can get, I would think a bit more about how the changes in characters can be a proxy for society advancement: if in 2023’s best movies there are more villains than in 2022, what can I actually infer?_
 
### 2.Movie genres of different eras 
The past decade seems to have been bombared by successful superhero movies, but that has not always been the case. It seems as if eras of movie genres come and go, sometimes looking back to a golden age or maybe a more hopeful future. What and when were these eras? Did they really exist, or were they just an unfounded feeling? Were they correlated with outside events, such as economic crises, wars, or times of economic ease? Using the CMU Movie Summary Corpus’ plot summaries, the Stanford CoreNLP analysis, as well as some external data would let us tackle this interesting subject and tell the story of people’s favourite escape from reality: movies.

**Feedback**: _This idea can be interesting. You’re hinting at looking at the most successful genres over time, and their eventual correlation with external events. The former can be done and is interesting, but should be complemented with additional analyses. For the latter, do you plan on using an additional dataset? Or look manually at events of each year? Drawing inference about a possible correlation there can be a bit far-fetched, unless it’s well justified._

### 3.Superwoman or housewife?
Which roles do the women have in the movies? Do they display the main character or are they just the girlfriend or wife of the male protagonist? How are they pictured? Arethere more strong and independent women, that could be used as a role model, portrayed in the movies nowadays than 50 years ago? Toanalyze the question, if the movie industry is contributing to the overcoming of inequalities between genders or rather preventing it, methods described in the paper could be used to analyze the character of the agonists in the movies. Then the characters could be categorized into stereotypical feminine (beautiful, caring, polite), stereotypical masculine (strong, fearless, aggressive).

**Feedback**: _The idea of analysing gender gap in movies is interesing. Nevertheless, rhe procedure you describe does not seem to bring to answer the questions you are asking at the beginning. If you categorize the agonists of movies into stereotypical / non-stereotypical, how can it help in answering what role women have in the movies? Let’s say you have a woman agonist which does not fall into “beautiful, caring, polite” sterotype. What can you infer about her? I think you need to think a bit more on the direction you want to take and how you plan on doing it. Do you want to investigate the quantity of women agonists over time? Do you want to investigate whether women ever get attributes which are sterotipically associated with masculine characters?_
