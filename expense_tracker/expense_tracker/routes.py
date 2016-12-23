def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('list', '/')
    config.add_route('detail', '/expense/{id:\d+}')
    config.add_route('create', '/new-expense')
    config.add_route('edit', '/expense/{id:\d+}/edit')
    config.add_route('category', '/expense/{cat:\w+}')
    config.add_route('json_list', '/api/list')
    config.add_route('json_detail', '/api/detail/{id:\d+}')
