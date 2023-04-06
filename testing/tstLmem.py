import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri, Formula
from rpy2.robjects.packages import importr

# Activate the automatic conversion between pandas and R data frames
pandas2ri.activate()

# Import the R packages we need
base = importr('base')
stats = importr('stats')
lme4 = importr('lme4')

# Generate random data
np.random.seed(42)
n_subjects = 10
n_obs_per_subject = 10
n = n_subjects * n_obs_per_subject
groups = 5
group_labels = [f'Group_{i + 1}' for i in range(groups)]
subject_labels = [f'Subject_{i + 1}' for i in range(n_subjects)]

data = {
    'response': np.random.normal(0, 1, n),
    'fixed_effect': np.random.normal(0, 1, n),
    'group': np.random.choice(group_labels, n),
    'subject': np.repeat(subject_labels, n_obs_per_subject)
}

# Create a pandas data frame from the data
import pandas as pd
df = pd.DataFrame(data)

# Fit the linear mixed-effects model using the lmer function
formula = Formula('response ~ fixed_effect + (1|group) + (1|subject)')
model = lme4.lmer(formula, data=df)

# Display the model summary
summary = base.summary(model)
print(summary)

 #Assuming your data is stored in a DataFrame named 'df'
subject_counts = df['subject'].value_counts()
print(subject_counts)