from bs4 import BeautifulSoup


def apply_func_to_dict(d, keys, func):
    new_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            new_dict[k] = apply_func_to_dict(v, keys, func)
        elif isinstance(v, list):
            new_dict[k] = []
            for i in v:
                if isinstance(i, str):
                    if k in keys:
                        i = func(i)
                    new_dict[k].append(i)
                else:
                    new_dict[k].append(apply_func_to_dict(i, keys, func))
        else:
            if k in keys:
                v = func(v)
            new_dict[k] = v
    return new_dict


def add_target_blank_to_links(text):
    soup = BeautifulSoup(text, "html.parser")

    for link in soup.find_all("a"):
        link["target"] = "_blank"
        link["rel"] = "noopener"

    text = soup.body.decode_contents() if soup.body is not None else str(soup)
    return text
