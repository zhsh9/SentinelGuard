from utils.plugin.template import PluginTemplate
from config import extract_server_config, API
from utils.config_parse import process_config
from openai import OpenAI
from httpx import Timeout
import requests
import json
import config


class LLM(PluginTemplate):
    def __init__(self, data=None, context="", prompt="", config_path=config.CONFIG_FILE_PATH):
        super().__init__(data)  # super variables: self.logs
        self.context = context
        self.prompt = prompt
        self.config = extract_server_config(config_path)

        # OpenAI API Token Configuration:
        self.api = API()
        self.api.extract_api_config(config_path)

    def input_data_handling(self, log):
        self.context_engineering()
        self.prompt_engineering(log)

    def detect(self, log):
        """
        Detect one log record using OpenAI's GPT service.
        :param log: one log record.
        :return: True or False | Detected Result.
        """
        # Generate context & prompt
        self.input_data_handling(log)

        # Create the messages for the Chat API
        messages = [
            {"role": "system", "content": self.context},
            {"role": "user",   "content": self.prompt}
        ]

        try:
            # Official OpenAI Service
            if self.api.active and self.api.service == 'openai':
                client = OpenAI(
                    api_key=self.api.api_key,  # defaults to os.environ.get("OPENAI_API_KEY")
                    organization=self.api.organization,
                    project=self.api.project,
                    base_url=self.api.base_url,
                    timeout=Timeout(2.0),
                    default_headers={"api-version": self.api.api_version}
                )

                response = client.chat.completions.create(
                    model=self.api.model,
                    messages=messages,
                    max_tokens=128
                )
                result = response.choices[0].message['content'].strip()
            # Azure OpenAI Service
            elif self.api.active and self.api.service == 'azure':
                headers = {
                    'Content-Type': 'application/json',
                    'api-key': self.api.api_key,
                }
                params = {
                    'api-version': self.api.api_version,
                }
                post_data = {
                    'messages': messages,
                }

                response = requests.post(
                    self.api.base_url,
                    params=params,
                    headers=headers,
                    json=post_data
                )
                response = json.loads(response.content)
                result = response['choices'][0]['message']['content'].strip()
            else:
                raise ValueError("API is not active or service is not recognized")

            return self.process_result(result)
        except Exception as e:
            print(f"Error calling OpenAI API: {e} \nwith api key: {self.api.api_key} on model: {self.api.model}")
            return None

    def format_log(self, log):
        """
        Format the log data into a string.
        :param log: log data dictionary.
        :return: formatted log string.
        """
        return (f"Host: {log['remote_host']}, Log Name: {log['log_name']}, "
                f"User: {log['remote_user']}, Time: {log['time']}, "
                f"Request: {log['request']}, Status: {log['status']}, "
                f"Bytes: {log['bytes']}, Referer: {log['referer']}, "
                f"User Agent: {log['user_agent']}")

    def context_engineering(self):
        # Generate context string from background information. (e.g. server name, config ...)
        context  = ""
        context += f"You are a network security assistant who helps analyze network traffic and identify possible "
        context += f"security threats. Following is the information about http server:\n"
        context += f"The server is {self.config['server']}. "
        context += f"The log file to be analysed: {self.config['logs']['file']['path'] if self.config['logs']['file']['active'] else 'No active log file'}"
        context += f"The configuration of {self.config['server']} is {self.config['server_config']['path']+':\n' if self.config['server_config']['active'] else 'No active configuration file'}"
        context += f"{process_config(self.config['server_config']['path']) if self.config['server_config']['active'] else ''}"
        self.context += context

    def prompt_engineering(self, log):
        # Generate prompt string to inform what GPT/LLM model is proposed to do and its output format.
        prompt  = ""
        prompt += f"Analyse this request as a Real-time HTTP Intrusion Detection System:\n"
        prompt += f"```\n{self.format_log(log)}\n```"
        prompt += f"Based on the request method, content, URL, and status code and etc, can you analyze whether this could be an intrusion attempt?"
        prompt += f"Please provide reasons for your analysis. Your response format:\n"
        prompt += f"- Result: [Yes/No]\n"
        prompt += f"- Reason: \n"
        prompt += f"- Analysis: \n"
        self.prompt += prompt

    def process_result(self, result):
        """
        Process the result returned by the GPT model.
        :param result: raw result from GPT model.
        :return: processed result.
        """
        # Implement specific logic to interpret the result
        # Here we just return the result as a boolean for simplicity
        return result.lower() in ["- Result: Yes"]
