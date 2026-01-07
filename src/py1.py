#!/usr/bin/env python3
"""Simple Book Management CLI using the Library class."""
import argparse
import sys
from book_manager import Book, Library


def main(argv=None):
	argv = argv if argv is not None else sys.argv[1:]
	parser = argparse.ArgumentParser(description="Book management CLI")
	sub = parser.add_subparsers(dest="cmd")

	p_add = sub.add_parser("add", help="Add a book")
	p_add.add_argument("--isbn", required=True)
	p_add.add_argument("--title", required=True)
	p_add.add_argument("--author", required=True)
	p_add.add_argument("--year", type=int)

	p_remove = sub.add_parser("remove", help="Remove a book by ISBN")
	p_remove.add_argument("isbn", help="ISBN of the book to remove")

	p_list = sub.add_parser("list", help="List all books")
	p_list.add_argument("--json", action="store_true", help="Output JSON")

	p_find = sub.add_parser("find", help="Find books by title query")
	p_find.add_argument("query", help="Title query string")

	p_import = sub.add_parser("import", help="Import books from JSON file")
	p_import.add_argument("file", help="Path to JSON file")

	p_export = sub.add_parser("export", help="Export books to JSON file")
	p_export.add_argument("file", help="Path to JSON file")

	args = parser.parse_args(argv)

	lib = Library()
	lib.load()  # default books.json

	if args.cmd == "add":
		book = Book(isbn=args.isbn, title=args.title, author=args.author, year=args.year)
		ok = lib.add_book(book)
		if not ok:
			print("Book with that ISBN already exists.")
			return 1
		lib.save()
		print("Added:", book)
		return 0

	if args.cmd == "remove":
		ok = lib.remove_by_isbn(args.isbn)
		if not ok:
			print("No book found with that ISBN.")
			return 1
		lib.save()
		print("Removed book with ISBN", args.isbn)
		return 0

	if args.cmd == "list":
		books = lib.list_books()
		if args.json:
			import json

			print(json.dumps([b.to_dict() for b in books], indent=2, ensure_ascii=False))
			return 0
		if not books:
			print("No books in library.")
			return 0
		for b in books:
			print(f"{b.isbn} — {b.title} by {b.author}" + (f" ({b.year})" if b.year else ""))
		return 0

	if args.cmd == "find":
		found = lib.find_by_title(args.query)
		if not found:
			print("No matches.")
			return 0
		for b in found:
			print(f"{b.isbn} — {b.title} by {b.author}")
		return 0

	if args.cmd == "import":
		lib.load(args.file)
		lib.save()
		print("Imported from", args.file)
		return 0

	if args.cmd == "export":
		lib.save(args.file)
		print("Exported to", args.file)
		return 0

	parser.print_help()
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

