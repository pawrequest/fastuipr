from __future__ import annotations

from typing import Sequence, Union

from fastui import components as c, events
from fastui.events import GoToEvent
from loguru import logger

from DecodeTheBot.dtg_bot import DB_MODELS
from DecodeTheBot.ui.dtg_styles import HEAD, SUB_LIST, TITLE_COL, PLAY_COL
from fastuipr import builders, styles
from suppawt import get_set, convert


def get_headers(header_names: list) -> c.Div:
    headers = [c.Div(components=[c.Text(text=_)], class_name=HEAD) for _ in header_names]
    return c.Div(components=[headers], class_name=HEAD)


def objects_ui_with(objects: Sequence) -> c.Div:
    try:
        headers_and_rows = [_object_ui_with_related(_) for _ in objects]

        head_names = [_[0] for _ in headers_and_rows[0]]
        head_names = [get_set.title_from_snake(_) for _ in head_names]
        headers = get_headers(head_names)

        rows = [
            [_[1] for _ in row_obj]
            for row_obj in headers_and_rows
        ]

        return builders.wrap_divs(
            components=[
                headers,
                *rows,
            ],
            class_name=SUB_LIST,
        )
    except Exception as e:
        logger.error(e)


def objects_col(objects: Sequence) -> c.Div:
    try:
        if not objects:
            return builders.empty_div(class_name=styles.COL_STYLE)
        return builders.wrap_divs(
            components=[object_col_one(_) for _ in objects],
            class_name=styles.COL_STYLE,
            inner_class_name=styles.ROW_STYLE,
        )
    except Exception as e:
        logger.error(e)


def object_col_one(obj) -> Union[c.Div, c.Link]:
    if not obj:
        return builders.empty_div(class_name=styles.COL_STYLE)
    return builders.wrap_divs(
        components=[
            c.Link(
                components=[c.Text(text=get_set.title_or_name_val(obj))],
                on_click=events.GoToEvent(url=get_set.slug_or_none(obj)),
            )
        ],
        class_name=styles.COL_STYLE
    )


def get_typs() -> list[str]:
    typs = [convert.to_snake(_.__name__) for _ in DB_MODELS]
    return typs


def get_related_typs(obj) -> list[str]:
    typs = [f"{get_set.to_snake(_.__name__)}s" for _ in DB_MODELS if not isinstance(obj, _)]
    return typs


def _object_ui_with_related(obj) -> list[tuple[str, c.Div]]:
    out_list = [
        (
            typ,
            objects_col(getattr(obj, typ)),
        )
        for typ in get_related_typs(obj)
    ]

    ident_name = get_set.title_or_name_var(obj)
    out_list.insert(1, (ident_name, title_column(obj)))
    return out_list


def title_column(obj):
    url = get_set.slug_or_none(obj)
    title = get_set.title_or_name_val(obj)
    return builders.wrap_divs(
        class_name=TITLE_COL,
        components=[
            ui_link(title, url),
        ],
    )


def play_column(url):
    res = builders.wrap_divs(
        class_name=PLAY_COL,
        components=[
            c.Link(
                components=[c.Text(text="Play")],
                on_click=GoToEvent(url=url),
            ),
        ],
    )
    return res


def ui_link(title, url, on_click=None, class_name="") -> c.Link:
    on_click = on_click or GoToEvent(url=url)
    link = c.Link(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)
    return link
