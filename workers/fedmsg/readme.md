# fedora-messaging worker

This worker pulls events from the fedora-messaging queue in fedora land. Fedora-messaging replaced fedmsg as the single queue with all events on it.

# Development

1. Install reqs

```
pip install requirements.txt
```

2. Edit config.toml and set your queue name to something unique (lines 36 and 43)

3. Run worker

```
fedora-messaging --conf config.toml consume --callback-file=save.py:SaveMessage
```

4. Add new handlers for events

See TODOs in `save.py`
