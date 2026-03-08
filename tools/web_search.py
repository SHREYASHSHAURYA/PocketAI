from ddgs import DDGS


def web_search(query, max_results=5):

    try:
        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)

            for r in search_results:
                title = r.get("title", "")
                body = r.get("body", "")
                link = r.get("href", "")

                text = f"{title}: {body} (Source: {link})"
                results.append(text)

        if not results:
            return None

        return "\n".join(results)

    except Exception:
        return None