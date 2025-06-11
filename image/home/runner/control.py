#!/usr/bin/python3
import os
from pprint import pprint
import re
import requests
import signal
import subprocess
import time

ConfigMap = {
  'group': 'GITHUB_RUNNER_GROUP',
  'labels': 'GITHUB_RUNNER_LABELS',
  'name': 'GITHUB_RUNNER_NAME',
  'org': 'GITHUB_ORGANIZATION',
  'token': 'GITHUB_ACCESS_TOKEN'
}
GitHubApiVersion = "2022-11-28"

def Log(message):
  print("[CONTROL "+time.strftime('%Y-%m-%d %XZ')+"]", message)

if os.path.exists("/home/runner/.stop"):
  os.remove("/home/runner/.stop")
def StopHandler(sig, frame):
  with open("/home/runner/.stop", "w") as file:
    file.write(str(sig))
signal.signal(signal.SIGINT, StopHandler)
signal.signal(signal.SIGTERM, StopHandler)

class Config():
  def __init__(self):
    os.environ['TZ'] = 'UTC'
    time.tzset()
    errors = 0
    for key in ConfigMap:
      setattr(self, key, "")
      try:
        value = re.sub(r"\s+", "", os.environ[ConfigMap[key]])
      except:
        value = ""
      if value != "":
        setattr(self, key, value)
        continue
      try:
        file = os.environ[ConfigMap[key]+"_FILE"]
      except:
        file = ""
      if file == "":
        if key != 'group' and key != 'labels':
          print("Failed to read '"+key+"' from environment variable", ConfigMap[key])
          errors += 1
        continue
      try:
        with open(file) as f:
          value = re.sub(r"\s+", "", f.read())
      except:
        value = ""
      if value != "":
        setattr(self, key, value)
        continue
      print("Failed to read '"+key+"' from ", file)
      errors += 1
    if errors > 0:
      exit(1)
    for key in ConfigMap:
      value = getattr(self, key)
      if key == 'token':
        value = "********"
      Log("Config:"+key+" = "+str(value))
class Control():
  def __init__(self):
    Log("Import the configuration")
    self.config = Config()
    if os.path.exists("/home/runner/.stop"): exit(1)

    Log("Remove our local runner configuration")
    self.removeRunner()
    if os.path.exists("/home/runner/.stop"): exit(1)

    Log("Connect to GitHub/"+self.config.org)
    self.github = GitHub(self.config)
    if os.path.exists("/home/runner/.stop"): exit(1)

    Log("Remove our old runner registration")
    self.github.deleteRunner()
    if os.path.exists("/home/runner/.stop"): exit(1)

    Log("Get a new runner registration token")
    token = self.github.runnerToken()
    if os.path.exists("/home/runner/.stop"): exit(1)

    Log("Configure our local runner process")
    self.configureRunner(token)
    if os.path.exists("/home/runner/.stop"): exit(1)

    Log("Start our local runner process")
    process = self.startRunner()
    Log("Start monitoring our GitHub runner")
    self.stoptimer = 0
    while process.poll() == None:
      self.monitorRunner(process)
    exit(process.returncode)
  def configureRunner(self, token):
    cmd = [ "/home/runner/config.sh",
            "--unattended", 
            "--url","https://github.com/"+self.config.org,
            "--token",token,
            "--name",self.config.name,
            "--replace" ]
    if self.config.group != "":
      cmd.extend(["--runnergroup",self.config.group])
    if self.config.labels != "":
      cmd.extend(["--labels",self.config.labels])
    rc = subprocess.run(cmd, capture_output=True, text=True)
    if rc.returncode > 0:
      print(rc.stdout+"\n"+rc.stderr)
      exit(1)
  def monitorRunner(self, process):
    for t in range(42):
      if os.path.exists("/home/runner/.stop"):
        self.stopRunner(process)
      time.sleep(1)
      if process.poll() != None:
        return
    status = self.github.runnerStatus()
    Log("GitHub runner status: "+status)
    if status != "online":
      self.stopRunner(process)
  def removeRunner(self):
    if os.path.exists("/home/runner/.credentials"):
      os.remove("/home/runner/.credentials")
    cmd = ["/home/runner/config.sh","remove"]
    rc = subprocess.run(cmd, capture_output=False, text=True)
    if rc.returncode > 0:
      exit(1)
  def startRunner(self):
    cmd = ["/home/runner/run.sh"]
    process = subprocess.Popen(cmd)
    return process
  def stopRunner(self, process):
    Log("Stop our local runner process")
    process.terminate()
    if self.stoptimer == 0:
      self.stoptimer = time.time()
      return
    timer = time.time() - self.stoptimer
    if timer > 10:
      Log("Kill our local runner process")
      process.kill()

class GitHub():
  def __init__(self, config):
    self.api = "https://api.github.com"
    self.org = config.org
    self.name = config.name
    self.session = requests.Session()
    self.session.headers.update({
      'Accept': 'application/vnd.github+json',
      'Authorization': 'Bearer '+config.token,
      'X-GitHub-Api-Version': GitHubApiVersion
    })
  def error (self, method, path, response):
    Log(method+" "+self.api+path+" returned "+str(response.status_code)+" "+response.reason)
    try:
      pprint(response.json())
    except:
      pass
    exit(1)
  def failed(self, method, path, e):
    Log(method+" "+self.api+path+" failed")
    print(e)
    exit(1)
  def deleteRunner(self):
    runner = self.getRunner()
    try: 
      id = runner["id"]
    except:
      return False
    path = "/orgs/"+self.org+"/actions/runners/"+str(id)
    try:
      response = self.session.delete(self.api+path)
    except Exception as e:
      self.failed("DELETE", path, e)
    if response.status_code != 204:
      self.error("DELETE", path, response)
    return True
  def getRunner(self):
    path = "/orgs/"+self.org+"/actions/runners?per_page=100"
    try:
      response = self.session.get(self.api+path)
    except Exception as e:
      self.failed("GET", path, e)
    if response.status_code != 200:
      self.error("GET", path, response)
    data = response.json()
    for runner in data["runners"]:
      if runner["name"].lower() == self.name.lower():
        return runner
    return None
  def runnerStatus(self):
    runner = self.getRunner()
    try:
      return runner["status"]
    except:
      return ""
  def runnerToken(self):
    path = "/orgs/"+self.org+"/actions/runners/registration-token"
    try:
      response = self.session.post(self.api+path)
    except Exception as e:
      self.failed("POST", path, e)
    if response.status_code != 201:
      self.error("POST", path, response)
    data = response.json()
    return data["token"]

Control()