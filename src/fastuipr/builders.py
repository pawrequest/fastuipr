import typing as _t

import pydantic as _p

from fastui import class_name as _class_name, components as c, events as e
from fastuipr import styles


def back_link(text: str = 'Back', class_name=None) -> c.Link:
    return c.Link(components=[c.Text(text=text)], on_click=e.BackEvent(), class_name=class_name)


def model_nav(model_with_name_and_url_props) -> c.Link:
    return c.Link(
        components=[c.Text(text=model_with_name_and_url_props.__name__.title())],
        on_click=e.GoToEvent(url=model_with_name_and_url_props.url),
        active=f'startswith:{model_with_name_and_url_props.rout_prefix()}',
    )


def object_strs_texts(
        obj: _p.BaseModel,
        with_keys: _t.Literal['NO', 'YES', 'ONLY'] = 'NO',
        title: str = None,
        title_level: int = 3,
) -> list[c.Text]:
    """
    args:
    objs: pydantic models
    with_keys: 'NO', 'YES', 'ONLY' - whether to include values, keys and values, or only keys
    class_name: optional bootstrap class name
    title: optional title for the list of text components

    returns:
    a list of text components for each stringtype value in the model
    """
    txts = []
    if title:
        txts.append(c.Heading(text=title, level=title_level))
    for k, v in obj.model_dump().items():
        if not v:
            continue
        if isinstance(v, str):
            match with_keys:
                case 'NO':
                    txt_str = v
                case 'YES':
                    txt_str = f'{k} - {v}'
                case 'ONLY':
                    txt_str = k
                case _:
                    raise ValueError(f'with_keys: {with_keys} not valid')
            txts.append(c.Text(text=txt_str))
    return txts


def default_page(
        components: list[c.AnyComponent],
        title: str = '',
        navbar=None,
        footer=None,
        header_class: _class_name.ClassNameField = None,
        class_name: _class_name.ClassNameField = None,
) -> list['c.AnyComponent']:
    """"
    return a list of components wrapped in a page with title, navbar and footer

    add browser-tab Title and header component based on title and header_class
    """
    # components = list(components)
    comps = [
        *((c.Heading(text=title, class_name=header_class),) if title else ()),
        *components,
    ]
    return [
        c.PageTitle(text=title if title else ''),
        *((navbar,) if navbar else ()),
        c.Page(
            components=comps,
            class_name=class_name,
        ),
        *((footer,) if footer else ()),
    ]


def empty_page(nav_bar=None, footer=None, title='Empty Page') -> list[c.AnyComponent]:
    return default_page(
        components=[
            *((nav_bar,) if nav_bar else ()),
            c.Div.empty(),
        ],
        footer=footer,
        title=title,
    )


###

def wrap_divs(
        *,
        components: list[c.AnyComponent],
        class_name: _class_name.ClassName = None,
        inner_class_name: _class_name.ClassName = None,
        title: str | None = None,
        title_level: int = 2,
) -> c.Div:
    """
    wrap a list of components in a div, optionally with a title and/or inner class name for nesting
    use bootstrap classnames to affect container, columns, row type divs, as well as layout and styling

    use inner_wrap to nest divs, eg:

    Div.wrap(
            c.Text(text='hello'),
            c.Text(text='world'),
            class_name=styles.COL_STYLE,
            inner_class_name=styles.ROW_STYLE,
        )
    returns a single column with each component in a row
    """

    if title:
        components.insert(0, c.Heading(text=title, level=title_level))

    if inner_class_name:
        components = list_of_divs(
            components,
            class_name=inner_class_name,
        )

    return c.Div(
        components=components,
        class_name=class_name,
    )


def contained_divs(
        outers: list[list[c.AnyComponent], ...],
        container_class_name: _class_name.ClassName = styles.CONTAINER_STYLE,
        outer_class_name: _class_name.ClassName = styles.COL_STYLE,
        inner_class_name: _class_name.ClassName = styles.ROW_STYLE,
        title: str | None = None,
        title_level: int = 2,
) -> c.Div:
    """
    wrap components in divs, and then wrap those divs in a container div
    """
    outer = [wrap_divs(
        components=[inner],
        class_name=outer_class_name,
        inner_class_name=inner_class_name,
        title=title,
        title_level=title_level,
    )
        for inner in outers]
    return wrap_divs(
        components=outer,
        class_name=container_class_name,
    )


def list_of_divs(
        components: list[c.AnyComponent],
        class_name: _class_name.ClassName = None,
) -> list[c.Div]:
    """
    wrap a list of components in a list of divs with given bootstrap classname
    """
    divs = [c.Div(components=[comp], class_name=class_name) for comp in components]
    return divs


def empty_div(class_name: _class_name.ClassName = None) -> c.Div:
    """"
    return an empty div with optional bootstrap class name
    """
    return c.Div(components=[c.Text(text='')], class_name=class_name)


AlertType = _t.Literal['ERROR', 'WARNING', 'NOTIFICATION']


class AlertProt(_t.Protocol):
    message: str
    type: AlertType
    code: int | None = None


async def page_w_alerts(
        components: list['c.AnyComponent'],
        title: str = '',
        navbar=None,
        footer=None,
        class_name=None,
        alerts: list[AlertProt] | None = None,
) -> list['c.AnyComponent']:
    al_rows = await get_alert_rows(alerts) if alerts else []
    components_ = [
        *al_rows,
        *components,
    ]
    contained = [c.Div(components=components_, class_name=styles.CONTAINER_STYLE)]
    return [
        c.PageTitle(text=f'PawRequest dev - {title}' if title else ''),
        *((navbar,) if navbar else ()),
        c.Page(
            components=contained,
            class_name=class_name,
        ),
        *((footer,) if footer else ()),
    ]


async def get_alert_rows(alerts: list[AlertProt]) -> list[c.Div]:
    if not alerts:
        return []
    alert_txts = [c.Text(text=al.message) for al in alerts]
    alert_rows = list_of_divs(components=alert_txts, class_name=styles.ALERT_STYLE)
    return alert_rows
