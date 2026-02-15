from openai import OpenAI
from config.settings import get_api_key, LLM_MODEL

class Generator:

    def __init__(self):
        self.client = OpenAI(
            api_key=get_api_key(),
            base_url="https://api.groq.com/openai/v1"
        )

    def gerar(self, pergunta, contexto, historico):
        try:
            messages = [
                    {
                        "role": "system",
                        "content": """
                    Você é um assistente que responde apenas com base no contexto fornecido.
                    Se a resposta não estiver no contexto, diga:
                    "Não encontrei essa informação na base de dados."
                    Não invente informações.
                    """
                    }

            ]

            for remetente, msg in historico[-6:]:
                role = "assistant" if remetente == "GIGI" else "user"
                messages.append({"role": role, "content": msg})

            prompt = f"""
            CONTEXTO:
            {contexto}

            PERGUNTA ATUAL:
            {pergunta}
            """

            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
                temperature=0.2
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"

