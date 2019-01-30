#!/usr/bin/env python

from __future__ import print_function
import requests
import os
import sys
import re

# Travis-CI generic image has requests==2.2.1
# json methods were introduced in 2.4.2
# let's keep it short and avoid a pip install
import json


def main():
	xml = os.path.join(
		os.path.dirname(__file__),
		os.pardir,
		'addon.xml',
	)
	plugin_id = re.search(
		r'<addon id="(.*?)"',
		open(xml).read()
	).group(1)

	r = requests.post(
		os.environ['KODI_REPO_TRAVIS'],
		# with requests 2.4.2, could use `json=` instead
		data=json.dumps({
			'request': {
				'message': 'update {plugin_id} (from {TRAVIS_REPO_SLUG})'.format(plugin_id=plugin_id, **os.environ),
				'config': {
					'script': '.github/update.sh https://github.com/{TRAVIS_REPO_SLUG} {TRAVIS_TAG}'.format(**os.environ),
				}
			}
		}),
		headers={
			'Content-Type': 'application/json',
         	'Accept': 'application/json',
         	'Travis-API-Version': '3',
         	'Authorization': 'token {API_TRAVIS_TOKEN}'.format(**os.environ),
		}
	)
	try:
		# with requests 2.4.2, could use `.json()` instead
		rj = json.loads(r.content.decode())
		if rj['@type'] == 'error':
			print(r.content.decode())
			print(rj['error_message'], file=sys.stderr)
			exit(1)
		else:
			print(r.content.decode())
	except ValueError:
		print(r.status_code, file=sys.stderr)
		print(r.content.decode(), file=sys.stderr)
		exit(1)


if __name__ == '__main__':
	main()
