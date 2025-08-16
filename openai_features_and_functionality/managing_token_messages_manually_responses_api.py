
from openai import OpenAI
import os
from dotenv import load_dotenv
import tiktoken


# send conversation turns and chain them manually.
# We defined a custom function num_tokens_from_messages to count tokens from a list of messages with tiktoken.
#This approach gives you detailed control over conversation state and token management—useful for fine‑tuning agent workflows and staying within token limits.
MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

# Create an OpenAI client instance
client = OpenAI(
    # Replace with your actual API key or use: api_key=os.environ.get("OPENAI_API_KEY")
    api_key= os.getenv("OPENAI_API_KEY")
)


def num_tokens_from_messages(messages, model ="gpt-4o-mini-2024-07-18") :
    """Return the number of tokens used by a list of messages"""

    num_tokens = 0

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: Model not found. Using o220k_base encoding.")
        encoding = tiktoken.get_encoding("o200k_base")

    if model in {
        "gpt-3.5-turbo-0125",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4o-mini-2024-07-18",
        "gpt-4o-2024-08-06"
    }:
        tokens_per_message = 3
        tokens_pername = 1
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0125")
    elif "gpt-4o-mini" in model:
        print("Warning: gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-mini-2024-07-18.")
        return num_tokens_from_messages(messages, model="gpt-4o-mini-2024-07-18")
    elif "gpt-4o" in model:
        print("Warning: gpt-4o and gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-2024-08-06.")
        return num_tokens_from_messages(messages, model="gpt-4o-2024-08-06")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {model}.")

    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
         num_tokens += len(encoding.encode(value))

         if key == "name":
             num_tokens += tokens_pername
             num_tokens += 3
    return num_tokens

article_headings = [
    "I. Introduction A. Definition of the 2008 Financial Crisis B. Overview of the Causes and Effects of the Crisis C. Importance of Understanding the Crisis",
    "II. Historical Background A. Brief History of the US Financial System B. The Creation of the Housing Bubble C. The Growth of the Subprime Mortgage Market",
    "III. Key Players in the Crisis A. Government Entities B. Financial Institutions C. Homeowners and Borrowers",
    "IV. Causes of the Crisis A. The Housing Bubble and Subprime Mortgages B. The Role of Investment Banks and Rating Agencies C. The Failure of Regulatory Agencies D. Deregulation of the Financial Industry",
    "V. The Domino Effect A. The Spread of the Crisis to the Global Financial System B. The Impact on the Real Economy C. The Economic Recession",
    "VI. Government Responses A. The Troubled Asset Relief Program (TARP) B. The American Recovery and Reinvestment Act C. The Dodd-Frank Wall Street Reform and Consumer Protection Act",
    "VII. Effects on Financial Institutions A. Bank Failures and Bailouts B. Stock Market Decline C. Credit Freeze",
    "VIII. Effects on Homeowners and Borrowers A. Foreclosures and Bankruptcies B. The Loss of Home Equity C. The Impact on Credit Scores",
    "IX. Effects on the Global Economy A. The Global Financial Crisis B. The Impact on Developing Countries C. The Role of International Organizations",
    "X. Criticisms and Controversies A. Bailouts for Financial Institutions B. Government Intervention in the Economy C. The Role of Wall Street in the Crisis",
    "XI. Lessons Learned A. The Need for Stronger Regulation B. The Importance of Transparency C. The Need for Better Risk Management",
    "XII. Reforms and Changes A. The Dodd-Frank Wall Street Reform and Consumer Protection Act B. Changes in Regulatory Agencies C. Changes in the Financial Industry",
    "XIII. Current Economic Situation A. Recovery from the Crisis B. Impact on the Job Market C. The Future of the US Economy",
    "XIV. Comparison to Previous Financial Crises A. The Great Depression B. The Savings and Loan Crisis C. The Dot-Com Bubble",
    "XV. Economic and Social Impacts A. The Widening Wealth Gap B. The Rise of Populist Movements C. The Long-Term Effects on the Economy",
    "XVI. The Role of Technology A. The Use of Technology in the Financial Industry B. The Impact of Technology on the Crisis C. The Future of the Financial Industry",
    "XVII. Conclusion A. Recap of the Causes and Effects of the Crisis B. The Importance of Learning from the Crisis C. Final Thoughts",
    "XVIII. References A. List of Sources B. Additional Reading C. Further Research",
    "XIX. Glossary A. Key Terms B. Definitions",
    "XX. Appendix A. Timeline of the Crisis B. Financial Statements of Key Players C. Statistical Data on the Crisis",
]

#setup the system prompt
system_prompt = "You are a helpful assistant for a financial news website. You are writing a series of articles about the 2008 financial crisis. You have been given a list of headings for each article. You need to write a short paragraph for each heading. You can use the headings as a starting point for your writing.\n\n"
system_prompt += "All of the subheadings:\n"

#setup up the message list:
messages = []

for heading in article_headings:
    system_prompt += f"{heading}\n"

#Append the first system message
messages.append({"role":
    "system",
    "content":
        system_prompt})

#If the token conut  goes over the limit, the last messahe will be removed
MAX_TOKEN_SIZE = 2048

response = client.responses.create(
    model = MODEL,
    input=messages,
    store=False
)

messages.append({"role":
    "assistant",
    "content":
        response.output_text})

print("Current message count", len(messages))
print ("Current token count", num_tokens_from_messages(messages))

 # Whilst the Chat history object is more than 2048 tokens, remove the oldest non-system/developer message:
while num_tokens_from_messages(messages, model='gpt-4o-mini') > MAX_TOKEN_SIZE:
    #find the index of the first message that is not a system or developer messages
    non_system_msg_index = next(
        ( i for i, msg in enumerate(messages) if msg["role"] not in ["system", "developer"]), None
        )

    if non_system_msg_index is not None:
            messages.pop(non_system_msg_index)
            print("Removed a message to reduce token count!")
