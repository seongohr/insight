# Insight Coding Challenge for Data Engineering
## input dataset : censustract-00-10.csv 
I supposed that the name of the input is always 'censustract-00-10.csv'

* fields 


    * GEOID : Concatenated State-County-Census Tract Code
    * ST10 : State FIPS Code
    * COU10 : County FIPS Code
    * TRACT10 : Census Tract Code
    * AREAL10 : Land area (square miles)
    * AREAW10 : Water area (square miles)
    * CSA09 : Combined Statistical Area Code
    * CBSA09 : Core Based Statistical Area (CBSA) Code
    * CBSA_T : Core Based Statistical Area Title
    * MDIV09: Metropolitan Division Code
    * CSI : CBSA Status Indicator (1=Metropolitan statistical area, 2=Micropolitan statistical area, 3=Outside CBSA)
    * COFLG : Central/Outlying County Flag (C=Central county, O=Outlying county)
    * POP00 : Total population (2000)
    * HU00 : Total housing units (2000)
    * POP10 : Total population (2010)
    * HU10 : Total housing units (2010)
    * NPCHG : Numeric population change: 2000 to 2010
    * PPCHG : Percent population change: 2000 to 2010
    * NHCHG : Numeric change in housing units: 2000 to 2010
    * PHCHG : Percent change in housing units: 2000 to 2010
    
## output dataset : report.csv
* fields        
    
    
    * Core Based Statstical Area Code (i.e., CBSA09)
    * Core Based Statistical Area Code Title (i.e., CBSA_T)
    * total number of census tracts
    * total population in the CBSA in 2000
    * total population in the CBSA in 2010
    * average population percent change for census tracts in this CBSA. 
      Round to two decimal places using standard rounding conventions (i.e., Any percentage between 0.005% and 0.010%, inclusive, should round to 0.01% and anything less than 0.005% should round to 0.00%)
    
## Task
* Read the input file and generate the output file named report.csv with the fields specified in the output dataset section above.

## My approach
* Read the input file
    * Save headings and the field numbers as key, value paired dictionary to access the value of the field with field name in the array below.
    * Save other contents as array
    
* Process data
    * Made a dictionary with a key of each Core Based Statistical Area Code(CBSA)
    * Each key(CBSA) has another dictionary with several keys. The structure is like below.
    
    ~~~
    CBSA_dict = { 
                    CBSA : 
                         { 
                           'title': Core Based Statistical Area Title,
                           'tract10': set(census tract code),
                           'num_tract10': total number of census tracts,
                           'pop00' : total population in 2000 within a Core Based Statistical Area,
                           'pop10' : total population in 2010 within a Core Based Statistical Area,
                           'ppchg' : sum of all the percent changes in census tracts within a Core Based Statistical Area,
                           'not_num_tract10' : the number of census tracts with invalid percent changes in the input data.
                                               this is used for calculating average percent changes 
                                               -> sum of percent changes / (num_tract10 - not_num_tract10)
                         }
                }
    ~~~
    
   * Exception Cases
        1. The population in 2000 cannot be converted to numeric data -> set to 0
        2. The population in 2010 cannot be converted to numeric data -> set to 0
        3. The percent change cannot be converted to numeric data (ex. (X)) -> set to 0
           Exclude these cases when calculating average
    
   * Expected output and the dictionary data match
     * Core Based Statstical Area Code (CBSA) : key in CBSA_dict
     * Core Based Statistical Area Code Title (i.e., CBSA_T) : CBSA_dict[CBSA]['title']
     * Total number of census tracts : CBSA_dict[CBSA]['num_tract10']
     * Total population in the CBSA in 2000 : CBSA_dict[CBSA]['pop00']
     * Total population in the CBSA in 2010 : CBSA_dict[CBSA]['pop10']
     * Average population percent change for census tracts in this CBSA :
        * excluded the case with invalid percent change data (ex.(X)) 
        * CBSA_dict[CBSA]['ppchg'] / (CBSA_dict[CBSA]['num_tract10'] - CBSA_dict[CBSA]['not_num_tract10'])

## Run instructions
* Run the run.sh file

 
    sh run.sh
