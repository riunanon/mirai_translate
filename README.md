# mirai_translate
pythonでみらい翻訳を行う

install
```
pip install git+https://github.com/riunanon/mirai_translate
```

use [example](https://github.com/riunanon/mirai_translate/blob/main/example.py)
```py
from mirai_translate import mirai
mirai.translate("text","en", "ja") #en => ja
mirai.translate("テキスト","ja", "en") #ja => en
```
