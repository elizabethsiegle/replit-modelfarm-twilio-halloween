import streamlit as st
import os
from PIL import Image
from replit.ai.modelfarm import ChatMessage, ChatModel, ChatSession
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN'] 

client = Client(account_sid, auth_token)

st.title('Scare👻 a friend w/ a phone call☎️!')

image = Image.open('unsplashskeleton.jpeg')
st.write("Image is from [Sabina Music Rich on Unsplash](https://unsplash.com/photos/grayscale-photo-of-person-wearing-mask-OJy0JHnoUZQ?utm_content=creditShareLink&utm_medium=referral&utm_source=unsplash)")
st.image(image)

scare_input = st.text_input("What is your friend scared of?🕷️🐍")
like_input = st.text_input("What does your friend like?😍")

system_prompt = """
You are a master story-teller. Your stories are fictional and entertaining. It is Halloween, so most of the things you talk about are Halloween-themed.
"""

prompt = """
My grandma and I would always play tricks on each other by pretending to be scary storytelling clowns who created scary yet funny stories. She is ill. Cheer me up by crafting a short, scary yet punny and humorous tale for someone who likes the following: {} and is afraid of the following: {}. The output must only begin with "Once upon a time" and end with "the end." Do not mention my grandmother or me.
"""

user_num = st.text_input("Enter your friend's phone #, please")
if st.button('Enter'):
  model = ChatModel("chat-bison")
  response = model.chat([
    ChatSession(
      context=system_prompt,
      examples=[],
      messages=[
        ChatMessage(author="USER", content=prompt.format(like_input, scare_input)),
      ],
    )
  ], temperature=0.2)
  
  story = response.responses[0].candidates[0].message.content

  st.write("Your friend will get a phone call that spookily says: ", story)
  
  twiml = f"<Response><Say voice='Polly.Brian' language='en-UK'><prosody pitch='-10%' rate='85%' volume='-6dB'>{story}</prosody></Say></Response>"
  call = client.calls.create( 
      twiml = twiml,
      to=user_num, #user input 
      from_= '+1 855 302 1845' #'+18668453916' #twilio num
  )
  print(call.sid)
  
  # out_msg = f"Here is a scary story search result from Metaphor: {met_url}"
  # msg = client.messages.create( 
  #     body = out_msg,
  #     to=user_num, #user input 
  #     from_= '+1 855 302 1845' #'+18668453916' #twilio num
  # )
  # print(msg.sid)
