def build_attachments(photos):
    return ",".join(
        f'photo{photo["owner_id"]}_{photo["id"]}'
        for photo in photos
    )
