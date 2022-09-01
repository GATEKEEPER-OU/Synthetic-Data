import config
import glob
import os
import pandas as pd

from scipy.stats import wasserstein_distance
from scipy.stats import ks_2samp
from scipy.stats import pearsonr

# Real Data
evaluationDF = pd.read_csv(config.evaluation_file)

columns = ['userReference', 'Temperature', 'numDisplaysGenerated', 'numDisplaysMissing', 'numDisplaysIncorrect', \
           'Pearson Correlation', 'PC p-value', \
           'Wasserstein', 'Kolmogorov-Smirnov', 'KS p-value']

reportDF = pd.DataFrame(columns = columns)

# Get processed result files
files = glob.glob(config.RESULT_DIR + "/*.csv")

for filename in files:
    head, tail = os.path.split(filename)

    # Processed filename
    reportFile = os.path.join(config.EVALUATION_REPORT_DIR, tail)
    
    # Archive filename
    archiveFile = os.path.join(config.ARCHIVE_DIR, tail)

    # Processed Dataframe
    # processedDF = pd.DataFrame(columns = columns)

    # reading content of csv files
    df = pd.read_csv(filename)

    # File should only contain 1 user and 1 Temperature
    user = df.loc[0]['user']
    temperature = df.loc[0]['Temperature']
    df.drop(['user', 'Temperature'], axis=1, inplace=True)

    # Get the user from the evaluation
    evalDF = evaluationDF.copy()
    evalDF = evalDF[evalDF['user'] == user]
    evalDF.drop(['user'], axis=1, inplace=True)


    # As of 26/08/2022 11:30, the timing model is 60% accurate. So we expect missing data.
    # Nevertheless, the event model is 98% accurate so we expect the data that is generated to be realistic. 
    
    # Get the minimum and maximum normTime from the generated data
    minNT = min(df['normTime'])
    maxNT = max(df['normTime'])

    generatedDisps = set(df["display"])

    evalDF = evalDF.loc[(evalDF['normTime'] >= minNT) & (evalDF['normTime'] <= maxNT)]
    evaluationDisps = set(evalDF["display"])

    # We are interested in the common displays
    generatedData = generatedDisps.intersection(evaluationDisps)

    numMissingDisps = len(evaluationDisps.difference(generatedDisps))
    numIncorrectDisps = len(generatedDisps.difference(evaluationDisps))

    # Use the mean if there are duplicates 
    evalDF = evalDF.groupby(['normTime', 'code', 'display']).mean('value').reset_index()
    df = df.groupby(['normTime', 'code', 'display']).mean('value').reset_index()

    # Stats
    combinedDF = pd.merge(evalDF, df, on=['normTime', 'code', 'display'])
    X1 = combinedDF["value_x"].to_numpy()
    X2 = combinedDF["value_y"].to_numpy()

    wd = wasserstein_distance(X1, X2)
    ks, pvalue = ks_2samp(X1, X2)
    rho, p = pearsonr(X1, X2)

    userReference = tail.replace(".csv", "")
    reportDF.loc[len(reportDF.index)] = [userReference, round(temperature, 2), len(generatedDisps),  \
                 numMissingDisps, numIncorrectDisps, \
                 round(rho, 2), round(p), round(wd,2), round(ks, 2), round(pvalue, 2)]

    reportDF.to_csv(config.report_file, index=False)

    # Examples of plots. Will be tidied up for future reporting
    # WIP
    #import matplotlib.pyplot as plt
    #import seaborn as sns
    #from matplotlib.backends.backend_pdf import PdfPages
    #combinedDF.drop(['normTime'], axis=1, inplace=True)

    #output_filename = os.path.join(config.EVALUATION_REPORT_DIR, userReference + ".pdf")
    #pp = PdfPages(output_filename)
    
    #plot1 = plt.figure(1)
    #pd.plotting.scatter_matrix(combinedDF, diagonal="kde")
    #pp.savefig(plot1, dpi = 300, transparent = True)
    
    #plot2 = plt.figure(2)
    #ax2 = sns.lmplot(x = "value_x", y = "value_y", data=combinedDF, hue="display", fit_reg=False)

    #plot3 = plt.figure(3)
    #ax3 = combinedDF[["value_x", "value_y"]].plot()
    #ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    #pp.savefig(plot2, dpi = 300, transparent = True)
    #pp.savefig(plot3, dpi = 300, transparent = True)
    #pp.close()
