# mirai_translate
pythonでみらい翻訳を行う

install
```
pip install git+https://github.com/riunanon/mirai_translate
```

use [example](https://github.com/riunanon/mirai_translate/blob/main/example.py)
```py
from mirai_translate import Client
Client.translate("text","en", "ja") #en => ja
Client.translate("テキスト","ja", "en") #ja => en
```
