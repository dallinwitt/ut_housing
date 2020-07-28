# Utah Housing Affordability by County
## Data Analysis and Visualization

#### Motivation
As someone looking to buy a home in Utah right now, the relative affordability of Utah's largest counties is of direct concern to me, as is the general economic wellbeing of my home state. In order to get a perception of trends in housing affordability, I used county-level economic data from the [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/categories/30154), and county-level housing price data from the [Utah open data catalog](https://opendata.utah.gov/Social-Services/Average-Price-3-Bedroom-Homes-By-County-In-Utah-19/5icz-nmjb). 

#### Methods
I cleaned and merged the two datasets using Pandas, Numpy, and glob packages. The economic dataset and housing price datasets used different sampling frequencies so I had to resample both datasets to get them to be able to merge on a datetime index. This meant that the income data had to be linearly interpolated, which may have had some impact on the month-level accuracy of the ratio figures.

All visualization was done in R, using dplyr and ggplot2. I stacked the line plots to give a consistent sense of time between the three metrics plotted. 

#### Outcomes
The data showed a few interesting and unexpected features:
* Despite consistently being the most expensive county to live in, Wasatch County is relatively middle-of-the-pack in terms of income level.
* Washington County was the first to experience both the boom and bust of the housing crisis of 2007-2009.
* Wasatch and Washington Counties experienced the largest booms leading up to the housing crisis. 
* Tooele, Davis, and Weber Counties have consistently been the most affordable of Utah's largest counties.
