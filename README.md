# BackdoorHive

With this project Im planning to create:

- A Windows backdoor
- C2 server 
- Webapp for payload generation, bots visualisation and other features.


Supported commands:

## C2 commands:
| Command    | Functionnality    | Implemented    |
|-------------|-------------|-------------|
| sessions | display active clients | ✅ |
| session "id" | interact with specific session | ✅ |
| background | background the current active session | ✅ |
| exit | exit C2 server | ✅ |

## Session commands:
| Command              | Functionnality                        | Implemented   |
|----------------------|---------------------------------------|------------|
| check                | check user's privileges               | ✅ |
| check_edr            | check EDRs used in host               | 🔄 |
| wget                 | download file from a URL              | ✅ |
| download             | download file from client -> server   | ✅ |
| upload               | upload file from server -> client     | ✅ |
| keylogger start/stop | start/stop capturing keystrokes       | 🔄 |
| screenshot           | take a real-time screenshot on client | ✅ |
| kill_client          | Close connection with specific client | ✅ |
| help                 | display custom supported commands     | ✅ |