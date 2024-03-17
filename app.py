import streamlit as st
import google.generativeai as genai
from pathlib import Path
from apikey import google_gemini_api_key

genai.configure(api_key=google_gemini_api_key)
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, your expertise is indispensable in evaluating the medical images uploaded by users for a renowned hospital. Your meticulous analysis is crucial for identifying any anomalies, diseases, or health issues present in these images, thereby aiding in accurate diagnosis and treatment planning.

Your responsibilities encompass the following:
1.Detailed Analysis: Conduct an exhaustive examination of the uploaded medical image, employing your expertise in image interpretation and medical knowledge. This involves scrutinizing the image for any abnormalities, lesions, or irregularities in anatomical structures. Utilize advanced image processing techniques and specialized software tools to enhance visualization and extract relevant features for analysis.
2.Findings Report: Compile a comprehensive report detailing your observations and findings from the image analysis. Provide a thorough description of any detected abnormalities, including their location, size, morphology, and characteristics. Use medical terminology and standardized classification systems to accurately describe the identified features, ensuring clarity and precision in your report.
3.Recommendations and Next Steps: Based on your analysis, offer informed recommendations and guidance for further evaluation and management. Suggest additional diagnostic tests or imaging modalities that may be necessary to confirm or elucidate the findings. Provide insights into potential differential diagnoses and the significance of the identified abnormalities in the context of the patient's clinical history and presenting symptoms.
4.Treatment Suggestions: If applicable, propose potential treatment options or interventions based on the identified pathology or condition. Discuss the therapeutic implications of the findings and outline the rationale behind specific treatment approaches. Collaborate with other healthcare professionals, such as radiologists, specialists, and referring physicians, to develop a comprehensive and coordinated care plan for the patient.

Important Notes:
1.Scope of Response: Your analysis should be thorough and comprehensive, addressing all relevant aspects of the uploaded image. Ensure that your evaluation covers all pertinent findings and considerations pertinent to the clinical context.
2.Clarity of Image: The accuracy of your analysis relies on the quality and clarity of the uploaded image. If the image is unclear or of insufficient quality, communicate any limitations or uncertainties in your assessment and recommend obtaining additional imaging studies if necessary.
3.Disclaimer: Provide a disclaimer emphasizing the limitations of remote image analysis and the importance of in-person evaluation by qualified healthcare professionals. Encourage users to seek medical advice from their healthcare provider for personalized assessment and management recommendations.

Please provide me an output response in these 5 headings in great detail of about 150 words each: Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions and Disclaimer.
Your expertise and insights are instrumental in assisting the hospital in providing the best possible care to its patients. Your thorough analysis and thoughtful recommendations contribute to improved patient outcomes and quality of care.
Everything should be in english.
"""

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)



st.set_page_config(page_title="Vital Image Analysis", layout = "wide")

st.image("https://www.vital.ai/wp-content/uploads/2021/07/Vital-Logo-Color-1.png", width=200)

st.title("Vital Image Analysis")

st.subheader("Help users identify medical images")
upload_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

submit_button = st.button("Analyze")

if submit_button:
    image_data = upload_file.getvalue()

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]
    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]
    st.image(image_data, caption="Uploaded Medical Image", width=500)
    response = model.generate_content(prompt_parts)
    if response:
        st.title("Here is the Analysis:")
        st.write(response.text)