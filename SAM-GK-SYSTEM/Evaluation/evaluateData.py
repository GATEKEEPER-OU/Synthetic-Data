import config
import glob
import os
import pandas as pd

from scipy.stats import wasserstein_distance
from scipy.stats import ks_2samp
from scipy.stats import pearsonr

# Real Data
evaluationDF = pd.read_csv(config.evaluation_file)

columns = ['userReference', 'Temperature', 'numGenerated', 'numIncorrect',  'Pearson Correlation', \
           'Wasserstein', 'Kolmogorov-Smirnov', 'KS p-value']

reportDF = pd.DataFrame(columns = columns)

# Get processed result files
files = glob.glob(config.RESULT_DIR + "/*.csv")

for filename in files:
  head, tail = os.path.split(filename)

  # Report file
  reportFile = os.path.join(config.EVALUATION_REPORT_DIR, tail)

  # reading content of csv files
  df = pd.read_csv(filename)

  # File should only contain1 Temperature
  temperature = df.loc[0]['Temperature']
  df.drop(['Temperature'], axis=1, inplace=True)
  numGenerated = len(df)

  # We remove rows that have a value of -1. 
  # This means that either the orignal JSON result was flawed, or
  # something was missed in the JSON parsing.
  indexes = df[df['value'] == -1].index
  df.drop(indexes,inplace=True)
  numIncorrect = len(indexes)

  wd = ks = pvalue = cor = 0

  if len(df) > 0:
    origDF = df.copy()

    evalDF = evaluationDF.copy()

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

    # Use the mean if there are duplicates. There shouldn't be 
    evalDF = evalDF.groupby(['normTime', 'coding', 'display']).mean('value').reset_index()
    df = df.groupby(['normTime', 'coding', 'display']).mean('value').reset_index()

    # Stats
    combinedDF = pd.merge(evalDF, df, on=['normTime', 'coding', 'display'])

    X1 = combinedDF["value_x"].to_numpy()
    X2 = combinedDF["value_y"].to_numpy()

    if len(X1) > 1:
      wd = wasserstein_distance(X1, X2)
      ks, pvalue = ks_2samp(X1, X2)
      cor = pearsonr(X1, X2).statistic
    else:
      ks = pvalue = cor = 1

  userReference = tail.replace(".csv", "")
  reportDF.loc[len(reportDF.index)] = [userReference, round(temperature, 2), numGenerated, \
               numIncorrect, round(cor, 2), round(wd,2), round(ks, 2), round(pvalue, 2)]

  # For now we accept files with 
  # pvalue > 0.05 and cor >= 0.75 or <= -0.75
  if (pvalue >= 0.05) and (cor >= 0.75 or cor <= -0.75):
    try:
      filen = os.path.join(config.REAL_DIR, tail)
      origDF['userReference'] = userReference
      fileType = "real"
      origDF.to_csv(filen, index=False)
      os.remove(filename)
    except:
      pass
  else:
    filen = os.path.join(config.FAKE_DIR, tail)
    fileType = "fake"
    os.rename(filename, filen)

  # Examples of plots.
  import matplotlib.pyplot as plt
  import seaborn as sns
  from matplotlib.backends.backend_pdf import PdfPages
    
  combinedDF.drop(['normTime'], axis=1, inplace=True)
    
  pdfFile = userReference + "_" + str(round(temperature, 2)) + '_' + fileType + ".pdf"

  output_filename = os.path.join(config.EVALUATION_REPORT_DIR, pdfFile)
  pp = PdfPages(output_filename)
    
  pd.plotting.scatter_matrix(combinedDF, diagonal="kde")
  pp.savefig(dpi = 300, transparent = True)
  plt.close()
    
  pd.plotting.scatter_matrix(combinedDF, diagonal="hist")
  pp.savefig(dpi = 300, transparent = True)
  plt.close()
    
  sns.lmplot(x = "value_x", y = "value_y", data=combinedDF, hue="display", fit_reg=False)
  pp.savefig(dpi = 300, transparent = True)
  plt.close()

  ax = combinedDF[["value_x", "value_y"]].plot()
  #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  pp.savefig(dpi = 300, transparent = True)
  plt.close()
  pp.close()

reportDF.to_csv(config.report_file, index=False)