import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


def notify_new_job(link, title, company):
    topic = os.getenv("NTFY_TOPIC")
    if not topic:
        return

    message = f"{company}: {title}\n{link}"
    url = f"https://ntfy.sh/{quote(topic)}"
    request = Request(
        url,
        data=message.encode("utf-8"),
        headers={
            "Title": "New internship found",
            "Tags": "briefcase",
            "Click": link,
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=10):
            pass
    except URLError as error:
        print(f"Could not send phone notification: {error}")
