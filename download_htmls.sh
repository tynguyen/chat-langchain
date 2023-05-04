#!/bin/bash

input_file=".html/13K-cleaned-can-total-urls.txt"
base_dir=".html"

count = 0
while read url; do
    # Skip empty lines
    if [ -z "$url" ]; then
        continue
    fi
    # Create the directory path based on the URL
    sub_dir="${url#https://}"
    sub_dir="${sub_dir%/*}"

	echo "-----------------------------------------------------"
	echo "Processing URL: $url"
	echo " ---> sub_dir:  $sub_dir"

    # Create the directory if it doesn't exist
    if ! test -d "$base_dir/$sub_dir"; then
        mkdir -p "$base_dir/$sub_dir"
		echo " ---> create:  $base_dir/$sub_dir"
    fi

    # Download the HTML file and save it to the target directory
    curl -o "$base_dir/$sub_dir/$(basename $url)" "$url"
	((count++))
	echo " ---> [count: $count] Downloaded and saved:  $url"
done < "$input_file"

echo "-----------------------------------------------------------"
echo "Proceeded $count urls in total!!!"
