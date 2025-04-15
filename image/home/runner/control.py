#!/usr/bin/python3
import os
from pprint import pprint
import re
import requests
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

class Config():
  def __init__(self):
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
      print("[CONTROL] Config:"+key,"=", value)
class Control():
  def __init__(self):
    print("[CONTROL] Import the configuration")
    self.config = Config()
    print("[CONTROL] Remove our local runner configuration")
    self.removeRunner()
    print("[CONTROL] Connect to GitHub/"+self.config.org)
    self.github = GitHub(self.config)
    print("[CONTROL] Remove our old runner registration")
    self.github.deleteRunner()
    print("[CONTROL] Get a new runner registration token")
    token = self.github.runnerToken()
    print("[CONTROL] Configure our local runner process")
    self.configureRunner(token)
    print("[CONTROL] Start our local runner process")
    process = self.startRunner()
    print("[CONTROL] Start monitoring our GitHub runner")
    while process.poll() == None:
      self.monitorRunner(process)
    exit(process.returncode)
  def configureRunner(self, token):
    cmd = ["/home/runner/config.sh","--unattended", "--url","https://github.com/"+self.config.org,"--token",token,"--name",self.config.name]
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
      time.sleep(1)
      if process.poll() != None:
        exit(process.returncode)
    status = self.github.runnerStatus()
    print("[CONTROL] GitHub runner status:", status)
    if status != "online":
      process.terminate()
  def removeRunner(self):
    cmd = ["/home/runner/config.sh","remove"]
    rc = subprocess.run(cmd, capture_output=True, text=True)
    if rc.returncode > 0:
      print(rc.stdout+"\n"+rc.stderr)
      exit(1)
  def startRunner(self):
    cmd = ["/home/runner/run.sh"]
    process = subprocess.Popen(cmd)
    return process
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
    print("[CONTROL]",method, self.api+path, "returned", response.status_code, response.reason)
    try:
      pprint(response.json())
    except:
      pass
    exit(1)
  def failed(self, method, path, e):
    print("[CONTROL]",method, self.api+path, "failed")
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