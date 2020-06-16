# Introduction
This script merge the test measurements with the according test outcomes. With `JUnit` it is not possible to get the test outcome in a teardown fixture. Therefore this information must be extracted from the test reports.

# Usage
The parameters are specified inside the script. You probably need to adapt the followng parameters:
- `MEASUREMENT_PATH`: Path to your measurements without information about the test outcome
- `SUREFIRE_REPORTS_PATH`: Path to the folder where all the test reporst are located
- `OUTPUT_FILE_PATH`: Desired path to final merged data set

Within this section you can adapt the parameters:
```{python}
######### PARAMETERS ##########
ROOT = os.getcwd()
MEASUREMENT_PATH = ROOT+"/measurements.csv"
SUREFIRE_REPORTS_PATH = ROOT+"/16052020_VM6_SOURCETRANS_V2_NO-GC/surefire-results"
OUTPUT_FILE_PATH = ROOT+"/data-merge-output.csv"
RED='\033[0;31m'
NC='\033[0m'
######### PARAMETERS ##########
```

With this command you run the script:
```{bash}
./merge_results_and_measurements.py
```
