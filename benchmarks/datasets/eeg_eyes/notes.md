#EEG Eye Dataset

**Reference**: http://archive.ics.uci.edu/ml/datasets/EEG+Eye+State

All data is from one continuous EEG measurement with the Emotiv EEG Neuroheadset. The duration of the measurement was 117 seconds. The eye state was detected via a camera during the EEG measurement and added later manually to the file after analysing the video frames. '1' indicates the eye-closed and '0' the eye-open state. All values are in chronological order with the first measured value at the top of the data.

This a multivariate time series dataset with a binary integer target. We have imputed a random initial timestamp from which measurements start.
