# Autonomous Agent

## Run sample implementation
- The sample consists of the configuration of agents as described in the problem statement.
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
