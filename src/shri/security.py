import site
from os import path


def replace_server_error_template(base_dir):
    """
    This functions takes base_dir of project as argument and
    replaces django's default 500 page with our custom 500 template
    inside site-packages. This is used to prevent leaking private credentials.
    """
    site_paths = site.getsitepackages()

    site_path = None
    for location in site_paths:
        if "site-packages" in location:
            site_path = location
            break

    if not site_path:
        return print("Site path not found in ", site_paths)

    with open(path.join(base_dir, "templates/500.html"), "r") as file:
        html_contents = file.read()

    with open(path.join(base_dir, "templates/500.txt"), "r") as file:
        txt_contents = file.read()

    with open(
        path.join(site_path, "django/views/templates/technical_500.html"), "w"
    ) as file:
        file.write(html_contents)

    with open(
        path.join(site_path, "django/views/templates/technical_500.txt"), "w"
    ) as file:
        file.write(txt_contents)
