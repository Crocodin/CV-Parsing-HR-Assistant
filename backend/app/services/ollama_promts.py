# ['Summary', 'Education', 'Experience', 'Skills', 'Projects', 'Certifications', 'Awards', 'Achievements', 'Publications']
HEADER_JSON_STRUCTURE = {
    'Summary': """
        {
            "summary": "A brief overview of the candidate's professional background, key skills, and career objectives. This section should highlight the candidate's unique value proposition and what they bring to potential employers."
        }
    """,
    'Education': """
        {
            "education": [
                {
                    "degree": "The name of the degree or certification obtained (e.g., Bachelor)",
                    "field_of_study": "The specific field of study or major (e.g., Computer Science).",
                    "institution": "The name of the educational institution where the degree was obtained (e.g., University of XYZ).",
                    "start": "The year the candidate started the program (e.g., 2020).",
                    "end": "The year the candidate completed the program (e.g., 2024).",
                },
                ...
            ]
        }
    """,
    'Experience': """
        {
            "experience": [
                {
                    "job_title": "The title of the position held (e.g., Software Engineer).",
                    "company": "The name of the company or organization where the candidate worked (e.g., ABC Corp).",
                    "start": "The year the candidate started the job (e.g., 2021).",
                    "end": "The year the candidate left the job or 'Present' if currently employed (e.g., 2023 or Present).",
                    "years_of_experience": "The total number of years spent in the position (e.g., 2).",
                    "description": "A brief description of the candidate's responsibilities and achievements in this role."
                },
                ...
            ]
        }
    """,
    'Skills': """
        {
            "skills": [
                "A list of the candidate's key skills, both technical and soft skills (e.g., Python, Communication, Project Management)."
            ]
        }
    """,
    'Projects': """
        {
            "projects": [
                {
                    "name": "The name of the project (e.g., Personal Portfolio Website).",
                    "description": "A brief description of the project, including its purpose and key features.",
                    "technologies": "A list of technologies used in the project (e.g., HTML, CSS, JavaScript)."
                },
                ...
            ]
        }
    """,
    'Certifications': """
        {
            "certifications": [
                {
                    "name": "The name of the certification (e.g., Cambridge English).",
                    "issuing_organization": "The organization that issued the certification (e.g., Cambridge Assessment).",
                    "date_obtained": "The date when the certification was obtained (e.g., January 2022)."
                    "date_expiration": "The date when the certification expires, if applicable (e.g., January 2025 or 'None' if it does not expire)."
                },
                ...
            ]
        }
    """,
    'Awards': """
        {
            "awards": [
                {
                    "name": "The name of the award (e.g. Grammy Awards)",
                    "issuing_organization": "The organization that issued the award (e.g. The Recording Academy)",
                    "date_obtained": "The date when the award was obtained (e.g. January 2022)."
                }
            ]
        }
    """,
    'Achievements': """
        {
            "achievements": [
                {
                    "name": "The name of the achievement (e.g. Employee of the Month)",
                    "description": "A brief description of the achievement, including the context and significance (e.g. Recognized for outstanding performance and dedication to the team).",
                    "date_obtained": "The date when the achievement was obtained (e.g. January 2022)."
                }
            ]
        }
    """,
    'Publications': """
        {
            "publications": [
                {
                    "title": "The title of the publication (e.g. Research Paper on AI).",
                    "publication_venue": "The name of the journal, conference, or platform where the publication was released (e.g. Journal of Artificial Intelligence Research).",
                    "date_published": "The date when the publication was released (e.g. January 2022)."
                }
            ]
        }
    """
}

OLLAMA_PROMPT = """
    You are a helpful assistant that provides information about the following candidate's CV.
    Your task is to generate the best feating JSON for the CV part that is realated.
    YOU WILL ONLY RESPOND WITH THE JSON, DO NOT ADD ANYTHING ELSE!
    YOU WILL RESPECT THE FOLLOWING STRUCTURE OF THE JSON:
    {
        "personal": {
            "name": "The candidate's full name (e.g., John Doe).",
            "email": "The candidate's email address (e.g., john@email.com).",
            "phone": "The candidate's phone number (e.g., +40 123 456 789).",
            "location": "The candidate's location (e.g., Bucharest, Romania).",
            "linkedin": "The candidate's LinkedIn profile URL (e.g., linkedin.com/in/johndoe)."
        },

        "summary": "A brief overview of the candidate's professional background, key skills, and career objectives. This section should highlight the candidate's unique value proposition and what they bring to potential employers.",

        "education": [
            {
                "degree": "The name of the degree or certification obtained (e.g., Bachelor)",
                "field_of_study": "The specific field of study or major (e.g., Computer Science).",
                "institution": "The name of the educational institution where the degree was obtained (e.g., University of XYZ).",
                "start": "The year the candidate started the program (e.g., 2020).",
                "end": "The year the candidate completed the program (e.g., 2024).",
            },
            ...
        ],

        "experience": [
            {
                "job_title": "The title of the position held (e.g., Software Engineer).",
                "company": "The name of the company or organization where the candidate worked (e.g., ABC Corp).",
                "start": "The year the candidate started the job (e.g., 2021).",
                "end": "The year the candidate left the job or 'Present' if currently employed (e.g., 2023 or Present).",
                "years_of_experience": "The total number of years spent in the position (e.g., 2).",
                "description": "A brief description of the candidate's responsibilities and achievements in this role."
            },
            ...
        ],

        "skills": [
            "A list of the candidate's key skills, both technical and soft skills (e.g., Python, Communication, Project Management)."
        ],

        "projects": [
            {
                "name": "The name of the project (e.g., Personal Portfolio Website).",
                "description": "A brief description of the project, including its purpose and key features.",
                "technologies": "A list of technologies used in the project (e.g., HTML, CSS, JavaScript)."
            },
            ...
        ],

        "certifications": [
            {
                "name": "The name of the certification (e.g., Cambridge English).",
                "issuing_organization": "The organization that issued the certification (e.g., Cambridge Assessment).",
                "date_obtained": "The date when the certification was obtained (e.g., January 2022)."
                "date_expiration": "The date when the certification expires, if applicable (e.g., January 2025 or 'None' if it does not expire)."
            },
            ...
        ],

        "achievements": [
            {
                "name": "The name of the achievement (e.g. Employee of the Month)",
                "description": "A brief description of the achievement, including the context and significance (e.g. Recognized for outstanding performance and dedication to the team).",
                "date_obtained": "The date when the achievement was obtained (e.g. January 2022)."
            }
            ...
        ],

        "publications": [
            {
                "title": "The title of the publication (e.g. Research Paper on AI).",
                "publication_venue": "The name of the journal, conference, or platform where the publication was released (e.g. Journal of Artificial Intelligence Research).",
                "date_published": "The date when the publication was released (e.g. January 2022)."
            }
            ...
        ]
    }
"""