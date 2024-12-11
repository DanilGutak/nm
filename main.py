import cmd
import os
import signal
import subprocess
import yaml
import argparse
from pathlib import Path


class TaskmasterShell(cmd.Cmd):
    completekey = "tab"
    intro = "Welcome to Taskmaster Shell\n"
    prompt = "taskmaster> "

    def load_config(self, config):
        with open(config, "r") as file:
            return yaml.safe_load(file)
    
    def __init__(self, config):
        super().__init__()
        self.config = self.load_config(config)
        self.programs = self.config["programs"]
        self.processes = {}
        print(self.config)
        print(self.programs)    

    def do_start(self, arg):
        if not arg:
            print("Please provide a process to start")
            return
        if arg not in self.programs:
            print(f"Process {arg} not found in config")
            return
        if arg in self.processes:
            print(f"Process {arg} is already running")
            return
        process = self.programs[arg]
        command = process["cmd"]
        process = subprocess.Popen(command, shell=True)
        print(f"command: {command}")
        self.processes[arg] = process
        print(f"Process {arg} started")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="config.yaml", help="Path to the config file")
    args = args.parse_args()
    shell = TaskmasterShell(args.config)
    shell.cmdloop()
