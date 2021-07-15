# JAO-messageboard-parser

Simple library to parse messages of the JAO messageboards at https://jao.eu/

## Installation
Simply copy the JAOparser.py into your project and import it.

## Usage
Messages can either be retrieved by specifying which pages you want or filtered by a date range.
If you want the latest messages then retrieve page 0-x with x being the number of pages you want to fetch. There are 10 messages per page.

You can choose between groups "tso", "jao" or "all". This corresponds to the website interface.

Date example:
```python
from JAOparser import JAO_get_messages_from_dates
from datetime import datetime

messages = JAO_get_messages_from_dates(d_from=datetime(year=2021, month=7, day=1), d_to=datetime(year=2021, month=7, day=31), group='tso') 
```

Page example:
```python
from JAOparser import JAO_get_messages_from_pages
from datetime import datetime

messages = JAO_get_messages_from_pages(p_from=0, p_to=10, group='tso')
```

Please be considerate to JAO and do not retrieve huge volumes of messages shortly after eachother. There is no rate limiting or caching support in this library.

## Company proxy usage
Since this library uses the requests library for fetching you can setup proxy usage the same as normal requests:
```python
import os

os.environ['HTTP_PROXY'] = "http:\\<username>:<password>@<proxy_url>:<proxy_port>"
os.environ['HTTPS_PROXY'] = "https:\\<username>:<password>@<proxy_url>:<proxy_port>"
```

## Support
If you have questions about the library either open an issue on the github repo FrankBoermanTenneT/JAO-messageboard-parser or send an email to frank.boerman@tennet.eu 