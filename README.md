### audio2BIDSstim

Helper functions for processing an auditory stimulus into a BIDS compliant format.

Use with `python wav_files_to_bids_tsv.py path/to/your/wavfiles/*.wav -c path/to/your/config.json`.
By default extracts Mel spectrograms.

You have to copy the resulting tsv.gz and json files into your BIDS dataset and rename them according to your conditions/runs.

### Usage

<pre>usage: wav_files_to_bids_tsv.py [-h] [-c CONFIG] [-o OUTPUT]
                                [-t START_TIME [START_TIME ...]]
                                file [file ...]

Wav2bids stim converter.

positional arguments:
  file                  Name of file or space separated list of files or glob
                        expression for wav files to be converted.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to json file that contains the parameters to
                        librosa&apos;s melspectrogram function.
  -o OUTPUT, --output OUTPUT
                        Path to folder where to save tsv and json files, if
                        missing uses current folder.
  -t START_TIME [START_TIME ...], --start-time START_TIME [START_TIME ...]
                        Start time in seconds relative to first data sample.
                        Either a single float (same starting time for all
                        runs) or a list of floats.
</pre>
