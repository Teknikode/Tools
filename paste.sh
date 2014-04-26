#!/usr/bin/env bash
# name: teknik-paste
# requires: bash 4.0+, curl

usage() {
    echo "\
Teknik Pastebin Script in BASH \

Usage : $(basename ${0}) [ -t <paste title> ] [ -e <paste expiration> ] [ -f <type of code> ] [ -p <password> ] [ -h ]

<paste title>       Specify the title of paste to be used. (optional)
<paste expiration>  Specify expiration of paste. Either 1 day (1d) or 1 month (1m). Default is never. (optional)
<type of code>      Specify code language used, use any of the following values. (optional and default value is plain text)
<password>          Specify a password to protect your paste. (optional)

=> Some famous [ -f <type of code> ] Values::

php - PHP
actionscript3 - Action Script 3
asp - ASP
bash - BASH script
c - C language
csharp - C#
cpp - C++"
}

querystring="paste=yes"

while getopts "t:f:e:p:h" flags; do
	case "${flags}" in
		h)
			usage
			exit 0
		;;
		t)
			title=$(echo "${OPTARG}" | tr ' ' '%20')
			querystring="${querystring}&title=${title}"
		;;
		e)
			if [[ "${OPTARG}" == "1d" ]]; then
				expiry="d"
			elif [[ "${OPTARG}" == "1m" ]]; then
				expiry="m"
			else
				printf "That is not a valid expiration time. Specify either 1 day (1d) or 1 month (1m)."
				exit 1
			fi
			querystring="${querystring}&expiry=${expiry}"
		;;
		f)
			format="${OPTARG}"
			querystring="${querystring}&format=${format}"
		;;
		p)
			password="${OPTARG}"
			querystring="${querystring}&password=${password}"
		;;
	esac
done	

input="$(</dev/stdin)"

if [[ -n "${input}" ]]; then
	output=$(curl --silent --data "${querystring}" --data-urlencode "code2=${input}" http://p.teknik.io/index.php)
	pasteid=$(grep -Eo '<a HREF="[0-9]*' <<< ${output})
	if [[ -n "${pasteid}" ]]; then
		[[ -n "${title}" ]] && printf "Title Specified: ${title}\n"
		[[ -n "${expiry}" ]] && printf "Expiration Specified: ${expiry}\n"
		[[ -n "${format}" ]] && printf "Paste Format Specified: ${format}\n"
		[[ -n "${password}" ]] && printf "Paste is password protected!\n"
		printf "Your paste can be found at http://p.teknik.io/${pasteid:9}\n"
		exit 0
	else
		printf "There was an error submitting your paste! We are sorry."
		exit 1
	fi
else
	printf "Error! Nothing found on standard input. Did you submit anything to paste?"
	exit 1
fi