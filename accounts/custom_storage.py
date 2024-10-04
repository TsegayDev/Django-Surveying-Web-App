from django.core.files.storage import FileSystemStorage

class BookCoverStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = '/path/to/book_covers'
        super().__init__(*args, **kwargs)

class UserProfileStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = '/path/to/user_profiles'
        super().__init__(*args, **kwargs)
