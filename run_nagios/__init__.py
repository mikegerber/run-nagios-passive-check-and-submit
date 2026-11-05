import os.path
import subprocess

import requests
import yaml
from bs4 import BeautifulSoup


def run_check(check):
    try:
        plugin_output = subprocess.check_output(check)
        plugin_state = 0
    except subprocess.CalledProcessError as e:
        plugin_output = e.output
        plugin_state = e.returncode
    plugin_output = plugin_output.strip()
    if len(plugin_output) > 0:
        # The CGI does not like multiple lines
        plugin_output = b' '.join(plugin_output.splitlines())
    else:
        plugin_output = '(no output from plugin)'

    return plugin_state, plugin_output


def submit_result(host, service, plugin_state, plugin_output):
    config_filename = '~/.config/run-nagios-passive-check-and-submit.yaml'
    with open(os.path.expanduser(config_filename)) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    # cmd_typ depends on whether we submit a service or host check result
    cmd_typ = 30 if service else 87

    # Shorten plugin_output
    max_plugin_output_length = 1022
    if len(plugin_output) > max_plugin_output_length:
        plugin_output = plugin_output[:max_plugin_output_length]

    payload = {
        'cmd_typ': cmd_typ,
        'cmd_mod': 2,
        'host': host,
        'service': service,
        'plugin_state': plugin_state,
        'plugin_output': plugin_output,
        'btnSubmit': 'Commit'
    }

    r = requests.get(config['nagios_url'], params=payload,
                     auth=(config['nagios_user'], config['nagios_pass']),
                     verify=config['ca_bundle'])

    # Extract error message if any
    soup = BeautifulSoup(r.content, 'lxml')
    error_div = soup.find('div', attrs={'class': 'errorMessage'})
    error_text = error_div.text if error_div else None

    return (r.status_code, error_text)
