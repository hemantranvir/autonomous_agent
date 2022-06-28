"""AutonomousAgent class to run custom async handlers/behaviours with
messaging queue."""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO)


class AutonomousAgent:
    """AutonomousAgent class."""

    def __init__(self):
        """Instantiate the class."""
        self.inbox = []
        self.outbox = []
        self.msg_handlers = []
        self.behaviours = []

    def get_coroutines_group(self):
        """Get the asyncio gather group of coroutines."""
        coroutines = self.behaviours + [instance1.run_handlers()]
        return asyncio.gather(*coroutines)

    def register_msg_handler(self, message_type, handler):
        """Append given tuple of message type and message handler."""
        self.msg_handlers.append((message_type, handler))

    def register_behaviour(self, behaviour):
        """Append behaviours."""
        self.behaviours.append(behaviour(self.outbox))

    async def run_handlers(self):
        """Run message handlers for a specific message type.
        Please Note: asyncio sleep of 500ms is awaited for since this
        seems to be reasonable time to resume the handling loop and check
        for new messages.
        """
        while True:
            try:
                msg = self.inbox.pop()
                if msg is not None:
                    for message_type, handler in self.msg_handlers:
                        if isinstance(msg, message_type):
                            handler(msg)
            except Exception as exc:
                logging.debug("Exception caught in run handlers: ", exc)
                pass
            await asyncio.sleep(0.5)


if __name__ == '__main__':
    def handler(msg):
        if 'hello' in msg:
            print(msg)
        return

    async def behaviour(outbox):
        words = ["hello", "sun", "world", "space", "moon", "crypto", "sky",
                 "ocean", "universe", "human"]
        while True:
            first_word = random.choice(words)
            second_word = random.choice(words)
            outbox.append(f'{first_word} {second_word}')
            await asyncio.sleep(2)

    instance1 = AutonomousAgent()
    instance1.register_msg_handler(str, handler)
    instance1.register_behaviour(behaviour)

    instance2 = AutonomousAgent()
    instance2.register_msg_handler(str, handler)
    instance2.register_behaviour(behaviour)

    instance1.inbox = instance2.outbox
    instance2.inbox = instance1.outbox

    group1 = instance1.get_coroutines_group()
    group2 = instance2.get_coroutines_group()

    all_groups = asyncio.gather(group1, group2)

    loop = asyncio.get_event_loop()
    logging.info('Starting event loop..')
    loop.run_until_complete(all_groups)
