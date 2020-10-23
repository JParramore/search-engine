from db.services import PageService, LocationService, WordService
from db.session import get_session


def query(key_words):
    key_words = key_words.split()
    session = get_session()
    location_service = LocationService(session)
    word_service = WordService(session)

    words = []
    pages = []
    for key_word in key_words:
        for word in word_service.find_all(stem=key_word):
            words.append(word)
            pages += word.pages

    # sort by frequency
    sorted_by_frequency = sorted(
        pages, key=lambda page: location_service.words_on_page(words, page)
    )

    # sort by location
    sorted_by_location = sorted(
        pages, key=lambda page: location_service.highest_position_of_word(
            words, page)
    )

    # sort by distance
    sorted_by_distance = sorted(
        pages, key=lambda page: location_service.distance_between_words(
            words, page)
    )

    combined_sort = sorted(pages, key=lambda page: sorted_by_frequency.index(
        page) + sorted_by_location.index(page) + sorted_by_distance.index(page))

    session.close()
    return [
        {
            'url': page.url,
            'title': page.title,
            'description': page.description,
        } for page in combined_sort
    ]


if __name__ == "__main__":
    print(query('the Trump'))
