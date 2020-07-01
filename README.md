# audio2BIDSstim

Helper functions for processing a stimulus into a BIDS compliant format.

Use with `python wav_files_to_bids_tsv.py path/to/your/wavfiles/*.wav -c path/to/your/config.json`.
By default extracts Mel spectrograms.

You have to copy the resulting tsv.gz and json files into your BIDS dataset and rename them according to your conditions/runs.
