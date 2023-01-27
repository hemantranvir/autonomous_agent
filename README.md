# Autonomous Agent

## Introduction
Autonomous agents have a number of defining characteristics:
- Communicate with the environment via asynchronous messages
- Display reactiveness (handling messages) and proactiveness (generating new
messages based on internal state or local time)
- Can be thought of as representing a human, organisation, or thing in a specific domain
and tasks

The autonomous agent should support these operations and characteristics:
- Continuously consume messages (of different types) from an InBox
- Emit messages to an OutBox
- Allow for registration of message handlers to handle a given message type with its
specific handler (reactive: if this message then that is done)
- Allow for registration of behaviours (proactive: if this internal state or local time is
reached then this message is created)

Once the generic autonomous agent is in place, we will create a concrete instance which:
- Has one handler that filters messages for the keyword “hello” and prints the whole
message to stdout
- Has one behaviour that generates random 2-word messages from an alphabet of 10
words (“hello”, “sun”, “world”, “space”, “moon”, “crypto”, “sky”, “ocean”, “universe”,
“human”) every 2 seconds

## Run sample implementation
- The sample consists of the configuration of agents as described above
```
$ make run-sample
```

## Run tests
```
$ make run-test
```

## Run flake8
- Please activate virtual env before running flake8 since external library is required
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ make run-flake8
```

## Few notes
- Asyncio is used since the agent is bound by I/O (waiting for message queues/sleep interval)
  Did not use multiprocessing to keep it simple and sharing data between processes
  could get trickier (process lock/unlock etc.). Though I think a combination of
  asyncio and multiprocessing could be better for performance.
- In testing, fastest approach is taken to test the functionalities so the code 
  is a bit less general. For e.g. capturing stdout is omitted in tests instead a
  gloabal variable is used to save messages
- The inbox message checking can be improved. Currently the loop waits for 500ms
  before resuming to check for new messages. Ideally event emitters/listeners would be more suitable in this case.
  Also, after the loop resumes we check the messages and call handlers sequentially. The message checking & calling handlers can be separate async functions to improve speed up.
- The AutonomousAgent class interface can be improved and be made more uniform.
  Currently, the class requires handler to be a non-async function and behaviour to be async function. We can make it uniform or allow both async/non-async function registrations.
- Only one external library (flake8 is used) for linting
