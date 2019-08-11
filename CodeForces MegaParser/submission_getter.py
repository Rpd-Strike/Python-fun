import urllib.request
import json
import sys
import time, os, re
from bs4 import BeautifulSoup

DOWNLOAD_DIR = 'Solutions'
SUBMISSION_URL = 'http://codeforces.com/contest/{ContestId}/submission/{SubmissionId}'

EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

replacer = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'"}
keys = replacer.keys()

def get_ext(comp_lang):
    if 'C++' in comp_lang:
        return 'cpp'
    for key in EXT_keys:
        if key in comp_lang:
            return EXT[key]
    return ""

def parse(source_code):
    for key in keys:
        source_code = source_code.replace(key, replacer[key])
    return source_code

base_dir = DOWNLOAD_DIR
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

def submission_code(submission):
    con_id, sub_id = submission['contestId'], submission['id']
    prob_name, prob_id = submission['problem']['name'], submission['problem']['index']
    comp_lang = submission['programmingLanguage']
    submission_full_url = SUBMISSION_URL.format(ContestId=con_id, SubmissionId=sub_id)
    print ('%s , Fetching submission: %s' % (str(con_id) + ' ' + prob_id, submission_full_url))
    submission_info = urllib.request.urlopen(submission_full_url).read()
    soup = BeautifulSoup(submission_info, 'html.parser')
    submission_text = soup.find('pre', id='program-source-text')
    if submission_text is None:
        print ('Could not fectch solution %d', sub_id)
        return None
    result = submission_text.text.replace('\r', '')
    ext = get_ext(comp_lang)
    # new_directory = base_dir + '/' + str(con_id) + prob_id
    # if not os.path.exists(new_directory):
    #     os.makedirs(new_directory)
    prob_name = re.sub(r'[\\/*?:"<>|]',"", prob_name)
    # file = open(new_directory + '/' + str(sub_id) + '.' + ext, 'w')
    # file.write(result)
    # file.close()
    return (result, ext)