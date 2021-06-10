- [ ] Create some test cases for usages
  - [ ] Test configuration file


---

- `run` when container is not built, or else, it's stopped so `restart`
- config to `.ssh/config` given ip tables of servers
- `python setup.py develop` works, but `pip install -e .` doesn't work...
- found out after making all of the code that `gpus="all"` tag is not supported in `docker`. I found an alternative called `python-on-whales` which seems more promissing and easy to comprehend.
- multithreaded / parallel builds -> slow when build consequtively
