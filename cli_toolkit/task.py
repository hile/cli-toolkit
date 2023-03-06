#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Asynchronous tasks for CLI scripts

This module implements script tasks to be executed asynchronously and
concurrently from script's run() method.
"""
import asyncio
import locale

from typing import Any, Awaitable, Dict, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .base import NestedCliCommand


class BaseScriptTask:
    """
    Common base class for script tasks

    :param parent: Parent script or command
    :type parent: Script, Command

    :param kwargs: Arguments passed to the task when run
    :type kwargs: dict
    """
    parent: 'NestedCliCommand'
    messages: List[str]
    errors: List[str]

    def __init__(self, parent: 'NestedCliCommand', **kwargs: Dict[Any, Any]) -> None:
        self.parent = parent
        self.messages = []
        self.errors = []
        parent.add_async_task(self.run, **kwargs)

    def error(self, *args: List[Any]) -> None:
        """
        Send subtask errors to parent
        """
        return self.parent.error(*args)

    def message(self, *args: List[Any]) -> None:
        """
        Send subtask messages to arent
        """
        return self.parent.message(*args)

    async def run(self, **kwargs: Dict[Any, Any]) -> None:
        """
        Run task. This must be implemented in child class
        """
        raise NotImplementedError('Task run() must be impelemented in child class')


class CommandLineTask(BaseScriptTask):
    """
    Shell command task linked to CLI script or command

    Runs a non-interactive shell command with specified arguments
    """
    command: Tuple[str]

    def __init__(self,
                 parent: 'NestedCliCommand',
                 command: Tuple[str],
                 **kwargs: Dict[Any, Any]) -> None:
        super().__init__(parent, **kwargs)
        self.command = command

    async def process_stderr(self, stderr: List[bytes]) -> None:
        """
        Method to process asynchronous messages to stderr from process
        """
        async for line in stderr:
            error = line.decode(locale.getpreferredencoding(False)).rstrip()
            self.errors.append(error)
            self.error(error)

    async def process_stdout(self, stdout: List[bytes]) -> None:
        """
        Method to process asynchronous messages to stdout from process
        """
        async for line in stdout:
            message = line.decode(locale.getpreferredencoding(False)).rstrip()
            self.messages.append(message)
            self.message(message)

    async def run(self, **kwargs: Dict[Any, Any]) -> Awaitable[None]:
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

    async def run(self, **kwargs: Dict[Any, Any]) -> None:
        """
        Run task. This must be implemented in child class
        """
        raise NotImplementedError('Task run() must be impelemented in child class')
