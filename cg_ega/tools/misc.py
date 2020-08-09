from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np

def _any(l, axis=1):
    return np.reshape(np.any(np.concatenate(l, axis=axis), axis=axis), (-1, 1))


def _all(l, axis=1):
    return np.reshape(np.all(np.concatenate(l, axis=axis), axis=axis), (-1, 1))


def reshape_results(results, freq):
    # resampling
    if type(results.index) != type(date.today()): # in case the results objects isn't formatted with dates
        start_time = date.today().strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(minutes=freq*(len(results.index)-1))).strftime("%Y-%m-%d %H:%M:%S")
        index = pd.period_range(start=start_time, end=end_time, freq=str(freq) + 'min').to_timestamp()
        results.index = index
    else:
        start_time = datetime.strptime(results.index[0].strftime('%Y-%m-%d'), '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.strptime(results.index[-1].strftime('%Y-%m-%d'), '%Y-%m-%d') + timedelta(days=1) - timedelta(
            minutes=float(freq))).strftime("%Y-%m-%d %H:%M:%S")
        index = pd.period_range(start=start_time, end=end_time, freq=str(freq) + 'min').to_timestamp()
        results = results.resample(str(freq) + 'min').mean()
        results = results.reindex(index=index)

    # creating the derivatives
    results = pd.concat([results, (results.diff(axis=0) / freq).rename(columns={"y_true": "dy_true", "y_pred": "dy_pred"})],
                        axis=1)

    return results


def extract_columns_from_results(results):
    return np.expand_dims(results.dropna().to_numpy().transpose(),axis=2)