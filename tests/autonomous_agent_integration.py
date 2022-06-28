"""Tests for AutonomousAgent class."""
import asyncio
import unittest

from autonomous_agent import AutonomousAgent

# Using a helper var to store stdout instead of capturing stdout during runtime
# due to ease of implementation
test_stdout_helper_var = None

sample_outbox_msg = 'hello world'
sample_stdout_msg = 'hello world stdout'

def handler(msg):
    if 'hello' in msg:
      global test_stdout_helper_var
      global sample_stdout_msg
      test_stdout_helper_var = sample_stdout_msg
      return msg

async def behaviour(outbox):
    global sample_outbox_msg
    outbox.append(sample_outbox_msg)
    await asyncio.sleep(1)
 
async def stop_loop(loop):
    # Waiting for 4 seconds to make sure all coroutines finishes
    await asyncio.sleep(4)
    loop.stop()


class TestAutonomousAgent(unittest.TestCase):
    """TestCase subclass for testing AutonomousAgent."""

    def setUp(self):
        self.first_agent = AutonomousAgent()
        self.msg_handler = handler
        self.first_agent.register_msg_handler(str, handler)

        self.second_agent = AutonomousAgent()
        self.second_agent.register_behaviour(behaviour)

        # First agent consumes msgs produced by second agent
        self.first_agent.inbox = self.second_agent.outbox

        global test_stdout_helper_var
        test_stdout_helper_var = None

    def tearDown(self):
        pass

    def test_cascade_of_agents(self):
        loop = asyncio.get_event_loop()
        all_coroutines = [self.first_agent.run_handlers()] + [stop_loop(loop=loop)] + self.second_agent.behaviours
        all_groups = asyncio.gather(*all_coroutines)
        try:
          loop.run_until_complete(all_groups)
        except Exception as exc:
            pass
        global test_stdout_helper_var
        global sample_stdout_msg
        self.assertEqual(test_stdout_helper_var, sample_stdout_msg)
