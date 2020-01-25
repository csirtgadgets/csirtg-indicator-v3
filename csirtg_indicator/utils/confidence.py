

def estimate_confidence(i):  # NOSONAR
    """
    Estimate the confidence of an indicator
    :param i: csirtg_indicator.Indicator object
    :return: int
    """
    if i.is_hash:
        return 4

    if not getattr(i, 'tags'):
        return 0

    if i.is_email:
        if len(i.tags) > 1:
            return 4
        return 3

    if i.is_url:
        if len(i.tags) > 1 or 'phishing' in i.tags:
            return 4
        return 3

    if i.tags and len(i.tags) > 1:
        return 3

    if i.is_ip:
        if not i.tags:
            return 2

        if 'scanner' in i.tags or len(i.tags) > 1:
            return 4

    if i.tags and len(i.tags) > 1:
        return 3

    return 2
