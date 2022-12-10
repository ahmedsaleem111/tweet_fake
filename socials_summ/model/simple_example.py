import cohere
co = cohere.Client('PRIVATE-KEY')

prompt = f"""January: Happy to be back in Tokyo for the season! :)
March: Went bowling with my buddies today, had lots of fun
June: Finally graduated from UCSD in Japanese literature!!!
August: In Paris for summer, would be happy to meet with my local friends

TLDR: Moved to Tokyo, graduated from UCSD in Japanese literature, and had summer vacation in Paris.
--
February: I'm happy to announce that I've decided to move to Oxford for work. Please wish me good luck 😀
November: Happy thanksgiving everyone!!!
December: This Christmas I've been volunteering at Cats and Dogs in Oxford. They are desperately in need of support, please donate guys!

TLDR: Moved to Oxford for work, volunteered at Cats and Dogs during Christmas.
--
February: Finally proposed to Gabriela! We're getting married in October.
October: Wow what a great wedding 😍😍😍
November: On honeymoon in South Africa, they have the cutest penguins!

TLDR:"""

response = co.generate(
    model='xlarge',
    prompt = prompt,
    max_tokens=40,
    temperature=0.8,
    stop_sequences=["--"])
