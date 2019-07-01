import random

from tagging import Session
from tagging.model import Item, Tag
import tagging.filehash

tag_names = ["snow", "fire", "lightning", "water", "simulation", "static"]


def insert(filepath, tags_):
    tag_names_ = set(tags_)
    all_tags = list_tags()
    existing_tags = []
    for tag_name in tag_names_:
        for tag in all_tags:
            if tag.name == tag_names:
                existing_tags.append(tag)
                break
        else:
            existing_tags.append(Tag(name=tag_name))
    hash_ = tagging.filehash.hash_from_file(filepath)
    item_ = Item(name=filepath, hash=hash_)
    session = Session()
    session.add(item_)
    session.commit()


def list_tags(file=None):
    session = Session()
    if file:
        return session.query(Item).one()
    else:
        return session.query(Tag).all()


if __name__ == "__main__":

    def test_data():
        import os
        path = r"D:\01_Projects\18_animationProjects\projects\02_sagenkoenige\artwork\creatureA"
        content = os.listdir(path)
        for file in content:
            filepath = os.path.join(path, file)
            yield (filepath)

    """
    for filepath in test_data():
        tags = random.sample(tag_names, 2)
        insert(filepath, tags)
    """

    session = Session()
    items = session.query(Item).all()
    for item in items:
        tags = [tag.name for tag in item.tags]
        print("%s: %s"%(item.name, tags))

    print("----------------")

    items_snow = session.query(Item).filter(Item.tags.any(Tag.name == "snow")).all()
    for item in items_snow:
        tags = [tag.name for tag in item.tags]
        print("%s: %s"%(item.name, tags))

    print("All tags: %s" % ([tag.name for tag in session.query(Tag).order_by(Tag.name)]))
    """
