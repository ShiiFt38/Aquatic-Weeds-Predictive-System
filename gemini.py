"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["AIzaSyD6ddAl28XNUyaRX1-vL2Y-T5l-Nik_fR4]"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "\nwhat is the water quality at hartbeespoort dam\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I do not have access to real-time information, including weather data. To get the current weather conditions at Hartebeesport Dam, I recommend checking a reliable weather website or app. \n\nHere are some resources you can use:\n\n* **AccuWeather:** [https://www.accuweather.com/](https://www.accuweather.com/)\n* **The Weather Channel:** [https://weather.com/](https://weather.com/)\n* **Google Weather:** [https://www.google.com/search?q=weather](https://www.google.com/search?q=weather)\n\nSimply search for \"Hartebeesport Dam weather\" on any of these websites or apps. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "what is the water quality at hartbeespoort dam",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I can't give you a definitive answer on the water quality at Hartebeesport Dam. Water quality can change frequently and is best determined by official sources. \n\nHowever, I can tell you where to find reliable information:\n\n* **Department of Water and Sanitation (DWS):** The DWS is responsible for monitoring and managing water quality in South Africa. They likely have reports or data available on their website. \n* **Local Municipality:** The municipality responsible for Hartebeesport Dam may have water quality reports or updates.\n* **Water Quality Monitoring Organizations:** Independent organizations, such as environmental NGOs, may conduct their own water quality testing and publish reports.\n* **News Outlets:** Local news sources might cover issues related to water quality in the area.\n\n**Important Notes:**\n\n* **Be cautious of unofficial or anecdotal information:** The quality can vary significantly depending on location within the dam, time of year, and other factors. \n* **Always check official sources for the most up-to-date information.**\n* **Exercise caution if you are planning to swim or engage in water sports in Hartebeesport Dam.**\n\nI hope this helps you find the information you need. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "write a report on water hyacinths at the harbeespoort dam\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "##  Hartebeesport Dam: Battling the Invasive Water Hyacinth\n\n**Introduction:**\n\nHartebeesport Dam, a popular tourist destination in South Africa, is facing a growing threat from invasive water hyacinths (Eichhornia crassipes). This fast-growing plant poses a significant challenge to the dam's ecosystem and recreational activities. This report aims to examine the current situation, the impact of water hyacinths, and potential solutions.\n\n**Current Situation:**\n\n* **Rapid Proliferation:** Water hyacinths are rapidly spreading across the dam, forming dense mats that cover the surface.\n* **Negative Impact on Ecosystem:** The dense mats block sunlight, reducing oxygen levels and impacting aquatic life. \n* **Threat to Recreation:** Boating, fishing, and other recreational activities are severely affected by the hyacinth infestation.\n* **Economic Consequences:** Tourism and the fishing industry are suffering economic losses due to reduced access and diminished recreational opportunities.\n\n**Impact of Water Hyacinths:**\n\n* **Ecological Impacts:**\n    * Reduced biodiversity: The hyacinths outcompete native aquatic plants, leading to a decline in biodiversity.\n    *  Altered water chemistry: The decomposition of hyacinth mats depletes oxygen and increases nutrient levels, further impacting aquatic life.\n    * Habitat loss: Fish and other wildlife lose suitable habitats due to the dense mats.\n\n* **Economic Impacts:**\n    * Tourism decline: Tourists are deterred by the unsightly appearance of the dam and limited access to recreational activities.\n    * Fishing industry losses: Fish populations decline due to habitat loss and reduced oxygen levels, affecting the fishing industry.\n    * Water supply issues: The hyacinths can clog water intakes, impacting water supply for surrounding areas.\n\n**Solutions:**\n\n* **Mechanical Removal:** Physical removal using specialized machinery is a common approach, but it is costly and labor-intensive.\n* **Biological Control:** Introducing natural predators like weevils or grass carp can help control the population. However, careful monitoring is essential to avoid unintended consequences.\n* **Chemical Control:** Herbicides can be used to kill the hyacinths, but concerns remain about their impact on the ecosystem.\n* **Integrated Management:** A combination of mechanical, biological, and chemical methods is often the most effective approach. \n\n**Future Strategies:**\n\n* **Public Awareness:** Educating the public about the dangers of invasive species and encouraging responsible behavior (e.g., avoiding introduction of new plants) is crucial.\n* **Community Involvement:** Engaging local communities in control efforts and raising awareness can contribute to long-term success.\n* **Research and Monitoring:** Continued research is needed to develop more effective and sustainable control methods.\n\n**Conclusion:**\n\nThe water hyacinth infestation at Hartebeesport Dam presents a serious challenge that requires coordinated action from government agencies, local communities, and researchers. A multi-pronged approach involving mechanical, biological, and chemical methods, along with public awareness and community involvement, is essential for effective control and long-term management of this invasive species.\n\n\n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)