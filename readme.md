# Coding Challenge
I picked challenge #1 (handling gaps in time series data) as I worked with time series data more recently.

## Approach

I spent most of the time trying to understand the structure and shape of the data. Results of that process are documented in `./src/challenge.ipynb`. An interactive version of that notebook is hosted at https://maxthemillion.github.io/challenge/. I recommend to use the latter as the preview in github does not render all charts correctly. The most important findings and further steps that could be taken are summarized below.

### Assumptions/Findings:
* Data originates from manually controlled production process
* The time series is intermitted, meaning there are temperature readings for multiple hours a day but there are large gaps between individual daily series.
* Normal pattern for heating_temperatures starts at lowest value each day (at around 25) and increases to about 35 each day. This repeats on a daily basis
* Normal pattern for cooling_temperatures starts high and drops to 15 quickly multiple times per day
* Abnormal patterns that should be detected by an algorithm are all other data patterns that deviate from the described ones above.

### What could be the target in a real life scenario:

In a real life scenario we may want to be able to check data in real time and produce an in case temperature readings enter abnormal territory as this may hint at critical flaws in the production process.

### What is required to set up such an alerting system:

1. **Algorithm that classifies data as normal/abnormal:** We'd require a system that does the classification of normal/abnormal data points for us. We have multiple options at hand including quite complex ones that use classification or prediction approaches, I outline a simple one below.
1. **Production-ready code:** The notebook provided only shows how I would do an exploratory analysis when confronted with data for the first time. I would go from here and write standard Python code which can be used to be run in a productive environment and which is also tested with pytest or equivalent libraries.

### How to create an anomaly detection algorithm?

Multiple options are available for anomaly detection in this context. I conclude by lining out one simple option that does not require filling gaps in the timeseries other than resampling to hourly frequency and normalizing it to the start of each production process:

*Statistical Analysis based on normalized daily time series:*

In continuation of my approach to split the timeseries by days or weeks outlined in the Jupyter notebook, we could go a step further and normalize all daily curves not just by the start of the day but to the starttime of the heating/cooling process. As the data is not that large, we could then go ahead and collect those temperature curves that are normal. We'd then have a distribution of normal data points in hourly frequency. Assuming these are normally distributed, we can then determine a threshold: For example, when a temperature reading deviates more than 2 standard deviations from the mean at that point of time in the heating/cooling process, we could produce the alert. This approach would not require us to fill in gaps in the data other than resampling to hourly frequency.
