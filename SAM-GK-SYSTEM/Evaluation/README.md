## This Directory contains scripts that reformat files and transfers files to downstream systems e.g. the Evaluator or API
### evaluateData.py
Evaluates the data.

For now:
Real Data is deemed to have a Pearson Correlation Coefficient of greater than or equal to 0.75 or less than or equal to -0.75; along with a Kolmogorov-Smirnov p-value of greater than or equal to 0.05. Some statistical guidance might be helpful.

### transferEvaluationsToMiddleware.py
Transfers evaluated files to the Middleware
