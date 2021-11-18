"""Tests for AutonomousAgent class."""
import asyncio
import unittest

from autonomous_agent import AutonomousAgent

# Using a helper var to store stdout instead of capturing stdout during runtime
# due to ease of implementation
test_stdout_helper_var = None

sample_outbox_msg = 'OUTBOX_MSG'

def handler(msg):
    if 'hello' in msg:
      global test_stdout_helper_var
      test_stdout_helper_var = msg
      return msg

async def behaviour(outbox):
    global sample_outbox_msg
    outbox.append(sample_outbox_msg)
    await asyncio.sleep(2)
 
async def put_msg_in_inbox(inbox, msg, loop):
    # Wait for 2 secs before/after to make sure the handler coroutines is running and executes
    await asyncio.sleep(2)
    inbox.append(msg)
    await asyncio.sleep(2)
    loop.stop()

class TestAutonomousAgent(unittest.TestCase):
    """TestCase subclass for testing AutonomousAgent."""

    def setUp(self):
        self.agent = AutonomousAgent()
        self.msg_handler = handler
        self.agent.register_msg_handler(str, handler)
        self.agent.register_behaviour(behaviour)
        global test_stdout_helper_var
        test_stdout_helper_var = None

    def tearDown(self):
        pass

    def test_msg_handler_correct_type(self):
        msg_to_put = 'hello world'
        loop = asyncio.get_event_loop()
        all_coroutines = [self.agent.run_handlers()] + [put_msg_in_inbox(inbox=self.agent.inbox, msg=msg_to_put, loop=loop)]
        all_groups = asyncio.gather(*all_coroutines)
        try:
          loop.run_until_complete(all_groups)
        except Exception as exc:
            pass
        global test_stdout_helper_var
        self.assertEqual(test_stdout_helper_var, msg_to_put)

    def test_msg_handler_incorrect_type(self):
        msg_to_put = 9999
        loop = asyncio.get_event_loop()
        all_coroutines = [self.agent.run_handlers()] + [put_msg_in_inbox(inbox=self.agent.inbox, msg=msg_to_put, loop=loop)]
        all_groups = asyncio.gather(*all_coroutines)
        try:
          loop.run_until_complete(all_groups)
        except Exception as exc:
            pass
        global test_stdout_helper_var
        self.assertIsNone(test_stdout_helper_var)

    def test_behaviour(self):
        loop = asyncio.get_event_loop()
        all_coroutines = self.agent.behaviours
        all_groups = asyncio.gather(*all_coroutines)
        loop.run_until_complete(all_groups)
        global sample_outbox_msg
        self.assertEqual(self.agent.outbox[0], sample_outbox_msg)
