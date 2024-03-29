# Fake-News-Project

**Update July 2023**: This was the code for my MEng Final Year Project. 
I originally intended to have this all nicely written up after submitting my dissertation, but the thought of freedom after 6 months of hard work on this very quickly overtook any desire I had to look at this code again for the immediate weeks/months proceeding the end of my degree. This has been an ongoing feeling until as of late. For the time being, please have a quick look over this readme for a brief explanation of what this project was about, some of the screenshots of the working project by the time I had to present, and some things I aim to do to offically 'finish' this.

> **Note**: Please also understand that this is code representative of what knowledge and skill I **_had_** as a final year university student.

## Tech stack
- Javascript, React
- Python, Flask
- MySQL 8.0
- Google Cloud Platform
- Docker

## System Diagram
![image](https://github.com/hotinglok/Fake-News-Project/assets/53564281/c322d84d-4f23-446d-9e2d-988bb924ee99)

## Overview
This is a web-app that allows a user to search for news articles about the same story from the four most viewed UK news providers (based on Ofcom 2020 data) and show how similar two chosen articles are by grouping paragraphs into statements that are shared/not shared between chosen articles. This is to help a user better infer which statements could be considered 'facts' based on consistency of the information presented and gain a better understanding of how each news provider prioritises and presents the information they publish. For example, there could be intention shown by one news provider showing a statistic/quotation early on in the article compared to another which shows the same statistc/quotation towards the end of an article or not even at all. 

#### User Journey
- User enters a keyword(s) to search for on any given date/range of dates.
- Articles containing keyword displayed for each news provider.
- User selects a 'root' article, web-app returns articles most likely to be about the same story based on title/description of articles.
- User selects second article to compare 'root' article to.
- Analysis is done and the final comparison screen with sorted paragraphs is shown.
  - Information about the articles such as title, publication/modification dates, keywords are displayed.
  - Paragraphs are sorted into 'quotations', 'stats', and any paragraphs which do not contain direct quotations or statistics.
- User can freely re-arrange paragraphs in case any errors occur with the similarity algorithm used.

## Screenshots
### Initial search screen
![image](https://github.com/hotinglok/Fake-News-Project/assets/53564281/cb1bc735-9b57-4a03-8721-4e8c979461bc)

### Display of found articles (after searching 'cat') and selection of 'root' article
![image](https://github.com/hotinglok/Fake-News-Project/assets/53564281/b92f74a0-40f4-46eb-9203-3ae3cf5bd062)

### Choosing second article to compare with
![image](https://github.com/hotinglok/Fake-News-Project/assets/53564281/22412160-f5e4-4d1c-8743-1cecb223f26f)

### Final outputted comparison screen (pt.1)
![image](https://github.com/hotinglok/Fake-News-Project/assets/53564281/cd5d2ca0-e0a5-45b7-8f1a-cdf3cf5ae778)

### Final outputted comparison screen (pt.2)
![image](https://github.com/hotinglok/Fake-News-Project/assets/53564281/90060339-0027-4346-8be6-146ee843633c)

### Final outputted comparison screen (pt.3)
![analysis_2](https://github.com/hotinglok/Fake-News-Project/assets/53564281/d157c30e-ecab-4474-a00b-05fd7d47ddb9)

## Project Description
The area I chose to focus on was _Fake News_. Myself and many others were deeply affected by the pandemic, so much so that I found myself very reliant on news media in the hopes that things could get better. Given the spike in relevancy of this topic with the incredible amount of misinformation that was brought to light every day/week, I had found the motivation to try and make something I would personally find useful if no one else.

The problem with most Fake News projects at the time of my research was that many software-based solutions were not very nuanced. Many have tried making fake news 'detectors' using machine learning models, attempting to programmatically discern whether a piece of text was 'fake' or 'real' by trying to find patterns in large volumes of scraped articles from around the world. However, I proposed that these approaches could always be considered flawed because there is no singular definition of 'fake news', hence these kinds of approaches lack the nuance to provide meaningful results.

As such, I wanted to make a tool which helped people better compare information they were given in a more short-form medium to better highlight which information can be cross-referenced between multiple sources and which could not.

## Things to do post writing this up
- Create a dummy database with real scraped data.
- Edit any functions that would have previously connected to a GCP Cloud DB to use the local database.
- Fix filepaths
- Deploy somewhere
