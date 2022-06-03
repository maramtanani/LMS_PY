class LibraryCreateException(Exception):
    pass


class TitleList(list):
    pass


class Title(object):
    def __init__(self, id, name, author, isbn):
        self.id = id
        self.name = name
        self.author = author
        self.isbn = isbn
        self._copies = CopyList()

    def __str__(self):
        return f'Title with id: {self.id}'

    def __repr__(self):
        return f'Title with id: {self.id}'

    @property
    def copies_list(self):
        return self._copies

    @copies_list.setter
    def copies_list(self, value):
        self._copies = value

    def search_copies(self, copy_id):
        for copy in self._copies:
            if copy.id == copy_id:
                return copy
        return None

    def delete_copy(self, copy):
        index = self._copies.index(copy)
        self._copies.pop(index)


class Copy(object):
    def __init__(self, id, availability, publisher):
        self.id = id
        self.availability = availability
        self.publisher = publisher

    def book(self):
        self.availability = False

    def return_copy(self):
        self.availability = True

    def __str__(self):
        return f'Copy with id: {self.id}'

    def __repr__(self):
        return f'Copy with id: {self.id}'


class CopyList(list):
    pass


class Library(object):
    def __init__(self, name, id, location):
        self.name = name
        self.id = id
        self.location = location
        self._librarians = []
        self._readers = []
        self._titles = TitleList()

    @property
    def titles_list(self):
        return self._titles

    @titles_list.setter
    def titles_list(self, value):
        self._titles = value


class SearchMixin(object):
    def search_titles(self, search_value, by='name'):
        for title in self.titles_list:
            if getattr(title, by) == search_value:
                return title
        return None


class Librarian(SearchMixin):
    def __init__(self, id, full_name , age , id_no, emplyment_type):
        self.id = id
        self.name = full_name
        self.age = age
        self.id_no = id_no
        self.emplyment_type = emplyment_type

    def __str__(self):
        return f'Librarian with id: {self.id}'

    def __repr__(self):
        return f'Librarian with id: {self.id}'

    def add_title(self, title):
        self.titles_list.append(title)

    def delete_title(self, title):
        index = self.titles_list.index(title)
        self.titles_list.pop(index)

    def add_copy(self, title_id, copy):
        title = self.search_titles(title_id, 'id')
        if title:
            title.copies_list.append(copy)

    def delete_copy(self, title_id, copy_id):
        title = self.search_titles(title_id, 'id')
        if title:
            copy = title.search_copies(copy_id)
            if copy:
                title.delete_copy(copy)


class Client (SearchMixin):
    def __init__(self, id, full_name , age , id_no , phone_number ):
        self.id = id
        self.name = full_name
        self.age = age
        self.id_no = id_no
        self.phone_number = phone_number 

    def borrow(self, title_id):
        title = self.search_titles(title_id, 'id')
        if title:
            for copy in title.copies_list:
                if copy.availability:
                    copy.book()
                    return copy
        return None

    def return_copy(self, title_id, copy_id):
        title = self.search_titles(title_id, 'id')
        if title:
            copy = title.search_copies(copy_id)
            if copy:
                copy.return_copy()
        return None

    def __str__(self):
        return f'Reader with id: {self.id}'

    def __repr__(self):
        return f'Reader with id: {self.id}'


if __name__ == "__main__":
    library = Library('Library', '42', 'Wrocław')
    titles_list = library.titles_list
    print(f'Original titles_list {titles_list}')
    librarian = Librarian('42', 'Tom', 'Jack', titles_list)

    first_title = Title('1', 'The first one', 'KZ', 213)
    second_title = Title('2', 'The second one', 'OM', 123)
    librarian.add_title(first_title)
    librarian.add_title(second_title)
    print(f'Original titles_list after adding titles: {titles_list}')

    first_book_one_copy = Copy('1', True, 'Wrocław')
    first_book_two_copy = Copy('2', True, 'Wrocław')
    first_book_three_copy = Copy('3', True, 'Warszawa')
    librarian.add_copy(first_title.id, first_book_one_copy)
    librarian.add_copy(first_title.id, first_book_two_copy)
    librarian.add_copy(first_title.id, first_book_three_copy)

    second_book_one_copy = Copy('1', True, 'Warszawa')
    second_book_two_copy = Copy('2', True, 'Warszawa')
    second_book_three_copy = Copy('3', True, 'Warszawa')
    librarian.add_copy(second_title.id, second_book_one_copy)
    librarian.add_copy(second_title.id, second_book_two_copy)
    librarian.add_copy(second_title.id, second_book_three_copy)

    first_reader = Reader('1', 'Jacek', 'Lewandowski', 42, titles_list)

    searched_title = first_reader.search_titles('The first one')
    print(f'Searched title {searched_title}')
    booked_copy = first_reader.borrow(searched_title.id)
    print(f'Booked copy {booked_copy}')
    first_reader.return_copy(first_title.id, booked_copy.id)
    print(
        f'Booked copy returned - it has availability: {booked_copy.availability}')

    print('Delete title')
    librarian.delete_title(second_title)
    print(f'Available titles: {titles_list}')
    print('Delete copy')
    librarian.delete_copy(first_title.id, first_book_three_copy.id)
    print(f'Available copies: {first_title.copies_list}')
