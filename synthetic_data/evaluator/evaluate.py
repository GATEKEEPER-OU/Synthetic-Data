def evaluate(input_dir: str , real_dir: str, fake_dir: str, report_file: str, n_days = None):
    import glob
    import os
    import pandas as pd

    from scipy.stats import wasserstein_distance
    from scipy.stats import ks_2samp
    from scipy.stats import pearsonr

    # File to evaluate against. Confidential Data.
    # User information has been removed for demo and file has been aggregated.
    # This impacts on the evaluation. Paper will take into account user information.
    # Confirm with Data Controller before sharing with third-parties.
    # Of course, code can be hacked, so simply reading file from secure location offers no security.
    # Code will also need to be locked down.
    evalFile = os.path.join(os.path.dirname(__file__), 'confidential', 'evaluation.csv')
    evaluationDF = pd.read_csv(evalFile)

    n_seconds = None
    if n_days is not None:
        n_seconds = n_days * 86400

    columns = ['userReference', 'Temperature', 'numGenerated', 'numIncorrect',  'Pearson Correlation', \
            'Wasserstein', 'Kolmogorov-Smirnov', 'KS p-value']

    reportDF = pd.DataFrame(columns = columns)

    # Get processed result files
    files = glob.glob(input_dir + "/*.csv")

    for filename in files:
        print('Evaluating ' + filename)
        _, tail = os.path.split(filename)

        # reading content of csv files
        df = pd.read_csv(filename)

        # File should only contain Temperature
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
            if n_seconds is not None:
                if maxNT - minNT <= n_seconds:
                    n_seconds = None

            evalDF = evalDF.loc[(evalDF['normTime'] >= minNT) & (evalDF['normTime'] <= maxNT)]

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
        # For demo, we have decreased risk. Change metrics to increase the chances of real data
        if (pvalue > 0.01) and (abs(cor) > 0.50):
            try:
                n_keep_min = minNT
                n_keep_max = maxNT
          
                # Return n_days. If n_seconds is none we keep all
                if n_seconds is not None:
                    # There may be gaps. We want to keep the best
                    times = sorted(list(origDF['normTime'].unique()))
                    n_between = 0
                    for i, t1 in enumerate(times):
                        max_time = min(t1 + n_seconds, maxNT)
                        j = i + 1
                        for k, t2 in enumerate(times[j:]):
                            if t2 > max_time:
                                break
                            if (k-i) > n_between:
                                n_between = k - i
                                n_keep_min = t1
                                n_keep_max = t2
                        if max_time == maxNT:
                            # We have the maximum numner
                            break
                    origDF = origDF.loc[(origDF['normTime'] >= n_keep_min) & (origDF['normTime'] <= n_keep_max)]
                filen = os.path.join(real_dir, tail)
                origDF.to_csv(filen, index=False)
                os.remove(filename)
            except:
                pass
        else:
            filen = os.path.join(fake_dir, tail)
            os.rename(filename, filen)

    # Examples plots have been removed. Too much for a simple demo.
    reportDF.to_csv(report_file, index=False)