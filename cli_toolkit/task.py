"""
Asynchronous tasks for CLI scripts

This module implements script tasks to be executed asynchronously and
concurrently from script's run() method.
"""

import asyncio
import locale


class BaseScriptTask:
    """
    Common base class for script tasks

    :param parent: Parent script or command
    :type parent: Script, Command

    :param kwargs: Arguments passed to the task when run
    :type kwargs: dict
    """
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.messages = []
        self.errors = []
        parent.add_async_task_callback(self.run, **kwargs)

    def error(self, *args):
        """
        Send subtask errors to parent
        """
        return self.parent.error(*args)

    def message(self, *args):
        """
        Send subtask messages to arent
        """
        return self.parent.message(*args)

    async def run(self, **kwargs):
        """
        Run task. This must be implemented in child class
        """
        raise NotImplementedError('Task run() must be impelemented in child class')


class CommandLineTask(BaseScriptTask):
    """
    Shell command task linked to CLI script or command

    Runs a non-interactive shell command with specified arguments
    """
    def __init__(self, parent, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command

    async def process_stderr(self, stderr):
        """
        Method to process asynchronous messages to stderr from process
        """
        async for line in stderr:
            error = line.decode(locale.getpreferredencoding(False)).rstrip()
            self.errors.append(error)
            self.error(error)

    async def process_stdout(self, stdout):
        """
        Method to process asynchronous messages to stdout from process
        """
        async for line in stdout:
            message = line.decode(locale.getpreferredencoding(False)).rstrip()
            self.messages.append(message)
            self.message(message)

    async def run(self, **kwargs):
        """
        Run specified shell command with asyncio
        """
        process = await asyncio.create_subprocess_exec(
            *self.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await self.process_stdout(process.stdout)
        await self.process_stderr(process.stderr)
        return await process.wait()


class Task(BaseScriptTask):
    """
    Script python task linked to CLI script or command

    This class must be inherited to child class that implements run() method.
    """

    async def run(self, **kwargs):
        """
        Run task. This must be implemented in child class
        """
        raise NotImplementedError('Task run() must be impelemented in child class')
