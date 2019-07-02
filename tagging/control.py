import random
import logging

from tagging import Session
from tagging.model import Item, Tag
import tagging.filehash


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('tagging')


def insert(filepath, tags):
    session = Session()
    tag_names = set(tags)
    existing_tags = list_tags(session=session)
    tags = []
    for tag_name in tag_names:
        for tag in existing_tags:
            if tag.name == tag_name:
                tags.append(tag)
                break
        else:
            tags.append(Tag(name=tag_name))
    hash_ = tagging.filehash.hash_from_file(filepath)
    item = Item(name=filepath, hash=hash_, tags=tags)

    session.add(item)
    session.commit()
    session.close()


def list_tags(session, file=None):
    if file:
        return session.query(Item).filter(Item.name == file).one()
    else:
        return session.query(Tag).all()


def find_item_by_hash(hash):
    session = Session()
    item = session.query(Item).filter_by(hash=hash).all()
    session.close()
    return item


def find_item_by_name(name):
    session = Session()
    item = session.query(Item).filter(Item.name == name).all()
    session.close()
    return item


def find_items_by_tags(tags):
    session = Session()
    item = session.query(Item).filter(Tag.name.in_(tags))
    session.close()
    return item


if __name__ == "__main__":

    def test_data():
        import os
        tag_names = ["snow", "fire", "lightning", "water", "simulation", "static"]
        path = r"D:\01_Projects\18_animationProjects\projects\02_sagenkoenige\artwork\creatureA"
        content = os.listdir(path)
        for file in content:
            filepath = os.path.join(path, file)
            tags = random.sample(tag_names, 1)
            insert(filepath, tags)

    #test_data()
    session = Session()
    tags = list_tags(session)
    for tag in tags:
        print(tag.name)

    print('---')
    items = find_items_by_tags(tags=['fire'])
    for item in items:
        print(item.name)

    print('---')
    items = find_item_by_name(r'D:\01_Projects\18_animationProjects\projects\02_sagenkoenige\artwork\creatureA\creatureA_ortho_side_v002.png')
    for item in items:
        print(item.name)
        print(item.hash)

    items = find_item_by_hash(hash='ae7c4edbbe9e4da5d18594225d0366a117260215')
    print('---')
    for item in items:
        print(item.name)
        print(item.hash)