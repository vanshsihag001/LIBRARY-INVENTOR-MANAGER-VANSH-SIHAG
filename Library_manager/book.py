# library_manager/book.py

class Book:
    
    #Represents a single book in the library.
    #status = "available" or "issued"
    

    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        
        if status not in ("available", "issued"):
            status = "available"
        self.status = status

    def __str__(self):
        return f"[{self.isbn}] {self.title} by {self.author} - {self.status}"

    def to_dict(self):
        #Convert Book to a dict for JSON saving
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        #Create a Book from dict data
        return cls(
            title=data.get("title", "Unknown"),
            author=data.get("author", "Unknown"),
            isbn=data.get("isbn", ""),
            status=data.get("status", "available"),
        )

    def issue(self):
        #Mark book as issued if available.
        if self.is_available():
            self.status = "issued"
            return True
        return False

    def return_book(self):
        #Mark book as available if currently issued
        if not self.is_available():
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"