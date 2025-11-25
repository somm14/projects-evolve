import numpy as np

values1 = {'EXERANY2':
    {1: 'Yes',
    2: 'No',
    7: 'Don’t know/Not Sure',
    9: 'Refused'}
}

values2 = {'SLEPTIM1':
    {77: 'Don’t know/Not Sure',
    99: 'Refused'}
}

values3 = {'SMOKE100':
    {1: 'Yes',
     2: 'No',
     7: 'Don’t know/Not Sure',
     9: 'Refused'}
}

values4 = {'ALCDAY4':
    {range(101, 200): '1 day per week',
    range(201, 300): '2 days per week',
    777: 'Don’t know/Not sure',
    888: 'No drinks in past 30 days',
    999: 'Refused'}
}

values5 = {'MENTHLTH':
    {88: None,
     77: 'Don’t know/Not sure',
     99: 'Refused'}}

values6 = {'GENHLTH':
    {1: 'Excellent',
     2: 'Very good',
     3: 'Good',
     4: 'Fair',
     5: 'Poor',
     7: 'Don’t know/Not Sure',
     9: 'Refused'}}

values7 = {'PHYSHLTH':
    {77: 'Don’t know/Not sure',
     99: 'Refused'}}

values8 = {'DIABETE4':
    {1: 'Yes',
     2: 'Yes, but female told only during pregnancy',
     3: 'No',
     4: 'Pre-diabetes or borderline diabetes',
     7: 'Don’t know/Not Sure',
     9: 'Refused'}}

values9 = {'CVDCRHD4':
    {1: 'Yes',
     2: 'No',
     7: 'Don’t know/Not sure',
     9: 'Refused'}}

values10 = {'ASTHMA3':
    {1: 'Yes',
     2: 'No',
     7: 'Don’t know/Not sure',
     9: 'Refused'}}

values11 = {'CHCOCNC1':
    {1: 'Yes',
     2: 'No',
     7: 'Don’t know/Not sure',
     9: 'Refused'}}

values12 = {'COLGSEX1':
    {1: 'Male',
     2: 'Female'}}

values13 = {'_AGEG5YR':
    {1: 'Age 18 to 24',
     2: 'Age 25 to 29',
     3: 'Age 30 to 34',
     4: 'Age 35 to 39',
     5: 'Age 30 to 44',
     6: 'Age 45 to 49',
     7: 'Age 50 to 54',
     8: 'Age 55 to 59',
     9: 'Age 60 to 64',
     10: 'Age 65 to 69',
     11: 'Age 70 to 74',
     12: 'Age 75 to 79',
     13: 'Age 80 or older',
     14: np.nan}}

values14 = {'INCOME3':
    {1: 'Less than $10,000',
     2: '$10,000 to < $15,000',
     3: '$15,000 to < $20,000',
     4: '$20,000 to < $25,000',
     5: '$25,000 to < $35,000',
     6: '$35,000 to < $50,000',
     7: '$50,000 to < $75,000',
     8: '$75,000 to < $100,000',
     9: '$100,000 to < $150,000',
     10: '$150,000 to < $200,000',
     11: '$200,000 or more',
     77: 'Don’t know/Not sure',
     99: 'Refused'}}

values15 = {'_EDUCAG':
    {1: 'Did not graduate High School',
     2: 'Graduated High School',
     3: 'Attended College or Technical School',
     4: 'Graduated from College or Technical School',
     9: np.nan}}

values16 = {'EMPLOY1':
    {1: 'Employed for wages',
     2: 'Self-employed',
     3: 'Out of work for 1 year or more',
     4: 'Out of work for less than 1 year',
     5: 'A homemaker',
     6: 'A student',
     7: 'Retired',
     8: 'Unable to work',
     9: 'Refused'}}

values17 = {'_STATE':
    {1: 'Alabama',
     2: 'Alaska',
     4: 'Arizona',
     5: 'Arkansas',
     6: 'California',
     8: 'Colorado',
     9: 'Connecticut',
     10: 'Delaware',
     11: 'District of Columbia',
     12: 'Florida',
     13: 'Georgia',
     15: 'Hawaii', 
     16: 'Idaho',
     17: 'Illinois',
     18: 'Indiana',
     19: 'Iowa',
     20: 'Kansas',
     21: 'Kentucky',
     22: 'Louisiana',
     23: 'Maine',
     24: 'Maryland',
     25: 'Massachusetts',
     26: 'Michigan',
     27: 'Minnesota',
     28: 'Mississippi',
     29: 'Missouri',
     30: 'Montana',
     31: 'Nebraska',
     32: 'Nevada',
     33: 'New Hampshire',
     34: 'New Jersey',
     35: 'New Mexico',
     36: 'New York',
     37: 'North Carolina',
     38: 'North Dakota',
     39: 'Ohio',
     40: 'Oklahoma',
     41: 'Oregon',
     42: 'Pennsylvania',
     44: 'Rhode Island',
     45: 'South Carolina',
     46: 'South Dakota',
     47: 'Tennessee',
     48: 'Texas',
     49: 'Utah',
     50: 'Vermont',
     51: 'Virginia',
     53: 'Washington',
     54: 'West Virginia',
     55: 'Wisconsin',
     56: 'Wyoming',
     66: 'Guam',
     72: 'Puerto Rico',
     78: 'Virgin Islands'}}

values18 = {'_BMI5CAT':
    {1: 'Underweight',
     2: 'Normal Weight',
     3: 'Overweight',
     4: 'Obese'}}