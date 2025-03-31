from openai import OpenAI
from api_resource import *
import base64

def get_gpt_model():
    model = OpenAI(api_key=openai_api)
    return model

def prompt_gpt4o(model, prompt, image_path=None, demonstrations=None):
    """
    Generates a response from the GPT-4o model using optional image input,
    and supports adding demonstration examples.

    Args:
        model: The GPT-4o model instance.
        prompt (str): The text prompt for the model.
        image_path (str, optional): The file path of the image. Defaults to None.
        demonstrations (list of tuples, optional):
            A list of (demo_query, demo_image_path, demo_answer).
            Each tuple is used as a demonstration example before the final prompt.

    Returns:
        str: The model's response text.
    """
    try:
        messages = []

        # 1. Add demonstration pairs, if any
        if demonstrations:
            for (demo_query, demo_image_path, demo_answer) in demonstrations:
                # (A) User demonstration message
                user_content = [{"type": "text", "text": demo_query}]

                if demo_image_path:
                    # Convert demo image to base64
                    with open(demo_image_path, "rb") as image_file:
                        base64_image = f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
                    user_content.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": base64_image},
                        }
                    )

                messages.append({"role": "user", "content": user_content})

                # (B) Assistant demonstration message (the "answer")
                assistant_content = [{"type": "text", "text": demo_answer}]
                messages.append({"role": "assistant", "content": assistant_content})

        # 2. Add the final user prompt
        final_user_content = [{"type": "text", "text": prompt}]

        if image_path:
            # Convert final prompt image to base64
            with open(image_path, "rb") as image_file:
                base64_image = f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
            final_user_content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": base64_image},
                }
            )

        messages.append({"role": "user", "content": final_user_content})

        # 3. Generate response from the model
        response = model.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.01,
            max_tokens=4096,
        )

        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"An error occurred while querying the GPT-4o model: {e}")


if __name__ == "__main__":
    gpt_client = get_gpt_model()
    resp = prompt_gpt4o(gpt_client, "where is the capital of China?")
    print(resp)