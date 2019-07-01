import random
import logging

from tagging import Session
from tagging.model import Item, Tag
import tagging.filehash


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('tagging')

tag_names = ["snow", "fire", "lightning", "water", "simulation", "static"]


def insert(filepath, tags_, session):
    tag_names_ = set(tags_)
    log.debug('Tag: %s' % tag_names_)
    all_tags = list_tags(session=session)
    log.debug(all_tags)
    for t in all_tags:
        log.debug("Existing Tag %s" % t.name)
    existing_tags = []
    for tag_name in tag_names_:
        for tag in all_tags:
            log.debug('Existing tag: %s' % tag.name)
            log.debug('Given Tag: %s' % tag_name)
            if tag.name == tag_name:
                existing_tags.append(tag)
                break
        else:
            existing_tags.append(Tag(name=tag_name))
    hash_ = tagging.filehash.hash_from_file(filepath)
    item_ = Item(name=filepath, hash=hash_, tags=existing_tags)

    session.add(item_)
    session.commit()
    session.close()


def list_tags(session, file=None):
    if file:
        return session.query(Item).filter(Item.name == file).one()
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

    session = Session()
    for filepath in test_data():
        tags = random.sample(tag_names, 2)
        insert(filepath, tags, session)

    items = session.query(Item).all()
    for item in items:
        tags = [tag.name for tag in item.tags]
        print("%s: %s : %s"%(item.name, tags, item.hash))

    print("----------------")

    items_snow = session.query(Item).filter(Item.tags.any(Tag.name == "snow")).all()
    for item in items_snow:
        tags = [tag.name for tag in item.tags]
        print("%s: %s"%(item.name, tags))

    print("All tags: %s" % ([tag.name for tag in session.query(Tag).order_by(Tag.name)]))

    fire_tag = session.query(Tag).filter(Tag.name=="fire").all()
    for f_tag in fire_tag:
        print(f_tag.name)
        for i in f_tag.items:
            print(i.name)
