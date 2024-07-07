import openai
import fitz  # PyMuPDF

# Set your OpenAI API key here
api_key = 'YOUR_OPENAI_API_KEY'
openai.api_key = api_key

# Set the ChatGPT endpoint URL
endpoint_url = 'https://api.openai.com/v1/chat/completions'

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def parse_resume_with_chatgpt(resume_text):
    """Parse the resume text using ChatGPT API and return JSON formatted result."""
    prompt = f"""
    You are a professional resume parser. Your task is to extract relevant information from the resume provided and convert it into a structured JSON format. Here is the resume:

    {resume_text}

    Please parse the content and structure it into the following JSON format:

    {{
      "Name": "Name of the individual",
      "Contact": {{
        "Phone": "Phone number",
        "Email": "Email address",
        "LinkedIn": "LinkedIn profile URL",
        "GitHub": "GitHub profile URL"
      }},
      "Education": [
        {{
          "Institution": "Name of the institution",
          "Degree": "Degree obtained",
          "Field of Study": "Field of study",
          "Start Date": "Start date",
          "End Date": "End date"
        }}
      ],
      "Experience": [
        {{
          "Company": "Company name",
          "Position": "Job title",
          "Start Date": "Start date",
          "End Date": "End date",
          "Responsibilities": [
            "Responsibility 1",
            "Responsibility 2"
          ]
        }}
      ],
      "Skills": [
        "Skill 1",
        "Skill 2"
      ],
      "Projects": [
        {{
          "Project Name": "Name of the project",
          "Description": "Brief description of the project",
          "Technologies": [
            "Technology 1",
            "Technology 2"
          ]
        }}
      ]
    }}

    Please ensure that the information is parsed accurately and structured according to the format above.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can choose another model like "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a professional resume parser."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.2
        )
        # Extract the response text
        parsed_resume = response.choices[0].message['content'].strip()
        return parsed_resume
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main(pdf_path):
    """Main function to extract text from PDF and parse it using ChatGPT API."""
    resume_text = extract_text_from_pdf(pdf_path)
    parsed_resume = parse_resume_with_chatgpt(resume_text)
    if parsed_resume:
        print(parsed_resume)
    else:
        print("Failed to parse the resume.")

# Example usage
pdf_path = 'Smilika_Reddy_Sangam_025 (1).pdf'  # Path to your PDF resume
main(pdf_path)
