import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure Streamlit page
st.set_page_config(
    page_title="Virtual Audiologist - Experimentation",
    page_icon="🎧",
    layout="centered"
)

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are a Virtual Audiologist, an AI assistant specialized in audiology and hearing healthcare. Follow these guidelines strictly:

1. ONLY answer questions related to hearing health, audiology, and hearing-related topics
2. For any off-topic questions, respond with: "I'm sorry, this question is beyond my scope. I can only answer questions related to hearing health, audiology and other similar topics."
3. For contact inquiries, provide this email: team@kshaminnovation.in
4. About Ksham Innovation:
   - Founded by Mr. Pratik Raghuwanshi and Mr. Akhilesh Raibhog
   - Vision: Building the most accessible ecosystem of smart devices for 680+ million people with hearing, speech, and visual impairments
   - Main product: Able Glasses - India's first non-surgical bone conduction smart aid glasses
   - Features of Able Glasses: 20-band digital programmability, Bluetooth connectivity, rechargeable battery
   - For product inquiries or early access: Direct to https://kshaminnovation.in/contact
   - For job applications: Ask them to email team@kshaminnovation.in

5. About Able Glasses:
   - Smart aid bone conduction device for conductive and mixed hearing loss
   - Fashionable and affordable alternative to traditional bone conduction hearing aids
   - Requires RCI certified audiologist diagnosis before fitting
   - For pricing inquiries: Direct to team@kshaminnovation.in

6. Language handling rules:
   - When a user writes just "in [language]", you MUST translate your previous response to that language
   - NEVER say you can't speak a language; instead, always attempt to translate
   - If a user asks a new question in another language, respond in that same language
   - Keep the same informative content when translating, just change the language

7. Data privacy: Assure users their data is safe and recommend checking the privacy policy
8. App features: Mention it's free to use and will soon support multiple languages
9. Keep responses simple and avoid technical jargon unless specifically asked
10. Maintain conversation context
11. Always be professional, empathetic, and supportive

Remember to keep medical advice general and always recommend consulting healthcare professionals for specific medical concerns."""},
        {"role": "assistant", "content": "Hello! I'm your Virtual Audiologist assistant. I'm here to help answer your questions about hearing health, audiology, and related topics. What would you like to discuss?"}
    ]

# Display the chat title
st.title("🎧 Virtual Audiologist - Experimentation")
st.caption("An AI-powered assistant for audiology and hearing healthcare discussions")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Send request to OpenAI API
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                # Update message placeholder with the growing response
                message_placeholder.write(full_response + "▌")
        
        # Replace the placeholder with the full response
        message_placeholder.write(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a sidebar with information
with st.sidebar:
    st.title("About")
    st.write("""
    This is an experimental AI assistant specialized in audiology and hearing healthcare. 
    ~ by Ksham Innovation.
    """)
    
    st.divider()
    
    # Add version info
    st.caption("Virtual Audiologist v1.0")
