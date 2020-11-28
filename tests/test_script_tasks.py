
import asyncio
import os
import signal
import sys

import pytest

from cli_toolkit.script import Script
from cli_toolkit.task import Task, CommandLineTask


# pylint: disable=too-few-public-methods
class MockCalledMethod:
    """
    Mock a called method
    """
    def __init__(self):
        self.call_count = 0
        self.args = None
        self.kwargs = None

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.args = args
        self.kwargs = kwargs


# pylint: disable=too-few-public-methods
class MockSigInt(MockCalledMethod):
    """
    Mock SIGINT handler
    """
    def __call__(self, *args, **kwargs):
        print('MOCK SIGINT', *args, **kwargs)
        super().__call__(*args, **kwargs)
        sys.exit(1)


class MessageTask(Task):
    """
    Test task waiting for some time
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.message = None

    async def run(self, **kwargs):
        """
        Run test task
        """
        sleep_time = kwargs.get('sleep', None)
        if sleep_time:
            await asyncio.sleep(sleep_time)
        self.message = kwargs.get('message', None)


class FailTask(Task):
    """
    Failing test task
    """
    async def run(self, **kwargs):
        """
        Run test task
        """
        raise ValueError('Failure is an option')


class SleepyTask(Task):
    """
    Run task that waits and is cancelled
    """
    async def run(self, **kwargs):
        """
        Run test task
        """
        print(f'sleep in task {os.getpid()}')
        await asyncio.sleep(10)


class CancelTask(Task):
    """
    Run task that sends SIGINT to script and is cancelled
    """
    async def run(self, **kwargs):
        """
        Run test task
        """
        pid = kwargs['pid']
        await asyncio.sleep(0.5)
        print(f'kill pid {pid} with SIGINT')
        os.kill(pid, signal.SIGINT)


def test_script_tasks_cli_ls(monkeypatch):
    """
    Test running trivial command from script CLI task
    """
    script = Script()
    CommandLineTask(script, ('ls', '/'))
    mock_method = MockCalledMethod()
    monkeypatch.setattr(script, 'message', mock_method)
    with pytest.raises(SystemExit) as exit_status:
        script.run()
    assert exit_status.value.code == 0
    assert mock_method.call_count > 1


def test_script_tasks_cli_ls_errors(monkeypatch):
    """
    Test running trivial command with error from script CLI task
    """
    script = Script()
    CommandLineTask(script, ('ls', '/B098D090-BC2A-4ADF-B8EB-35984FE035FF'))
    mock_method = MockCalledMethod()
    monkeypatch.setattr(script, 'error', mock_method)
    with pytest.raises(SystemExit) as exit_status:
        script.run()
    assert exit_status.value.code == 0
    assert mock_method.call_count == 1


def test_script_tasks_cli_multiple_tasks(monkeypatch):
    """
    Test running multiple commands from script CLI task
    """
    script = Script()
    CommandLineTask(script, ('ls', '/usr'))
    CommandLineTask(script, ('ls', '/usr'))
    CommandLineTask(script, ('find', '/tmp'))
    mock_method = MockCalledMethod()
    monkeypatch.setattr(script, 'message', mock_method)
    with pytest.raises(SystemExit) as exit_status:
        script.run()
    assert exit_status.value.code == 0
    assert mock_method.call_count > 1


def test_script_tasks_with_failing_task():
    """
    Test script with a task that raises ValueError exception
    """
    script = Script()
    FailTask(script)
    with pytest.raises(ValueError):
        script.run()


def test_script_tasks_with_wait_task_cancelled(monkeypatch):
    """
    Test script with a task that raises ValueError exception
    """
    mock_sigint = MockSigInt()
    monkeypatch.setattr('cli_toolkit.script.Script.SIGINT', mock_sigint)

    script = Script()
    CancelTask(script, pid=os.getpid())
    SleepyTask(script)
    with pytest.raises(SystemExit) as exit_code:
        script.run()

    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1
    assert mock_sigint.call_count == 1


def test_script_tasks_with_multiple_tasks():
    """
    Test script with two instances calling same Task object
    """
    script = Script()

    kwargs = {
        'sleep': 1,
        'message': 'Test message'
    }
    dummy = MessageTask(script)
    task = MessageTask(script, **kwargs)
    assert task.message is None

    with pytest.raises(SystemExit) as exit_status:
        script.run()
    assert exit_status.value.code == 0

    assert dummy.message is None
    assert isinstance(task.message, str)
    assert task.message == kwargs['message']
