# NLP-Project

## Project structure

Notes in all files
The directory contains a copy of the external GitHub repo, converted to python 3 and cleaned a bit:
- seless files (and dependencies) have been removed
- the code contained in the `main.py` file has been transformed into a function that can be imported from other files

When adding dependencies you should run `pipreqs . --force` from the root directory, after installing it with `pip install pipreqs`.

### Notes

- Sentence pairs 99 and 129 removed from dataset because they do not belong in it (source https://semanticsimilarity.files.wordpress.com/2013/11/trmmucca20131_12.pdf)
- Addded library spacy, `pip install spacy` then added en_core_web_sm using `python -m spacy download en_core_web_sm`  please fix requirements file as i did not want to try and break it :)
