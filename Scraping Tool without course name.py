import requests
from bs4 import BeautifulSoup

def scrape_course_data(course_url):
    # Fetch the course's page
    response = requests.get(course_url)
    course_soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the major's name
    course_name_element = course_soup.select_one('div.header_text--courses h1 span')
    course_name = course_name_element.text.strip() if course_name_element else 'No course name found'

    # Extract the introduction
    introduction_element = course_soup.select_one('div.c-copy-section p.keyfact')
    introduction = introduction_element.text.strip() if introduction_element else 'No introduction found'
    
    # Extract modules
    modules = []
    year_headings = course_soup.select('div.o-container--small h4')
    for heading in year_headings:
        if 'year' in heading.text.lower() or 'final' in heading.text.lower():
            next_ul = heading.find_next('ul')
            if next_ul:
                modules.extend([li.text.strip() for li in next_ul.find_all('li')])

    # Extract assessment information
    assessment_info = {}
    assessment_table = course_soup.select_one('p:contains("assessment method") + table')
    if assessment_table:
        rows = assessment_table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 4:  # Ensure there are four columns
                year, written_exam, coursework, practical_exam = [col.text.strip() for col in columns]
                assessment_info[f'Year {year}'] = {
                    'Written Exam': written_exam,
                    'Coursework': coursework,
                    'Practical Exam': practical_exam
                }

    return {
        'Course Name': course_name,
        'Introduction': introduction,
        'Modules': modules,
        'Assessment': assessment_info
    }

course_url = 'https://courses.uwe.ac.uk/6F3B/software-engineering-for-business' #Add major url here
course_data = scrape_course_data(course_url)

# Print the course data
#print(f"Course Name: {course_data['Course Name']}")
print(f"Introduction: {course_data['Introduction']}")
print("\nModules:")
for module in course_data['Modules']:
    print(f" - {module}")

print("\nAssessment Information:")
for year, details in course_data['Assessment'].items():
    print(f" {year}:")
    print(f"  Written Exam: {details['Written Exam']}")
    print(f"  Coursework: {details['Coursework']}")
    print(f"  Practical Exam: {details['Practical Exam']}\n")
