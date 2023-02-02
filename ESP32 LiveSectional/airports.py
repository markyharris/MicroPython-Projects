# airports.py
#
# Define the airports dictionary. Format: 'Pin Number of LEDs:"Airport ID"',
# Use a site like www.skyvector.com to find airports who report METAR's.
# Be sure to use the 4 character identifier, i.e. "KPHX" and be sure to quote the identifier.
# To setup an LED pin to be a legend LED use the following designators at the appropriate pin number;
#    "LG_VFR" - denote a legend item as VFR
#    "LG_MVFR" - denote a legend item as MVFR
#    "LG_IFR" - denote a legend item as IFR
#    "LG_LIFR" - denote a legend item as LIFR
#    "LG_NOWX" - denote a legend item as an airport not currently reporting weather
# If none of these are used, then no Legend will be displayed.
#
# A few examples provided below. The list named 'airports' will be used.
# So be sure only one list is named 'airports'.

# Phoenix Terminal Area Chart airports
airports = {
    0:"KDVT",
    1:"KSDL",
    2:"KLUF",
    3:"KGEU",
    4:"KBXK",
    5:"KGYR",
    6:"KPHX",
    7:"KFFZ",
    8:"KCHD",
    9:"KIWA",
    10:"KP08",
    11:"KCGZ",
    12:"KA39",
    13:"KGXF",
    14:"LG_NOWX",
    15:"LG_LIFR",
    16:"LG_IFR",
    17:"LG_MVFR",
    18:"LG_VFR",
    }

# San Francisco Terminal Area Chart airports
airports_SF = {
    0:"KDVO",
    1:"KCCR",
    2:"KL83",
    3:"KTCY",
    4:"KLVK",
    5:"KOAK",
    6:"KSFO",
    7:"KHAF",
    8:"KSQL",
    9:"KNVQ",
    10:"KSJC",
    11:"KRHV",
    12:"KE16",
    }

# Test list used for debugging
airports_test = {
    0:"LG_VFR",
    1:"LG_MVFR",
    2:"LG_IFR",
    3:"LG_LIFR",
    4:"LG_NOWX",
    5:"KJWH",
    6:"KPHX",
    7:"KFFZ",
    8:"KCHD",
    9:"KIWA",
    10:"KEOE",
    11:"KBLF",
    12:"KASJ",
    13:"CYQA",
    }

