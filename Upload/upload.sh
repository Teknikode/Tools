#!/usr/bin/env bash
# name: teknik-upload
# requires: bash 4.0+, curl

files="$@"

if [[ -z "${files}" ]]; then
	printf 'You must submit a file to be uploaded!\n'
	exit 0
else
	printf 'Uploading file(s) now!'
	n=1
	for i in "$@"; do
		printf "\nUploading file #${n} ... "
		out=$(curl -sf -F file="@${i}" http://upload.teknik.io/includes/upload.php)
		if [[ -n "${out}" ]]; then
			printf "uploaded! Your file can be found at http://u.teknik.io/${out}\n"
		else
			printf 'error uploading file!\n'
		fi
		((n++))
	done
fi
