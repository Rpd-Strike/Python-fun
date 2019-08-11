import urllib.request
import json
import os, time
from submission_getter import submission_code

MAX_PROBLEM_SUBS = 1000 * 1000
BASE_DIR = 'Surse'
URL_CONTEST_SUBMISSION = 'https://codeforces.com/api/contest.status?contestId={contestId}'

def submissions_from_contest(contestId):
  url = URL_CONTEST_SUBMISSION.format(contestId=contestId)
  submissions = json.loads(urllib.request.urlopen(url).read())
  return submissions['result']

def save_progress(sources, contestId):
  for prob_id, data in sources.items():
    file_obj = open(BASE_DIR + '/' + str(contestId) + prob_id + '.txt', 'w')
    json.dump(data, file_obj, indent = 2)

def save_contest(contestId):
  submissions = submissions_from_contest(contestId)
  print( 'contest: ' + str(contestId) + ' has ' + str(len(submissions)) + ' submissions' )

  sources, count = {}, 0
  for sub in submissions:
    if sub['verdict'] != 'OK':
      continue
    
    count = count + 1
    if count > MAX_PROBLEM_SUBS:
      break
    
    print('remaining: ' + str(len(submissions) - count + 1))

    prob_id = sub['problem']['index']
    sub_id = str(sub['id'])
    if prob_id not in sources.keys():
      sources[ prob_id ] = {}
    
    code, ext = 'nothing', 'no-ext'
    
    waited_a_lot = False
    while True:
      try:
        code, ext = submission_code(sub)
        break
      except Exception as e:
        print(e)
        if not waited_a_lot:
          print("wwaiting 3 minutes")
          time.sleep(60)
          print("2 minutes left")
          time.sleep(60)
          print("1 minute left")
          time.sleep(60)
          waited_a_lot = True
        else:
          time.sleep(4)
    
    sources[ prob_id ][ sub_id ] = {
      'code': code,
      'ext': ext
    }

    if count % 10 == 0:
      save_progress(sources, contestId)
      time.sleep(2)
      print('Progress saved! ' + str(count) + ' submissions!')
      

# def print_content():
#   with open(BASE_DIR + '/' + '1192C', 'r') as f:
#     sources = json.loads(f.read())
#     print(sources['58163928']['code'])


def main():
  new_directory = BASE_DIR
  if not os.path.exists(new_directory):
      os.makedirs(new_directory)
      
  save_contest(1191)


if __name__ == "__main__":
  main()
