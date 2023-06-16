import sys
import argparse
import requests
import openai


class arg_input():
    def __init__(self, arg_input):
        self._arg_input = arg_input
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-n', metavar='n', type=int, help='an integer for processing')
        self._parser.add_argument('--idea', metavar='idea', type=str, help='a string for processing')

    def depatch_input(self):
        args = self._parser.parse_args()          
        return args.n, args.idea


class gpt_dalle():
    def __init__(self, n, idea):
        self._n = n
        self._idea = idea
        self._key = "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"
    
    def prompt_gpt(self):
        
        openai.api_key = self._key
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "DALL-E 2 is an AI art generation model. Below is a list of example prompts:"},
                {"role": "system", "content": "- hedgehog smelling a flower | clear blue sky | intricate artwork by Beatrix Potter | cottagecore aesthetic"},
                {"role": "system", "content": "- a big large happy kawaii Shiba-inu puppy in a futuristic abandoned city, anime movie, IMAX, cinematic lighting"},
                {"role": "system", "content": "- a photo of cat flying out to space as an astronaut, digital art"},
                {"role": "system", "content": "I want you to write me a list of {} detailed prompts exactly about the idea written after IDEA. \
                Follow the structure of the example prompts. This means a very short description of the scene, followed by modifiers divided by \
                commas to alter the mood, style, lighting, and more. Do not use bullet points or quotes. Separate each prompt with a new line and \
                just give me the pure answer".format(self._n)},
                {"role": "user", "content": "IDEA: {}".format(self._idea)},
        ]
        )
        return response['choices'][0]['message']['content']
        
    def dalle(self, idea):
        openai.api_key = self._key
        response = openai.Image.create(
        prompt=idea,
        n=1,
        size="512x512"
        )
        return response['data'][0]['url']
    
    def image_downloader(self):

        ideas = self.prompt_gpt()
        image_index = 0
        for i in ideas.split('\n'):
            print(i[2:])
            url = self.dalle(i[2:])
            response = requests.get(url)
            if response.status_code == 200:
                image_index += 1
                with open('output{}.png'.format(image_index), 'wb') as f:
                    f.write(response.content)

if __name__ == "__main__": 
    args = arg_input(sys.argv)
    gpt = gpt_dalle(args.depatch_input()[0], args.depatch_input()[1])
    gpt.image_downloader()
