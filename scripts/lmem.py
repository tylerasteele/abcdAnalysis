
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

try:
    # Import R's utility package
    utils = importr('utils')

    # Check if lme4 is installed
    installed_packages = utils.installed_packages()
    if 'lme4' not in installed_packages:
        print("Installing 'lme4' package in R.")
        utils.install_packages('lme4')

    # Import lme4
    lme4 = importr('lme4')

    # Run a simple linear mixed-effects model (LMM) using lme4
    r_code = '''
        library(lme4)
        data(sleepstudy)
        lmm <- lmer(Reaction ~ Days + (1|Subject), data = sleepstudy)
        summary(lmm)
    '''
    summary = robjects.r(r_code)
    print(summary)

except Exception as e:
    print("Error:", e)















"""
import rpy2.objects as robjects, pandas as pd 
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


robjects.r('install.packages("lme4")')
robjects.r('library(lme4)')


# Create a pandas DataFrame from your dictionary
patients_df = ...

# Convert the pandas DataFrame to an R DataFrame
with localconverter(robjects.default_converter + pandas2ri.converter):
    r_data = robjects.conversion.py2rpy(patients_df)

# Define the R formula for the model
formula = 'fmri_measurement ~ timepoint + (1|patientID)'

# Call the lmer() function from the lme4 package
lmer = robjects.r['lmer']
model = lmer(formula, data=r_data)

# Get model summary
summary = robjects.r['summary']
print(summary(model))

"""

