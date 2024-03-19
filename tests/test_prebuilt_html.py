from fastuipr import prebuilt_html


def test_prebuilt_html():
    html = prebuilt_html()
    assert html.startswith('<!doctype html>')
    assert 'https://cdn.jsdelivr.net/npm/@pydantic/fastui-prebuilt' in html
    assert '<title></title>' in html
    assert '<meta name="fastuipr:APIRootUrl"' not in html
    assert '<meta name="fastuipr:APIPathMode"' not in html
    assert '<meta name="fastuipr:APIPathStrip"' not in html


def test_prebuilt_html_meta_tags():
    html = prebuilt_html(
        title='Test Title',
        api_root_url='/admin/api',
        api_path_mode='query',
        api_path_strip='/admin',
    )
    assert '<title>Test Title</title>' in html
    assert '<meta name="fastuipr:APIRootUrl" content="/admin/api" />' in html
    assert '<meta name="fastuipr:APIPathMode" content="query" />' in html
    assert '<meta name="fastuipr:APIPathStrip" content="/admin" />' in html
