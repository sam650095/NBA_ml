# Fixed the output place

1. Press "Cmd + Shift + P "
2. Type "Python: Select Linter"
3. Pick "pylint" - Python linter"

# Apperence

1. Press "Cmd + Shift + P" again and type "Preferences: Open Settings (JSON)"
2. Type this into settings.json
   jsonCopy code"python.linting.pylintArgs": [
   "--disable=all",
   "--enable=W0611"
   ],
   "python.terminal.activateEnvironment": true
