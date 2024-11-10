from types import SimpleNamespace
from typing import Dict, Union
import collections.abc


def get_attrdict(d: Dict) -> SimpleNamespace:
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = get_attrdict(v)
    return SimpleNamespace(**d)


"""
Dictionary methods adapated from @vitchyr
"""


def dot_map_dict_to_nested_dict(dot_map_dict):
    """
    Convert something like
    ```
    {
        'one.two.three.four': 4,
        'one.six.seven.eight': None,
        'five.nine.ten': 10,
        'five.zero': 'foo',
    }
    ```
    into its corresponding nested dict.

    http://stackoverflow.com/questions/16547643/convert-a-list-of-delimited-strings-to-a-tree-nested-dict-using-python
    :param dot_map_dict:
    :return:
    """
    tree = {}

    for key, item in dot_map_dict.items():
        split_keys = key.split('.')
        if len(split_keys) == 1:
            if key in tree:
                raise ValueError("Duplicate key: {}".format(key))
            tree[key] = item
        else:
            t = tree
            for sub_key in split_keys[:-1]:
                t = t.setdefault(sub_key, {})
            last_key = split_keys[-1]
            if not isinstance(t, dict):
                raise TypeError(
                    "Key inside dot map must point to dictionary: {}".format(
                        key
                    )
                )
            if last_key in t:
                raise ValueError("Duplicate key: {}".format(last_key))
            t[last_key] = item
    return tree


def nested_dict_to_dot_map_dict(d, parent_key=''):
    """
    Convert a recursive dictionary into a flat, dot-map dictionary.

    :param d: e.g. {'a': {'b': 2, 'c': 3}}
    :param parent_key: Used for recursion
    :return: e.g. {'a.b': 2, 'a.c': 3}
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + "." + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(nested_dict_to_dot_map_dict(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def merge_recursive_dicts(a, b, path=None,
                          ignore_duplicate_keys_in_second_dict=False):
    """
    Merge two dicts that may have nested dicts.
    """
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_recursive_dicts(a[key], b[key], path + [str(key)],
                                      ignore_duplicate_keys_in_second_dict=ignore_duplicate_keys_in_second_dict)
            elif a[key] == b[key]:
                print("Same value for key: {}".format(key))
            else:
                duplicate_key = '.'.join(path + [str(key)])
                if ignore_duplicate_keys_in_second_dict:
                    print("duplicate key ignored: {}".format(duplicate_key))
                else:
                    raise Exception(
                        'Duplicate keys at {}'.format(duplicate_key)
                    )
        else:
            a[key] = b[key]
    return a


def dict_of_list__to__list_of_dicts(dct, n_items):
    """
    ```
    x = {'foo': [3, 4, 5], 'bar': [1, 2, 3]}
    ppp.dict_of_list__to__list_of_dicts(x, 3)
    # Output:
    # [
    #     {'foo': 3, 'bar': 1},
    #     {'foo': 4, 'bar': 2},
    #     {'foo': 5, 'bar': 3},
    # ]
    ```
    :param dict:
    :param n_items:
    :return:
    """
    if n_items is None:
        n_items = len(next(iter(dct.values())))
    new_dicts = [{} for _ in range(n_items)]
    for key, values in dct.items():
        assert len(values) == n_items, (key, len(values), n_items)
        for i in range(n_items):
            new_dicts[i][key] = values[i]
    return new_dicts


def list_of_dicts__to__dict_of_lists(lst: Union[list, tuple]):
    """
    ```
    x = [
        {'foo': 3, 'bar': 1},
        {'foo': 4, 'bar': 2},
        {'foo': 5, 'bar': 3},
    ]
    ppp.list_of_dicts__to__dict_of_lists(x)
    # Output:
    # {'foo': [3, 4, 5], 'bar': [1, 2, 3]}
    ```
    """
    assert isinstance(lst, (list, tuple)), type(lst)
    if len(lst) == 0:
        return {}
    keys = lst[0].keys()
    # output_dict = collections.defaultdict(list)
    output_dict = dict()
    for d in lst:
        assert set(d.keys()) == set(keys), (d.keys(), keys)
        for k in keys:
            if k not in output_dict:
                output_dict[k] = []
            output_dict[k].append(d[k])
    return output_dict
