# Smart-Resume-Parser-And-Job-Matching-Engine-Using-NLP
Tech Stack used is: <br> 1. Python <br> 2. spaCy-For NLP (Natural Language Processing)  <br> 3. pdfminer.six and docx2txt for parsing resumes  <br> 4. scikit-learn for job matching model  <br> 5. sentence-transformers for semantic matching  <br> 6. streamlit for converting my project into a web application   <br> 7. spaCy model - en-core-web-sm
A mini AI based project appliaction that helps match resumes with job descriptions using NLP and soon BERT.
<br> PROJECT OVERVIEW
<br> 1. Resume Parsing: Extracts text from upploaded .pdf and .docx resumes.
<br> 2. Job Description Parsing: Extracts text from job description files.
<br> 3. TD-IFD Matching Engine: Compares resume with job description using TD-IFD and cosine similarity.
<br> 4. Match Score: Calculates and displays how closely a resume matches the JD.
<br> 5. Skill Extraction: Extracts technical and soft skills from resume text.
<br> 6. Bar Chart of Skill Match: Shows which skills mached and which didn't. 
<br> 7. Multiple Resume and JD Support: Works on multiple resume and job description files. 
<br> 8. Streamlit Interfce (Frontend): user friendly interactive web interface.
<br> HOW IT WORKS?
<br> Step 1: UPLOAD <br> User Uploads a resume and job description. <br> Files are saved in /resumes/ and /job_descriptions/ 
<br> Step 2: Extract text <br> Resume Text is extracted using pdfminer or docx2txt. <br> JD is extracted the same way.
<br> Step 3: Match Using TF-IDF
