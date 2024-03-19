from __future__ import annotations

import typing as _t

from fastui import components as c

ModalType = tuple[c.Button, c.Modal]
AlertType = _t.Literal['ERROR', 'WARNING', 'NOTIFICATION', 'INFO']


AlertDict = dict[str, AlertType]
