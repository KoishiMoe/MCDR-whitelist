Whitelist plugin for MCDR
-----

A mcdr plugin that provides whitelist operation permissions for non-admin players, with operation records.

On a Minecraft server with whitelisting enabled, if players can be trusted, this plugin can be used to allow them to manipulate the whitelist without giving them administrative rights. Also, the plugin supports reason logging, so you can ask your players to provide reasons for whitelisting.

## Config
```json
{
  "add_permission_level": 1,
  "remove_permission_level": 2,
  "query_permission_level": 2,
  "admin_permission_level": 4,
  "require_reason": true,
  "extra_deny": []
}
```

* `add_permission_level`: Minimum permission level required to add whitelist
* `remove_permission_level`: Minimum permission level required to remove whitelist
* `query_permission_level`: Minimum permission level required to query operation logs
* `admin_permission_level`: Minimum privilege level required to perform administrative operations such as clearing logs, setting allow and deny lists
* `require_reason`: Whether a reason is required for the operation
* `extra_deny`: Deny players on the list to perform actions, even if they have the required permission level

## Usage
### add
```plaintext
!!whitelist add [player] [reason]
```

### remove
```plaintext
!!whitelist remove [player] [reason]
```

### query
```plaintext
!!whitelist query              // Query all operation records
!!whitelist query -n [number]  // Query the latest n operation records, defaults to 10 if not specified.
!!whitelist query -s [player]  // Query the operation records of this player
!!whitelist query -t [player]  // Query the operation records targeting this player
```
Parameters can be combined with each other, for example:
```plaintext
!!whitelist query -n 10 -s demo -t demo2
```

### clear logs
```plaintext
!!whitelist clear
```

### extra deny
```plaintext
!!whitelist deny [player]  // Add the player to deny list.
!!whitelist allow [player]  // Remove the player from deny list. The player still needs sufficient permissions to operate the whitelist.
```
