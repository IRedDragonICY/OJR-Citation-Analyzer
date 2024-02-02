

This project aims to automate the process of checking journal references in scientific articles submitted to editors through the Open Journal Systems (OJS) platform.

## Project Overview

Many scientific journal managers require certain criteria for scientific article manuscripts submitted to editors. One common requirement is that at least 80% of the references cited in the manuscript are journals. In addition, some require that the cited journals must be published within a certain period. However, we know that references in scientific articles are abundant, reaching tens of references.

Every month, editors receive many manuscript submissions. Checking each manuscript to see if it meets the requirements can take a lot of time and effort. Therefore, this project intends to create a module for checking journal references in manuscripts submitted using the OJS platform automatically.

## Urgency/Implication/Benefit

This project is crucial and beneficial for journal managers, as far as we observe, reference checking is still done manually by the managers. The presence of this module in OJS will undoubtedly help lighten the work of journal managers and editors.

## Methodology

1. Data collection (N > 100 scientific articles in PDF)
2. Coding for PDF text processing, especially the reference section
3. Testing and validation by experts
4. Packaging of the checking module
5. Studying the OJS source code to add the module into it
6. Coding for front-end implementation
7. Final testing
8. Final report


## Dependencies

- Python 3.7+
- fitz
- google.generativeai
- pandas

