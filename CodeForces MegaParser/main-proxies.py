import urllib.request, urllib.parse
import json, threading
import os, time, datetime
from itertools import cycle

from submission_getter import submission_code
from proxies import get_proxies, get_proxies_manually

MAX_PROBLEM_SUBS = 1000 * 1000 * 10
MAX_THREADS = 5
NUM_PROXIES = 50
BASE_DIR = 'Surse'
URL_CONTEST_SUBMISSION = 'http://codeforces.com/api/contest.status?contestId={contestId}'

thread_count = 0
proxy_pool = cycle(get_proxies(NUM_PROXIES))

def submissions_from_contest(contestId):
  url = URL_CONTEST_SUBMISSION.format(contestId=contestId)
  # url = urllib.parse.quote(url)
  submissions = json.loads(urllib.request.urlopen(url).read())
  return submissions['result']

def save_progress(sources, contestId):
  for prob_id, data in sources.items():
    file_obj = open(BASE_DIR + '/' + str(contestId) + prob_id + '.txt', 'w')
    json.dump(data, file_obj, indent = 2)

def save_contest(contestId):
  global proxy_pool
  global thread_count, MAX_PROBLEM_SUBS, BASE_DIR, URL_CONTEST_SUBMISSION

  print('Thread ' + str(contestId) + ' started')
  thread_start_time = time.time()

  submissions = submissions_from_contest(contestId)
  print( 'Contest: ' + str(contestId) + ' has ' + str(len(submissions)) + ' submissions' )

  sources, count, subs_checked = {}, 0, 0
  submissions = sorted(submissions, key = lambda k: k['id'])
  using_proxy = next(proxy_pool)
  for sub in submissions:
    subs_checked = subs_checked + 1

    if sub['verdict'] != 'OK':
      continue

    count = count + 1
    if count > MAX_PROBLEM_SUBS:
      print('Thread ' + str(contestId) + ' reached maximum problem submissions')
      break
    
    percentage = subs_checked / len(submissions) * 100

    prob_id = sub['problem']['index']
    sub_id = str(sub['id'])
    if prob_id not in sources.keys():
      sources[ prob_id ] = {}
    
    code, ext = 'nothing', 'no-ext'

    while True:
      try:
        code, ext = submission_code(sub, using_proxy)
        break
      except Exception as e:
        print('Thread ' + str(contestId) + ' has Exception, waiting')
        print(e)
        time.sleep(4)
        using_proxy = next(proxy_pool)
    
    sources[ prob_id ][ sub_id ] = {
      'code': code,
      'ext': ext
    }

    if count % 10 == 0:
      save_progress(sources, contestId)
      print("\nSaved contest {}: {}/{}  {:.2f}%  saved: {}  time: "\
        .format(contestId, subs_checked, len(submissions), percentage, count) + \
        time.strftime("%H:%M:%S", time.gmtime(time.time() - thread_start_time)) + "\n")

    if count % 500 == 0:
      proxy_pool = cycle(get_proxies(NUM_PROXIES))

  thread_count = thread_count - 1
  print('Thread ' + str(contestId) + ' finished')

def thread_version():
  global thread_count
      
  contest_list = [i + 1 for i in range(1191)]
  
  thread_count = 0
  t_list = []
  while len(contest_list) > 0:
    print('thread count: ' + str(thread_count))

    if thread_count < MAX_THREADS:
      thread_count = thread_count + 1
      th = threading.Thread(target=save_contest, args=(contest_list[-1],))
      t_list.append(th)
      contest_list = contest_list[:-1]
      th.start()
    else:
      for th in t_list:
        th.join()

    time.sleep(1)
  
  print('All work finished! WOW')

def simple_version():
  print('type contestID:')
  contestID = int(input())
  save_contest(contestID)



def main():
  new_directory = BASE_DIR
  if not os.path.exists(new_directory):
      os.makedirs(new_directory)
      
  simple_version()


if __name__ == "__main__":
  main()
