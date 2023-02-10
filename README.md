# Mastodon Francis Bot

This bot is used to toot words from the [DELF](https://www.alliance-francaise.co.nz/diplomas/delf-and-dalf/) test to help people study.

## Audio

- https://github.com/TensorSpeech/TensorFlowTTS

Requires tensorflow (inference done on the CPU)

## Images

- https://github.com/robrohan/stable-diffusion-tensorflow

Requires tensorflow and stable diffusion (inference can done on the CPU)

## Video

Requires the above, and FFMPG to be installed

## Database

See _data/import.sql_. Currently just uses _data/words.tsv_ and _data/sentences.tsv_

```
make database
```

## 

```
sqlite3 ~/Downloads/collection.anki21
sqlite> .headers on
sqlite> .mode csv
sqlite> .output data.csv
sqlite> select flds from notes;
sqlite> .quit
```

Replace the [1F] char with the ';' char

```
cat data.csv | awk -F";" '{print $1"\t"$6 $7"\t"$4"\t"$5 }' > step1.tsv
```

Replace the html text in the _step1.tsv_ file.

