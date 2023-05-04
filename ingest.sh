# Bash script to ingest data
# This involves scraping the data from the web and then cleaning up and putting in Weaviate.
# Error if any command fails
set -e
# wget -r -A.html https://langchain.readthedocs.io/en/latest/
bash download_htmls.sh
mkdir .pkl
python3 ingest.py .html .pkl/13K-cleaned-can-total.pkl
