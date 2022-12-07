# Exploratory Data Analysis (EDA) on Anime Data from MyAnimeList
--------------------------------------

<p align="center">
    <img src="https://github.com/RealXun/EDA_ANIME/blob/main/src/images/cover.png" width="1000">
</p>

## Introduction to Anime (Japanese Animation)
--------------------------------------

<div align="justify">"Anime" is the term used by Western audiences to describe Japanese animated films and television programs (although it is used to describe any animation in Japan).
  
At first, animated pieces were known as senga eiga (線画映画, line-drawing film) or senga kigeki (線画喜劇, cartoon comedy film), which were often specified in katakana (cartoon comedy, カートン・コメディ, cartoon comedy).

Between 1907 and 1912 the first animated shorts were made, usually associated with political cartoonists, and in 1933 came the first piece of Japanese animation or spoken Japanese anime, Chikara to Onna Yo no Naka.

The following years would be, logically, marked by the war, and almost any audiovisual piece would be focused on a propaganda use. In 1948, one of the most important studios, Toei Animation, was born, and in 1958 it made the first color film, Hakujaden (白蛇伝, The Tale of the White Snake).

It was probably not until 1962 that the word anime began to be used, in a standardized way, in Japan to refer to animated productions. It seems that the film magazine Eiga Hyoron was the first.

During the 1970s some of the most popular anime in the country were born, such as Ashita no Joe (1970, Fuji TV), Arupusu no Shoujo Haiji (Heidi, 1974, Fuji TV), Lupin III (1971, YTV), Gatchaman (1972, Fuji TV), Mazinger Z (1972, Fuji TV), Uchuu Senkan Yamato (1974, YTV), Candy Candy (1976, TV Asahi) or Kidou Senshi Gundam (1979, NBN), but it was not until the 1980s when a real revolution would take place.

The first half of the 1990s saw the emergence of a new type of animation that was ready to blow the brains of viewers and burst the expectations of everything seen until then in cartoons. It was Japanese anime and there is no doubt that the two culprits of this irruption were Dragon Ball and Akira, two authentic bombshells that made us become aware of this new style of animation. These phenomena were accompanied by the arrival of private television stations, with many hours of programming to fill, which were busy with lots of Japanese anime series that were cheap to license. New publishers emerged, acquiring the rights to anime films destined to fill the shelves of video stores in response to this new demand.

Today's teenagers are getting hooked on Japanese anime again. It's happening to them as it happened in the 90s, for example, with Dragon Ball, The Knights of the Zodiac (Saint Seiya) or Chicho Earthquake (Chicho Terremoto - Dash Kappei). Not to mention the Dragon Ball phenomenon. It is true that now there are also many adults who maintain their taste for the series and movies created by the famous Japanese anime studios, and that has an influence.

Anime may be going through one of its best periods in history. The genre has audiences almost everywhere in the world. The stories are reaching diverse audiences and, technology permitting, a series of tools are available to improve manga adaptations or new proposals. A boom.</div>

## About the work done
--------------------------------------

Usually when we think of Data Science, Machine Learning or Artificial Intelligence, we think of the models and the wonderful applications, but the first step is usually to explore and clean the data.

The purpose of this EDA is getting insights out of data while exploring it (after doing some Data cleaning/preparation/transformation) in order to answer some previos questions and prove some hypothesis.

The parts in the proyect is as follows:

- Data Preparation, Cleaning and Descriptive Analysis
- Data and Visual Analysis
- Conclusions
- References

[Click here to open the Jupyter Notebook](https://github.com/RealXun/EDA_ANIME/blob/eb2d58dcfe9fffe1b481e7d7da5557491d2300a3/src/EDA_Anime.ipynb)

## Libraries used
--------------------------------------
```
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import seaborn as sns
from collections import Counter
from scipy.stats import chi2_contingency
from sklearn.linear_model import LinearRegression
```

## Questions and Hypothesis
--------------------------------------
- Which is the most common anime source?
- Which is the most coomon anime typ?
- PG-13 - Teens 13 or older has more animes int he top 10.
- Is PG-13 - Teens 13 or older the most typical rating for animea?
- Which genre is most release? Is this gender the more voted between the audience?
- Find out the best anime Producer and Studio
- Find out the most voted Theme and Genre for an anime. Are this the ones with more releases?
- Is there any correlation between having more votes and getting higher score?
- More Number of Episodes does not mean higher score. Therefore, Is there any correlation between having a higher Score and the Number of Episodes?
- Longer duration of the episodes means higher score. Therefore, Is there any correlation between having a higher Score and the Duration of the episodes?

