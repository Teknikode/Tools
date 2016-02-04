#!/usr/bin/env bash
# name: teknik-upload
# creator: KittyKatt
# requires: bash 4.0+, curl

files="$@"

if [[ -z "${files}" ]]; then
	printf 'You must submit a file to be uploaded!\n'
	exit 1
else
	printf 'Uploading file(s) now!'
	n=1
	for i in "$@"; do
		printf "\nUploading file #${n} ... "
		out=$(curl -sf -F file="@${i}" https://api.teknik.io/v1/Upload)
		echo "${out}"
		if [[ "${out}" =~ "error" ]]; then
			printf 'error uploading file!\n'
			exit 1
		else
			out="${out##*Name\":\"}"
			out="${out%%\"*}"
			printf "uploaded! Your file can be found at https://u.teknik.io/${out}\n"
		fi
		((n++))
	done
fi
