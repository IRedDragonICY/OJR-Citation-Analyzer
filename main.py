import fitz
import google.generativeai as genai
import pandas as pd

with open('api_key.txt', 'r') as file:
    api_key = file.read()

def extract_references(file_path):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    doc = fitz.open(file_path)
    text = ''
    for page in doc:
        text += page.get_text()

    references_index = text.upper().find('REFERENCES')
    end_index = text.upper().find('ACKNOWLEDGMENTS') if text.upper().find('ACKNOWLEDGMENTS') != -1 else text.upper().find('APPENDIX')

    references_text = text[references_index:end_index] if references_index != -1 and end_index != -1 else text[references_index:]

    journals = [line.split('. ', 1)[-1] for line in model.generate_content("Extract the FULL JOURNAL names from the following references according to Scimago Journal Rank (SJR): " + references_text).text.split('\n')]

    index_key = [line.split('. ', 1)[-1] for line in model.generate_content("Extract the journal names from the following references (must same as references!):" + references_text).text.split('\n')]

    return dict(zip(index_key, journals))


def comment_references(pdf, index_key, sjr,journalid):
    references_found = False
    for page_num, page in enumerate(pdf, start=1):
        text = page.get_text()
        if "REFERENCES" in text:
            references_found = True
        if references_found:
            web = f"https://www.scimagojr.com/journalsearch.php?q={journalid}&tip=sid&clean=0"
            comment = str(sjr) + "\n" + web
            search_results = page.search_for(index_key)
            for result in search_results:
                highlight = page.add_highlight_annot(result)
                highlight.set_info(title="ScimagoJR", content=comment)


def main():
    journals = extract_references('references.pdf')

    df = pd.read_csv('scimagojr 2022.csv', sep=';')
    pdf = fitz.open('references.pdf')

    quartiles_count = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Not found': 0}

    for journal in journals.values():
        matching_rows = df[df['Title'] == journal]

        if len(matching_rows) > 0:
            quartile = matching_rows.iloc[0]["SJR Best Quartile"]
            print(f'Journal: {journal} - SJR: {quartile}   Name Journal on SJR: {matching_rows.iloc[0]["Title"]}  ID: {matching_rows.iloc[0]["Sourceid"]}')
            index_key = list(journals.keys())[list(journals.values()).index(journal)]
            journalid = matching_rows.iloc[0]["Sourceid"]
            comment_references(pdf, index_key, quartile, journalid)
            # Menambahkan count untuk quartile ini
            quartiles_count[quartile] += 1
        else:
            print('Journal not found')
            quartiles_count['Not found'] += 1

    total_journals = sum(quartiles_count.values())
    print("\nSummary:")
    for quartile, count in quartiles_count.items():
        percentage = (count / total_journals) * 100
        print(f'{quartile}: {count} journals ({percentage:.2f}%)')

    for page in pdf:
        if 'REFERENCES' in page.get_text():
            comment = "\n".join([f'{quartile}: {count} journals ({(count / total_journals) * 100:.2f}%)' for quartile, count in quartiles_count.items()])
            highlight = page.add_highlight_annot(page.search_for("REFERENCES")[0])
            highlight.set_info(title="Summary", content=comment)

    pdf.save('references1.pdf')
    pdf.close()
    print('Done')

if __name__ == "__main__":
    main()
