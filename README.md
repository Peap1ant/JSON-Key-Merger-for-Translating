# JSON Key Merger for Translating

This is Python script for merge key from JSON into another JSON file.

## Why You need to use this?

To update Translating, you need to merge both JSOM manually for updating.

But with this, it can add key from new version of lang file into old version for "no-more-use-brain"!

## What it does

It needs 2 JSON(Original JSON and Target JSON) to work.

Original JSON is newer version of lang file, and Target JSON is old version of lang file, which contains translations.

By select JSON and press button at GUI, It gonna make new JSON contains translations + new keys from Original JSON which Target JSON haven't.

Also there is chect box for delete missing key(unused key) at Target file for better JSON, check if you want

here is example:

Original JSON

```json
{
    "key": "value",
    "new_key": "new_value"
}
```

Target JSON

```json
{
    "key": "value"
}
```

Merged JSON

```json
{
    "key": "value",
    "new_key": ""
}
```

## How can I use it?

1. Clone repository or download as zip file
2. Install Python 3.7+
3. Open gui as bash

```bash
python merge_tool.py
```