def inheritdocs(class_):
    """
    Args:
        class_ (class): the class to make inherit documentation from any inherited
    """
    for name, method in vars(class_).items():
        if not method.__doc__:
            for parent in class_.__bases__:
                try:
                    p_method = getattr(parent, name)
                    if p_method and p_method.__doc__:
                        method.__doc__ = p_method.__doc__
                except AttributeError:
                    continue
    return class_
