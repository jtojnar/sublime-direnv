import sublime, sublime_plugin
from os import environ
import os.path

class DirenvAllow(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window()
        folder = window.folders()[0]
        envrc_file = folder + "/.envrc"
        try:
            open_envrc = open(envrc_file)
            read_envrc = open_envrc.readlines()
        except:
            sublime.status_message("Not .envrc file")

        if os.path.exists(envrc_file):

            for envrc in read_envrc:
                replace_export = envrc.replace('export ', '')
                replace_lf = replace_export.replace('\r\n','')
                environment = replace_lf.split("=")
                environ[environment[0]] = environment[1]

            sublime.status_message("Find .envrc file.")
