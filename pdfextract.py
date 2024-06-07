import pdfplumber
import csv
import re

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text

def categorize_resume(text):
    sections = {
        'education': '',
        'skills': '',
        'experience': '',
        'projects': '',
        'certifications': '',
        'other': ''
    }

    # Define patterns for each section
    patterns = {
        'education': r'(education|academic background|qualifications)',
        'skills': r'(skills|technical skills|expertise)',
        'experience': r'(experience|work history|employment)',
        'projects': r'(projects|portfolio)',
        'certifications': r'(certifications|courses|training)'
    }

    current_section = 'other'
    lines = text.split('. ')

    for line in lines:
        section_found = False
        for section, pattern in patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                current_section = section
                section_found = True
                break
        sections[current_section] += line.strip() + ' '

    return sections

def main():
    pdf_path = 'resume.pdf'  # Change to your PDF path
    extracted_text = extract_text_from_pdf(pdf_path)
    preprocessed_text = preprocess_text(extracted_text)
    categorized_text = categorize_resume(preprocessed_text)

    # Store in CSV with tags/labels
    with open('categorized_resume.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Text'])
        for category, text in categorized_text.items():
            writer.writerow([category, text.strip()])

if __name__ == "__main__":
    main()
