# Getting Started
The FASTEST way to Indicator!

# Examples
## Shell
```bash
$ pip install csirtg-indicator
$ csirtg-indicator --group everyone --indicator http://example.com/1.htm --tlp green --tags phishing

{
    "indicator": "http://example.com/1.htm",
    "itype": "url",
    "tlp": "green",
    "count": 1,
    "tags": ["phishing"],
    "uuid": "42842ea0-03d9-4d38-a0ae-b705788e862b"
}
```

## Python
```python
from csirtg_indicator import Indicator
i = Indicator('example.com')

print(i)
```

