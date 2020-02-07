from MySQLdb._exceptions import IntegrityError
from parse_feed import parse_feed
from db_connect import db_connect, db_close

table, col, cursor, connection = db_connect()
INSERTION_QUERY = """INSERT INTO {} ({}) VALUES (%s) """.format(table, col)


def process_feed():
    """
    Returns
        A list of messages with the links to be posted on different social platforms.
    """
    site_name, items = parse_feed()

    # Sample Post will be of the form:
    # Checkout this new post from Git: TITLE OF THE POST https://LINK_TO_POST
    POST = """Checkout this new post from""" + site_name + """: {}"""

    messages = []
    for item in items:
        title = item.title
        link = item.link
        try:
            cursor.execute(INSERTION_QUERY, (link, ))
            messages.append(
                {
                    'text': POST.format(title),
                    'link': link,
                }
            )
            # msgs.append(POST.format(title, link))
        except IntegrityError:
            # print(f'Duplicate link : {link}')
            continue

    db_close(cursor, connection)

    return messages


if __name__ == "__main__":
    print(f'{len(process_feed())} entries were added to the database.')
