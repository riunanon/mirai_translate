import re
from dataclasses import dataclass, field
from time import time
from typing import Optional
import httpx


class MiraiTranslateError(Exception):
    pass


@dataclass
class Client:
    delay_sec: Optional[int] = 6
    _cli: httpx.Client = field(
        default=httpx.Client(base_url="https://miraitranslate.com"),
        init=False,
    )
    # Key required to access `translate.php`
    _tran: Optional[str] = field(default=None, init=False)
    _prev_req_time: Optional[float] = field(default=None, init=False)

    def __post_init__(self):
        self._refresh_tran()
    def _refresh_tran(self):
        self._assure_deley()
        try:
            res = self._cli.get("/trial")
        except httpx.ReadTimeout:
            raise MiraiTranslateError("Response from Mirai Translate timed out")
        self._prev_req_time = time()
        self._tran = (
            re.search(rb'var tran = "(.+?)";', res.content).group(1).decode("utf-8")
        )

    def _translate(self, text: str, source: str, target: str) -> str:
        payload = dict(
            input=text,
            source=source,
            target=target,
            profile="inmt",
            filter_profile="nmt",
            tran=self._tran,
        )
        self._assure_deley()
        try:
            res = self._cli.post(
                "/trial/api/translate.php",
                json=payload,
            )
        except httpx.ReadTimeout:
            raise MiraiTranslateError("Response from Mirai Translate timed out")
        self._prev_req_time = time()
        j = res.json()

        status = j["status"]
        if status == "failed" or status == "limit":
            raise MiraiTranslateError(j["error_msg"])

        if status != "success":
            raise MiraiTranslateError(
                '"status" should be either "failed", "limit", '
                f'or "success" but got {status}'
            )

        return j["outputs"][0]["output"][0]["translation"]

    def translate(self, text: str, source: str, target: str) -> str:
        try:
            return self._translate(text, source, target)
        except MiraiTranslateError:
            self._refresh_tran()
            return self._translate(text, source, target)
