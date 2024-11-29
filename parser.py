import bibtexparser as bp

"""
# single file all fields
# multiple files all fields

{
    authors:
    title:
    type: journal, conference, book, thesis, techreport, misc
    year:
    pages:
}

"""


class Parser:

    @staticmethod
    def single_bib(bibtex: str) -> dict[str, str]:
        try:
            data = bp.parse_string(bibtex)
            result = {
                'authors': data.entries[0].fields_dict['author'].value,
                'title': data.entries[0].fields_dict['title'].value,
                'type': data.entries[0].entry_type,
                'year': data.entries[0].fields_dict['year'].value,
                'pages': data.entries[0].fields_dict['pages'].value
            }

            return result

        except Exception as e:
            Exception("Invalid bibtex file "f"{e}")

    @staticmethod
    def multiple_bib(bibtex: list[str]) -> list[dict[str, str]]:
        try:
            result = []
            for bib in bibtex:
                data = bp.parse_string(bib)
                result.append({
                    'authors': data.entries[0].fields_dict['author'].value,
                    'title': data.entries[0].fields_dict['title'].value,
                    'type': data.entries[0].entry_type,
                    'year': data.entries[0].fields_dict['year'].value,
                    'pages': data.entries[0].fields_dict['pages'].value
                })

            return result

        except Exception as e:
            Exception("Invalid bibtex file "f"{e}")


bibs = ["""
@ARTICLE{Cesar2013,
  author = {Jean César},
  title = {An amazing title},
  year = {2013},
  volume = {12},
  pages = {12--23},
  journal = {Nice Journal}
}
""", """

@ARTICLE{Cesar2014,
  author = {Jean César},
  title = {An amazing title},
  year = {2013},
  volume = {12},
  pages = {12--23},
  journal = {Nice Journal}
}
""", """

@ARTICLE{Cesar2015,
  author = {Jean César},
  title = {An amazing title},
  year = {2013},
  volume = {12},
  pages = {12--23},
  journal = {Nice Journal}
}
"""]

bib = """
@ARTICLE{Cesar2015,
  author = {Jean César},
  title = {An amazing title},
  year = {2013},
  volume = {12},
  pages = {12--23},
  journal = {Nice Journal}
}
"""

p = Parser()
print(p.single_bib(bib))
print(p.multiple_bib(bibs))
