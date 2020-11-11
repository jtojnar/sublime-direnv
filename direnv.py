import sublime, sublime_plugin

import asyncio
import json
import os
import threading

def yes_no_dialog(message: str, yes_title: str, no_title: str):
    '''Like yes-no-cancel dialog but keep asking on cancel.'''
    result = sublime.yes_no_cancel_dialog(message, yes_title, no_title)
    if result == sublime.DIALOG_CANCEL:
        return yes_no_dialog(message, yes_title, no_title)

    return result

class DirenvLoad(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window()
        directory = window.folders()[0]

        thread = threading.Thread(target=lambda: asyncio.run(self.__direnv(directory)))
        thread.start()

    async def __check_timeout(self, proc):
        try:
            return await asyncio.wait_for(asyncio.shield(proc.wait()), 10.0)
        except asyncio.exceptions.TimeoutError:
            termination = yes_no_dialog('direnv is taking too long. Do you wish to wait?', '_Terminate', 'Keep _waiting')
            if termination == sublime.DIALOG_YES:
                print('Terminating direnv…')
                proc.terminate()
            elif termination == sublime.DIALOG_NO:
                return await self.__check_timeout(proc)

    async def __direnv(self, directory):
        os.environ['DIRENV_DEBUG'] = '1'
        proc = await asyncio.create_subprocess_exec(
            *'direnv export json'.split(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=os.environ,
            cwd=directory
        )

        sublime.status_message('Waiting for direnv…')

        await self.__check_timeout(proc)

        outs, errs = await proc.communicate()

        if outs and proc.returncode == 0:
            print(outs.decode('utf-8'))
            variables = json.loads(outs.decode('utf-8'))
            for name, value in variables.items():
                if value is None:
                    del os.environ[name]
                else:
                    os.environ[name] = value
            sublime.status_message('Environment updated.')
        else:
            print(errs.decode('utf-8'))
            sublime.status_message('Failed to update environment.')
