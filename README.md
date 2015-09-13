flussonic python api
--------------------

```bash
git clone https://github.com/gonzafirewall/flusspy
cd flusspy
pip install -r reqs.txt
`````

```python
from flusspy import Flussonic

f = Flussonic("http://dvr.compapy.com/flussonic/api/", auth=("secret", "ultr4s3cr3t"))
print f.get_config()
`````
