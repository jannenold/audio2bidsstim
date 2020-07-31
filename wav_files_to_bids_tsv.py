import numpy as np
import joblib
import glob
import json
import os
import librosa as lbr

def your_own_feature_extractor(filename,  **kwargs):
    '''Template for your own feature extractor.
    
    It needs to process a filename and return three variables:
    an ndarray of features of shape (samples, features), 
    the sampling rate of the features in Hz,
    names for the columns of each features

    Parameters
    ----------
    filename : str, path to wav file to be converted

    Returns
    -------
    '''
    pass

def get_mel_spectrogram(filename, log=True, sr=44100, hop_length=512, **kwargs):
    '''Returns the (log) Mel spectrogram of a given wav file, the sampling rate of that spectrogram and names of the frequencies in the Mel spectrogram

    Parameters
    ----------
    filename : str, path to wav file to be converted
    sr : int, sampling rate for wav file
         if this differs from actual sampling rate in wav it will be resampled
    log : bool, indicates if log mel spectrogram will be returned
    kwargs : additional keyword arguments that will be
             transferred to librosa's melspectrogram function

    Returns
    -------
    a tuple consisting of the Melspectrogram of shape (time, mels), the repetition time in seconds, and the frequencies of the Mel filters in Hertz 
    '''
    wav, _ = lbr.load(filename, sr=sr)
    melspecgrams = lbr.feature.melspectrogram(y=wav, sr=sr, hop_length=hop_length,
                                              **kwargs)
    if log:
        melspecgrams[np.isclose(melspecgrams, 0)] = np.finfo(melspecgrams.dtype).eps
        melspecgrams = np.log(melspecgrams)
    log_dict = {True: 'Log ', False: ''}
    freqs = lbr.core.mel_frequencies(
            **{param: kwargs[param] for param in ['n_mels', 'fmin', 'fmax', 'htk']
                if param in kwargs})
    freqs = ['{0:.0f} Hz ({1}Mel)'.format(freq, log_dict[log]) for freq in freqs]
    return melspecgrams.T, sr / hop_length, freqs


if __name__ == '__main__':
    import argparse
    from itertools import cycle
    parser = argparse.ArgumentParser(description='Wav2bids stim converter.')
    parser.add_argument('file', help='Name of file or space separated list of files or glob expression for wav files to be converted.', nargs='+')
    parser.add_argument('-c' ,'--config', help='Path to json file that contains the parameters to librosa\'s melspectrogram function.')
    parser.add_argument('-o', '--output', help='Path to folder where to save tsv and json files, if missing uses current folder.')
    parser.add_argument('-t', '--start-time', help='Start time in seconds relative to first data sample.'
            ' Either a single float (same starting time for all runs) or a list of floats.', nargs='+', type=float, default=0.)
    args = parser.parse_args()

    if args.config:
        with open(args.config, 'r') as fl:
            config = json.load(fl)
    else:
        config = dict()
    if len(args.file) == 1 and '*' in args.file[0]:
        args.file = glob.glob(args.file[0])
    if isinstance(args.start_time, float):
        args.start_time = list(args.start_time)
    if len(args.start_time) > 1 and len(args.start_time) != len(args.file):
        raise ValueError('Number of files and number of start times are unequal. Start time has to be either one element or the same number as number of files.')
    for wav_file, start_time in zip(args.file, cycle(args.start_time)):
        melspec, sr_spec, freqs = get_mel_spectrogram(wav_file, **config)
        tsv_file = os.path.basename(wav_file).split('.')[0] + '.tsv.gz'
        json_file = os.path.basename(wav_file).split('.')[0] + '.json'
        if args.output:
            tsv_file = os.path.join(args.output, tsv_file)
            json_file = os.path.join(args.output, json_file)
        np.savetxt(tsv_file, melspec, delimiter='\t')
        metadata = {'SamplingFrequency': sr_spec, 'StartingTime': start_time,
                    'Columns': freqs}
        with open(json_file, 'w+') as fp:
            json.dump(metadata, fp)


